from fastapi import FastAPI, Request, HTTPException, APIRouter
from pydantic import BaseModel
import json
from view.view import View
from model.model import Model
from datetime import datetime
from model.dto.product import Product

router = APIRouter()

view = View()
model = Model()

# Endpoint para obtener todos los productos en la página principal sin iniciar sesión
@router.get("/allproductsPrincipalNo_log", description="Obtener todos los productos")
def get_all_productsPagPrincipal(request: Request):
    try:
        products = model.get_all_products()  # Obtiene todos los productos desde el modelo
        return view.getPrincipalNo_Log(request, products)  # Renderiza la vista correspondiente
    except Exception as e:
        # --- Añade estas líneas para depurar ---
        import traceback
        print("------ ERROR EN /allproductsPrincipalNo_log ------")
        traceback.print_exc() # Imprime el traceback completo en los logs de Docker
        print("-------------------------------------------------")
        # --- Fin de líneas añadidas ---
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los productos en la página principal para artistas
@router.get("/allproductsPrincipalArtista", description="Obtener todos los productos")
def get_all_productsPagPrincipalArtista(request: Request):
    try:
        products = model.get_all_products()
        return view.getPrincipalArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener todos los productos en la página principal para usuarios
@router.get("/allproductsPrincipalUsuario", description="Obtener todos los productos")
def get_all_productsPagPrincipalUsuario(request: Request):
    try:
        products = model.get_all_products()
        return view.getPrincipalUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsExplorarNo_log", description="Obtener todos los productos")
