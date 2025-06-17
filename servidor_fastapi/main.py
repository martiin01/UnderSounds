from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates 
from firebase_admin import credentials, initialize_app
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import os

# Importar routers de los controladores
from controller.auth_api import router as AuthApiRouter
from controller.pago import PagoController # Import the class
from controller import productos, perfil, carrito, auth # Import modules with routers
from view.view import View # Necesario para PagoController 
from model.dao.implementations.cart_dao import CartDAO # Necesario para PagoController
from model.dao.implementations.user_dao import UserDAO

from controller import auth_api_impl 

# --- Inicialización Firebase y Lifespan ---
def initialize_firebase():
    cred_path = os.path.join(os.path.dirname(__file__), "firebaseClaves.json")
    if not os.path.exists(cred_path):
        print(f"Error: Firebase credentials file not found at {cred_path}")
        return
    try:
        cred = credentials.Certificate(cred_path)
        initialize_app(cred)
        print("Firebase Admin SDK inicializado correctamente.")
    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")

async def lifespan(app: FastAPI):
    from model.dao.init__db import initialize_database
    initialize_firebase()
    initialize_database()
    yield
    print("Shutting down application.")
# --- Fin Inicialización ---

app = FastAPI(
    title="Music E-Commerce API",
    description="API para gestionar usuarios, productos y compras.",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Montar Archivos Estáticos SIN prefijo /static ---
# Monta cada subdirectorio directamente en la ruta correspondiente
# Estas carpetas deben existir dentro de view/templates/
STATIC_DIRS = ["css", "js", "img", "json", "audio", "fonts"]
TEMPLATE_DIR = "view/templates"

for static_dir in STATIC_DIRS:
    dir_path = os.path.join(TEMPLATE_DIR, static_dir)
    if os.path.isdir(dir_path):
        app.mount(f"/{static_dir}", StaticFiles(directory=dir_path), name=static_dir)
        print(f"Mounted static directory: /{static_dir} -> {dir_path}")
    else:
        print(f"Warning: Static directory not found, skipping mount: {dir_path}")

# --- Instanciar dependencias para PagoController ---
view_instance = View()
cart_dao_instance = CartDAO()
user_dao_instance = UserDAO()

# --- Instanciar PagoController ---
pago_controller = PagoController(
    view=view_instance,
    cart_dao=cart_dao_instance,
    user_dao=user_dao_instance
)

# --- Incluir Routers ---
# API Endpoints
app.include_router(AuthApiRouter, tags=["Auth API"])

app.include_router(pago_controller.get_router(), tags=["Pago"]) 
# Rutas que sirven páginas HTML y datos asociados (SIN prefijo)
app.include_router(auth.router, tags=["Auth Pages"]) # Sin prefix
app.include_router(productos.router, tags=["Productos Pages"]) # Sin prefix
app.include_router(perfil.router, tags=["Perfil Pages"]) # Sin prefix
app.include_router(carrito.router, tags=["Carrito Pages"]) # Sin prefix
# --- Ruta Raíz ---
@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def root(request: Request):
    # Redirige a la página principal de productos para no logueados
    return RedirectResponse(url="/allproductsPrincipalNo_log")

# --- Ejecución (opcional, para desarrollo) ---
# if __name__ == "__main__":
#     import uvicorn
#     # Hay que asegurar que Uvicorn recargue cuando cambies archivos para desarrollo
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)