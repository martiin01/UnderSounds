import pytest
from model.dao.implementations.user_dao import UserDAO
from model.dao.exceptions import EntityNotFoundError
from model.dto.user_profile import UserProfile

def test_get_user_by_id_found():
    dao = UserDAO()
    user = dao.get_user_by_id("1")  # Asegúrate de que el usuario con ID 1 exista en la base de datos de prueba
    assert user.id == "1"

def test_get_user_by_id_not_found():
    dao = UserDAO()
    with pytest.raises(EntityNotFoundError):
        dao.get_user_by_id("9999")  # ID que no existe