def get_all_productsExplorar(request: Request):
    try:
        # Se asume que model.get_all_products() retorna una cadena JSON
        products = model.get_all_products()
        return view.getExplorarNo_Log(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsExplorarArtista", description="Obtener todos los productos")
def get_all_productsExplorar(request: Request):
    try:
        # Se asume que model.get_all_products() retorna una cadena JSON
        products = model.get_all_products()
        return view.getExplorarArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsExplorarUsuario", description="Obtener todos los productos")
def get_all_productsExplorar(request: Request):
    try:
        # Se asume que model.get_all_products() retorna una cadena JSON
        products = model.get_all_products()
        return view.getExplorarUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obtener productos por tipo (CDs) sin iniciar sesión
@router.get("/allproductsCdsNo_log", description="Obtener todos los productos")
def get_all_productsExpCdsNo_log(request: Request):
    try:
        products = model.get_products_by_type("D.Compactos")  # Filtra productos por tipo
        return view.getPag_CdsNo_Log(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   
@router.get("/allproductsCdsUser", description="Obtener todos los productos")
def get_all_productsExpCdsUsuario(request: Request):
    try:
        products = model.get_products_by_type("D.Compactos")
        return view.getPag_CdsUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

@router.get("/allproductsCdsArtist", description="Obtener todos los productos")
def get_all_productsExpCdsArtista(request: Request):
    try:
        products = model.get_products_by_type("D.Compactos")
        return view.getPag_CdsArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsVinilosNo_log", description="Obtener todos los productos")
def get_all_productsExpVinilosNo_log(request: Request):
    try:
        products = model.get_products_by_type("Vinilos")
        return view.getPag_VinilosNo_Log(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsVinilosUser", description="Obtener todos los productos")
def get_all_productsExpVinilosUsuario(request: Request):
    try:
        products = model.get_products_by_type("Vinilos")
        return view.getPag_VinilosUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsVinilosArtist", description="Obtener todos los productos")
def get_all_productsExpVinilosArtista(request: Request):
    try:
        products = model.get_products_by_type("Vinilos")
        return view.getPag_VinilosArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsCamisetasNo_log", description="Obtener todos los productos")
def get_all_productsCamisetasNo_log(request: Request):
    try:
        products = model.get_products_by_type("Camisetas")
        return view.getPag_CamisetasNo_Log(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsCamisetasUser", description="Obtener todos los productos")
def get_all_productsCamisetasUsuario(request: Request):
    try:
        products = model.get_products_by_type("Camisetas")
        return view.getPag_CamisetasUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/allproductsCamisetasArtist", description="Obtener todos los productos")
def get_all_productsCamisetasArtista(request: Request):
    try:
        products = model.get_products_by_type("Camisetas")
        return view.getPag_CamisetasArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsCassettesNo_log", description="Obtener todos los productos de tipo cassette")
def get_all_productsCassettesNo_log(request: Request):
    try:
        products = model.get_products_by_type("Cassettes")
        return view.getPag_CassettesNo_Log(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsCassettesUser", description="Obtener todos los productos")
def get_all_productsCassettesUsuario(request: Request):
    try:
        products = model.get_products_by_type("Cassettes")
        return view.getPag_CassettesUsuario(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/allproductsCassettesArtist", description="Obtener todos los productos")
def get_all_productsCassettesArtista(request: Request):
    try:
        products = model.get_products_by_type("Cassettes")
        return view.getPag_CassettesArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




# Endpoint para obtener un producto por su ID (producto_id es string)
@router.get("/getDetalleDiscoNo_log/{product_id}", description="Obtener producto por ID")
def getDetalleDiscoNo_log(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)  # `product_id` is extracted from the URL
        return view.getDetalleDiscoNo_Log(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener un producto por su ID (producto_id es string)
@router.get("/getDetalleDiscoUsuario/{product_id}", description="Obtener producto por ID")
def getDetalleDiscoUsuario(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)  # `product_id` is extracted from the URL
        return view.getDetalleDiscoUsuario(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obtener un producto por su ID (producto_id es string)
@router.get("/getDetalleDiscoArtista/{product_id}", description="Obtener producto por ID")
def getDetalleDiscoArista(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)  # `product_id` is extracted from the URL
        return view.getDetalleDiscoArtista(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getDetalleCamisetaNo_log/{product_id}", description="Obtener producto por ID")
def getDetalleCamisetaNo_log(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)
        return view.getDetalleCamisetaNo_Log(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
# Endpoint para obtener un producto por su ID (producto_id es string)
@router.get("/getDetalleProductoArtista/{product_id}", description="Obtener producto por ID")
def getDetalleproductoArtista(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)
        return view.getDetalleDiscoArtista(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para obtener un producto por su ID (producto_id es string)
@router.get("/getDetalleProductoUsuario/{product_id}", description="Obtener producto por ID")
def getDetalleproductoUsuario(request: Request, product_id: str):
    try:
        product = model.get_product_by_id(product_id)
        return view.getDetalleDiscoUsuario(request, product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint nuevo para obtener todos los productos en un json DUDA
@router.get("/allproductsUsuarioJson", description="Obtener todos los productos y devolver en JSON")
def get_all_productsPagPrincipal(request: Request):
    try:
        # Se asume que model.get_all_products() retorna una cadena JSON
        products = model.get_all_products()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getProdMusicalesArtista/{user_id}", description="Obtener productos por usuario")
def get_productos_by_user(request: Request, user_id: str):
    try:
        products = model.get_products_by_author(user_id)
        return view.getProductosMusicales(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/getSubirProdMusicales", description="Obtener productos por usuario")
def getSubirProdMusicales(request: Request):
    try:
        return view.getSubirProdMusicales(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getSubirMerch", description="Obtener productos por usuario")
def getSubirMerch(request: Request):
    try:
        return view.getSubirMerch(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getMerchandisingArtista/{user_id}", description="Obtener merchandising por usuario")
def get_merchandising_artista(request: Request, user_id: str):
    try:
        products = model.get_products_by_author(user_id)
        return view.getMerchandisingArtista(request, products)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para crear un nuevo producto
@router.post("/productos/nuevo/{user_id}", description="Crear un nuevo producto")
def create_product(request: Request, user_id: str, nombre: str, product_type: str, precio: float, imagen: str, estilo: str = ""):
    try:
        product_data = {
            "id": "",  # El ID se asignará automáticamente
            "nombre": nombre,
            "imagen": imagen,
            "precio": precio,
            "fecha": datetime.now().isoformat(),  # Fecha actual
            "tipo": product_type,
            "estilo": estilo,
            "autor": user_id,  # ID del usuario que crea el producto
        }
        product = Product.model_validate(product_data)  # Valida los datos del producto
        model.create_product(product)  # Llama al modelo para crear el producto
        return {"message": "Producto creado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))