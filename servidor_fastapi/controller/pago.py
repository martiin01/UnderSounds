import os
import stripe
import json
from fastapi import APIRouter, Request, Depends, HTTPException, Body, Header, Response, Cookie
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime
from pydantic import ValidationError

from view.view import View
# from controller.checkout_api_impl import CheckoutApiImpl # No longer needed
from model.dao.implementations.cart_dao import CartDAO
from model.dao.implementations.user_dao import UserDAO

# --- Configuration ---
load_dotenv()
STRIPE_SECRET_KEY = "xxxxxxxxxxxxx"
STRIPE_PUBLISHABLE_KEY = "xxxxxxxxxxxxx"
# Cambia esto por tu publishable key real
STRIPE_WEBHOOK_SECRET = "xxxxxx" # Cambia esto por tu webhook real
# STRIPE_WEB

if not all([STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, STRIPE_WEBHOOK_SECRET]):
    print("Warning: Stripe environment variables not fully configured.")
    # raise Exception("Stripe API keys or webhook secret not found.")

stripe.api_key = STRIPE_SECRET_KEY

# --- Pydantic Model for Guest Payment Intent ---
class CreateGuestPaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Total amount in cents")

# --- Controller Class ---
class PagoController:
    # Updated __init__ to include ComprasDAO
    def __init__(self, view: View, cart_dao: CartDAO,  user_dao: UserDAO):
        self.router = APIRouter(tags=["Pago"], prefix="/pago")
        self.view = view
        self.cart_dao = cart_dao
        self.user_dao = user_dao
        self._register_routes()

    # --- Get User Identifier (Registered or None) ---
    async def get_current_user_identifier(self, request: Request) -> Optional[str]:
        user_id = request.cookies.get("user_session_id")
        return user_id if user_id else None

    # --- Calculate Amount (Only for Registered Users) ---
        # --- Calculate Amount (Only for Registered Users) ---
    def _calculate_registered_user_order_amount(self, user_id: str) -> int:
        if not user_id:
             raise ValueError("User ID is required to calculate amount from cart.")

        print(f"DEBUG _calculate: Fetching cart for user {user_id}") # Log 1
        cart_items = self.cart_dao.get_cart_for_user(user_id)
        print(f"DEBUG _calculate: Cart items fetched: {cart_items}") # Log 2: Mira qué devuelve el DAO

        if not cart_items:
            print(f"DEBUG _calculate: Cart is empty for user {user_id}.") # Log 3
            # Decide si carrito vacío debe ser error 400 o simplemente 0 (Stripe fallará igual si es < 50)
            # Lanzar error es más claro para el usuario.
            raise ValueError("Cannot proceed to payment, the cart is empty.")

        total_cents = 0
        print(f"DEBUG _calculate: Starting loop for {len(cart_items)} items.") # Log 4
        for i, item in enumerate(cart_items):
            print(f"--- Item {i+1} ---") # Log 5
            # Usa getattr con default None para distinguir entre 0 y ausente
            price_value_raw = getattr(item, 'precio', None)
            quantity_raw = getattr(item, 'cantidad', None)
            product_id = getattr(item, 'id', 'Unknown')

            print(f"DEBUG _calculate: Item {i+1} raw data: product_id={product_id}, price='{price_value_raw}', quantity='{quantity_raw}'") # Log 6

            # Validación y limpieza
            if price_value_raw is None or quantity_raw is None:
                print(f"Warning: Missing price or quantity for product {product_id}. Skipping.")
                continue

            try:
                # Limpiar precio: quitar '$', espacios, y reemplazar ',' por '.'
                price_str_cleaned = str(price_value_raw).replace('$', '').replace(',', '.').strip()
                price_float = float(price_str_cleaned)

                # Validar cantidad
                quantity_int = int(quantity_raw)
                if quantity_int <= 0:
                     print(f"Warning: Invalid quantity ({quantity_int}) for product {product_id}. Skipping.")
                     continue

                # Calcular céntimos
                price_cents = int(price_float * 100)
                item_total = quantity_int * price_cents
                total_cents += item_total
                print(f"DEBUG _calculate: Item {i+1} processed: price_cents={price_cents}, quantity={quantity_int}, item_total={item_total}, running_total={total_cents}") # Log 7

            except (ValueError, TypeError) as e:
                print(f"Warning: Invalid format for product {product_id} (price='{price_value_raw}', quantity='{quantity_raw}'). Error: {e}. Skipping.") # Log 8
                continue

        print(f"DEBUG _calculate: Final calculated total_cents = {total_cents}") # Log 9
        if total_cents < 50: # Stripe minimum charge
             print(f"DEBUG _calculate: Total {total_cents} is below minimum 50.") # Log 10
             raise ValueError("Order amount is below the minimum required for payment (€0.50).")

        return total_cents

    async def _handle_successful_registered_payment(self, user_id: str) -> None:
        """
        Handles post-payment actions for a REGISTERED user after successful
        payment confirmation via webhook. Clears the user's cart.
        """
        print(f"Handling successful payment for registered user: {user_id}. Clearing cart.")
        # 1. Check if cart exists (optional, clear_cart might handle non-existent)
        try:
            cart_items = self.cart_dao.get_cart_for_user(user_id)
            if not cart_items:
                print(f"Info: Cart was already empty for user {user_id} during webhook processing.")
                return # Nothing to clear
        except Exception as e:
            # Log the error but proceed to attempt clearing anyway,
            # as the payment was successful.
            print(f"Warning: Could not verify cart items before clearing for user {user_id}: {e}")

        # 2. Clear Cart
        try:
            self.cart_dao.clear_cart(user_id)
            print(f"Successfully cleared cart for user {user_id}")
        except Exception as e:
            print(f"CRITICAL: Error clearing cart for user {user_id} after successful payment: {e}")
            # Log this critically. Payment succeeded, but cart remains.
            # Don't raise HTTPException here as payment is done, but ensure logging.
            # Consider adding monitoring for these cases.


    def _register_routes(self):
        @self.router.get("", response_class=HTMLResponse)
        async def get_payment_page(request: Request):
            if not STRIPE_PUBLISHABLE_KEY:
                 raise HTTPException(status_code=500, detail="Stripe configuration error (Publishable Key missing).")
            try:
                context_data = {"stripe_pk": STRIPE_PUBLISHABLE_KEY}
                user_id = await self.get_current_user_identifier(request)
                print(f"DEBUG: User ID from cookie in /pago GET: {user_id}")

                if user_id:
                    # --- USUARIO LOGUEADO: Calcular total del carrito SIEMPRE ---
                    total_cents = 0
                    try:
                        total_cents = self._calculate_registered_user_order_amount(user_id)
                        context_data["total_amount_euros"] = f"{total_cents / 100:.2f}"
                        print(f"DEBUG: Serving getPagoUsuario/Artista for user {user_id}. Cart total: {total_cents} cents")
                    except ValueError as e: # Ej: Carrito vacío
                        print(f"Info: Cannot calculate total for user {user_id} (likely empty cart): {e}")
                        context_data["total_amount_euros"] = "0.00"
                    except Exception as e:
                        print(f"Error calculating total for user {user_id}: {e}")
                        context_data["total_amount_euros"] = "Error"

                    # Determinar tipo y servir plantilla
                    user_details = self.user_dao.get_user_by_id(user_id)
                    user_type = getattr(user_details, 'tipo_usuario', 'usuario') # Asegúrate que el atributo sea 'tipo_usuario'

                    if user_type == 'artista':
                        return self.view.getPagoArtista(request, pago=context_data)
                    else:
                        return self.view.getPagoUsuario(request, pago=context_data)
                else:
                    # --- INVITADO: No calcular total aquí ---
                    print("DEBUG: No user_id found, serving getPagoNo_Log")
                    # No pasamos total_amount_euros, pago_NoLog.html lo calcula desde sessionStorage
                    return self.view.getPagoNo_Log(request, pago=context_data)

            except Exception as e:
                print(f"Error loading payment page: {e}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail="Could not load payment page.")

        @self.router.post("/create-payment-intent")
        async def create_payment_intent(
            request: Request, # Acepta la request cruda
            user_id: Optional[str] = Depends(self.get_current_user_identifier) # Mantiene la dependencia para user_id
        ):
            print(f"DEBUG /create-payment-intent POST: user_id from dependency = {user_id}")
            if not stripe.api_key:
                 raise HTTPException(status_code=500, detail="Stripe configuration error (Secret Key missing).")

            amount_cents = 0
            metadata = {}
            # guest_data: Optional[CreateGuestPaymentIntentRequest] = None # No se usa como parámetro directo

            try:
                if user_id:
                    # --- USUARIO LOGUEADO: Calcular desde carrito ---
                    print(f"DEBUG /create-payment-intent POST: User identified ({user_id}). Calculating from cart.")
                    try:
                        amount_cents = self._calculate_registered_user_order_amount(user_id)
                        metadata["user_id"] = user_id
                        print(f"DEBUG /create-payment-intent POST: Calculated amount_cents={amount_cents} for user {user_id}")
                    except ValueError as cart_error: # Captura error de cálculo (ej: carrito vacío/bajo)
                         print(f"ERROR en _calculate_registered_user_order_amount para user {user_id}: {cart_error}")
                         # Lanza 400 directamente si el cálculo falla
                         raise HTTPException(status_code=400, detail=str(cart_error))

                else:
                    # --- INVITADO: Parsear y validar body manualmente ---
                    print(f"DEBUG /create-payment-intent POST: Guest user. Attempting to parse body.")
                    try:
                        # Lee el cuerpo JSON solo si no hay user_id
                        body_json = await request.json()
                        # Valida manualmente contra el modelo Pydantic
                        guest_data = CreateGuestPaymentIntentRequest(**body_json)
                        print(f"DEBUG /create-payment-intent POST: Parsed guest_data.amount: {guest_data.amount}")
                        amount_cents = guest_data.amount
                        # Re-valida mínimo (Pydantic's gt=0 ya lo hizo, pero por seguridad)
                        if amount_cents < 50:
                            raise ValueError("Order amount is below the minimum required for payment (€0.50).")
                    except ValidationError as e: # Captura errores de validación Pydantic
                        print(f"ERROR /create-payment-intent POST: Invalid guest data body: {e}")
                        # Lanza 422 si el body no coincide con el modelo
                        raise HTTPException(status_code=422, detail=e.errors())
                    except json.JSONDecodeError:
                        print("ERROR /create-payment-intent POST: Invalid JSON body for guest.")
                        raise HTTPException(status_code=400, detail="Invalid JSON body.")
                    except ValueError as guest_amount_error: # Captura amount < 50
                         print(f"ERROR /create-payment-intent POST (Guest ValueError): {guest_amount_error}")
                         raise HTTPException(status_code=400, detail=str(guest_amount_error))
                    except Exception as parse_error: # Otros errores de parseo
                         print(f"ERROR /create-payment-intent POST: Error parsing guest body: {parse_error}")
                         raise HTTPException(status_code=400, detail="Could not parse request body.")

                # --- Crear Payment Intent (Común para ambos casos) ---
                # Asegura que el importe final sea válido antes de llamar a Stripe
                if amount_cents < 50:
                     # Esta validación puede ser redundante pero es segura
                     raise ValueError("Final amount is below the minimum required for payment (€0.50).")

                print(f"Attempting to create PaymentIntent with amount: {amount_cents} cents, metadata: {metadata}")
                intent = stripe.PaymentIntent.create(
                    amount=amount_cents,
                    currency="eur",
                    automatic_payment_methods={"enabled": True},
                    metadata=metadata
                )
                print(f"PaymentIntent created successfully: {intent.id}")
                return {"clientSecret": intent.client_secret}

            # --- Mantener Manejadores de Excepciones Generales ---
            except HTTPException as http_exc: # Re-lanzar excepciones HTTP específicas
                 raise http_exc
            except ValueError as e: # Captura validación final de importe u otros ValueErrors
                 print(f"ERROR /create-payment-intent (Outer ValueError): {e}")
                 raise HTTPException(status_code=400, detail=str(e))
            except stripe.error.StripeError as e:
                 print(f"Stripe API error: {e}")
                 raise HTTPException(status_code=502, detail=f"Payment provider error: {getattr(e, 'user_message', str(e))}")
            except Exception as e:
                 print(f"Error creating payment intent: {e}")
                 import traceback
                 traceback.print_exc()
                 raise HTTPException(status_code=500, detail="Could not initiate payment.")


        @self.router.post("/webhook")
        async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
            if not STRIPE_WEBHOOK_SECRET:
                print("Error: Stripe Webhook Secret not configured.")
                raise HTTPException(status_code=500, detail="Webhook configuration error.")
            payload = await request.body()
            event = None
            try:
                event = stripe.Webhook.construct_event(
                    payload, stripe_signature, STRIPE_WEBHOOK_SECRET
                )
            except ValueError as e:
                print(f"Webhook error: Invalid payload: {e}")
                raise HTTPException(status_code=400, detail="Invalid payload")
            except stripe.error.SignatureVerificationError as e:
                print(f"Webhook error: Invalid signature: {e}")
                raise HTTPException(status_code=400, detail="Invalid signature")
            except Exception as e:
                print(f"Webhook construction error: {e}")
                raise HTTPException(status_code=500, detail="Webhook processing error")

             # Handle the event
            if event['type'] == 'payment_intent.succeeded':
                payment_intent = event['data']['object']
                metadata = payment_intent.get('metadata', {})
                user_id = metadata.get('user_id')

                if user_id:
                    # --- REGISTERED USER ---
                    print(f'PaymentIntent succeeded for REGISTERED user: {user_id}')
                    try:
                        # *** Call the SIMPLIFIED method ***
                        await self._handle_successful_registered_payment(user_id) # <-- LLAMADA ACTUALIZADA
                        print(f"Post-payment handling (cart clear) completed for user {user_id}")
                    except Exception as e:
                        # Catch errors from _handle_successful_registered_payment
                        print(f"CRITICAL: Error during post-payment handling for user {user_id}: {e}")
                        # Return 500 to signal failure; Stripe might retry.
                        if isinstance(e, HTTPException):
                            raise e
                        else:
                            # Log thoroughly, but maybe don't raise 500 if cart clear fails?
                            # Depends on how critical cart clearing is vs. retries.
                            # For now, let's still raise 500 to indicate something went wrong.
                            raise HTTPException(status_code=500, detail="Post-payment handling failed.")
                else:
                    # --- GUEST USER ---
                    print('PaymentIntent succeeded for GUEST user.')
                    # No database action needed for guests in this simplified flow.

            # ... (manejo de otros eventos como payment_failed sin cambios) ...
            elif event['type'] == 'payment_intent.payment_failed':
                 payment_intent = event['data']['object']
                 metadata = payment_intent.get('metadata', {})
                 user_id = metadata.get('user_id', 'Guest')
                 print(f'PaymentIntent failed for user: {user_id}.')
            else:
                print(f'Unhandled event type {event["type"]}')

            return Response(status_code=200, content="Webhook received")


    def get_router(self):
        return self.router
