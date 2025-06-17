from abc import ABC, abstractmethod
from typing import List
from model.dto.user_profile import UserProfile

class UserDAOInterface(ABC):
    @abstractmethod
    def get_all_users(self) -> List[UserProfile]:
        """Obtiene todos los usuarios"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> UserProfile:
        """Obtiene un usuario por su ID"""
        pass

    @abstractmethod
    def create_user(self, user: UserProfile) -> UserProfile:
        """Crea un nuevo usuario"""
        pass

    @abstractmethod
    def update_user(self, user_id: str, user: UserProfile) -> UserProfile:
        """Actualiza un usuario existente"""
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> None:
        """Elimina un usuario por su ID"""
        pass

    @abstractmethod
    def get_user_type(self, user_id: str) -> str:
        """Obtiene el tipo de usuario por su ID"""
        pass