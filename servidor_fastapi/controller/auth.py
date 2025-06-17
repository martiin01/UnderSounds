from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from view.view import View
from fastapi import Response, status # Añadir Response y status
from fastapi.responses import RedirectResponse 

# Es buena práctica usar APIRouter para organizar las rutas
router = APIRouter()
view = View()

@router.get("/Usuario/logInUsuario/login.html", response_class=HTMLResponse)
async def show_login_page(request: Request):
    """
    Muestra la página de inicio de sesión unificada (loginLog.html).
    Esta ruta solo sirve el HTML. La lógica de autenticación y la
    redirección posterior ocurren en el JavaScript de la página,
    que llama al endpoint API /auth/login.
    """
    try:
        # Llama al método de la vista que renderiza loginLog.html
        # Pasamos un diccionario vacío porque no necesita datos especiales del servidor
        # para mostrar el formulario inicial.
        return view.getLogInUsuario(request, login={})
    except Exception as e:
        # Considera loggear el error 'e' para depuración
        print(f"Error al cargar la página de login: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cargar la página de inicio de sesión.")

@router.get("/Usuario/regUsuario/registro.html", response_class=HTMLResponse)
async def show_user_register_page(request: Request):
    """
    Muestra la página de registro para usuarios normales (registro.html).
    Esta ruta solo sirve el HTML. La lógica de registro ocurre en el
    JavaScript de la página, que llama al endpoint API /auth/register.
    """
    try:
        # Llama al método de la vista que renderiza registro.html
        return view.getRegistroUsuario(request, registro={})
    except Exception as e:
        print(f"Error al cargar la página de registro de usuario: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cargar la página de registro.")

@router.get("/Artista/regArtista/registro_artista.html", response_class=HTMLResponse)
async def show_artist_register_page(request: Request):
    """
    Muestra la página de registro para artistas (registro_artista.html).
    Esta ruta solo sirve el HTML. La lógica de registro ocurre en el
    JavaScript de la página, que llama al endpoint API /auth/register.
    """
    try:
        # Llama al método de la vista que renderiza registro_artista.html
        return view.getRegistroArtista(request, registro={})
    except Exception as e:
        print(f"Error al cargar la página de registro de artista: {e}")
        raise HTTPException(status_code=500, detail="No se pudo cargar la página de registro de artista.")


@router.post("/logout", status_code=status.HTTP_303_SEE_OTHER, description="Cierra la sesión del usuario eliminando la cookie")
async def logout(response: Response):
    """
    Cierra la sesión del usuario eliminando la cookie 'user_session_id'
    y redirige a la página principal sin sesión.
    Usamos POST para seguir las buenas prácticas (logout cambia el estado del servidor).
    Usamos 303 See Other para la redirección después de un POST.
    """
    print("DEBUG: Endpoint /logout llamado. Eliminando cookie user_session_id.")
    # Instruye al navegador para eliminar la cookie
    response = RedirectResponse(url="/allproductsPrincipalNo_log", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="user_session_id", path="/") 
    return response
