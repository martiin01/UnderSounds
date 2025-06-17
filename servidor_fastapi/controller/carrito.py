from fastapi import FastAPI, Request, HTTPException, APIRouter
from view.view import View
from model.model import Model
from model.dto.add_to_cart_input import AddToCartInput
from fastapi import Request, HTTPException
import json

router = APIRouter()
view = View()
model = Model()


@router.get("/carritoNo_log")
def get_cartNo_log(request: Request):
    try:
        print("DEBUG: Sirviendo plantilla carrito1_NoLog.html")
        return view.getCarritoNo_Log(request, {}) # Pasar diccionario vacío
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/carritoUsuario/{user_id}")
def get_cartUsuario(request: Request, user_id: str):
    try:
        data = model.get_cart_for_user(user_id)
        
        return view.getCarritoUsuario(request, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/carritoArtista/{user_id}")
def get_cartArtista(request: Request, user_id: str):
    try:
        data = model.get_cart_for_user(user_id)
        cart = json.loads(data) if isinstance(data, str) else data
        return view.getCarritoArtista(request, cart)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/carrito/add/{user_id}/{product_id}")
def add_product_to_cart(request: Request, user_id: str, product_id: str, quantity: int = 1):
    """
    Endpoint para agregar un producto al carrito.
    Recibe el id del usuario y el id del producto en la ruta.
    """
    try:
        add_input = AddToCartInput(product_id=product_id, quantity=quantity)
        model.add_to_cart(user_id, add_input)
        return {"message": "Producto añadido al carrito correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/carrito/subtract/{user_id}/{product_id}")
def subtract_product_from_cart(request: Request, user_id: str, product_id: str, quantity: int = 1):
    """
    Endpoint para restar una cantidad de un producto en el carrito.
    Recibe el id del usuario y el id del producto en la ruta.
    Solo se restará si la cantidad actual es mayor que 1.
    """
    try:
        # Llamamos a la función subtract_from_cart del modelo
        model.subtract_from_cart(user_id, product_id, quantity)
        return {"message": "Cantidad actualizada en el carrito correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/carrito/delete/{user_id}/{product_id}")
def delete_product_from_cart(request: Request, user_id: str, product_id: str):
    """
    Endpoint para eliminar un producto del carrito.
    Recibe el id del usuario y el id del producto en la ruta.
    """
    try:
        model.delete_cart_item(user_id, product_id)
        return {"message": "Producto eliminado del carrito correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
