from fastapi import FastAPI, Request, HTTPException, APIRouter, Form
from pydantic import BaseModel
import json
from view.view import View
from model.model import Model
from model.dto.user_profile import UserProfile

router = APIRouter()

view = View()
model = Model()

# Endpoint para obtener el perfil de un artista por su ID
@router.get("/getArtistProfile/{artist_id}", description="Obtener perfil de artista por ID")
def get_artist_profile(request: Request, artist_id: str):
    try:
        artist_profile = model.get_user_by_id(artist_id)  # Obtiene el perfil del artista desde el modelo
        return view.getPerfilArtista(request, artist_profile)  # Renderiza la vista del perfil del artista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para obtener el perfil de un usuario por su ID
@router.get("/getUserProfile/{user_id}", description="Obtener perfil de usuario por ID")
def get_user_profile(request: Request, user_id: str):
    try:
        user_profile = model.get_user_by_id(user_id)  # Obtiene el perfil del usuario desde el modelo
        return view.getPerfilUsuario(request, user_profile)  # Renderiza la vista del perfil del usuario
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# Endpoint para obtener el menú de opciones del artista
@router.get("/getMenuArtista", description="Obtener menú de artista")
def get_menu_artista(request: Request):
    try:
        return view.getMenuArtista(request)  # Renderiza la vista del menú del artista
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para actualizar el nombre de usuario
@router.post("/UpdateProfileUser/{user_id}", description="Actualizar el nombre de usuario")
def update_profile_user(user_id: str, username: str = Form(...)):
    """
    Actualiza el nombre de usuario.
    Recibe el ID del usuario y el nuevo nombre desde un formulario.
    """
    try:
        model.update_user(user_id, username)  # Llama al modelo para actualizar el usuario
        return {"message": "Nombre de usuario actualizado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint para actualizar el nombre de usuario y el nombre de banda del artista
@router.post("/UpdateProfileUserArtist/{user_id}", description="Actualizar el nombre de artista y el nombre de banda")
def update_profile_user_artist(user_id: str, username: str = Form(...), bandname: str = Form(...)):
    """
    Actualiza el nombre de usuario y el nombre de banda del artista.
    Recibe el ID del usuario, el nuevo nombre de usuario y el nuevo nombre de banda desde un formulario.
    """
    try:
        model.update_artist(user_id, username, bandname)  # Llama al modelo para actualizar el perfil del artista
        return {"message": "Perfil de artista actualizado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))