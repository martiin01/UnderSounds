from abc import ABC, abstractmethod
from typing import List
from model.dto.forum import Forum  # Se asume que tienes un DTO Forum definido

class ForumDAOInterface(ABC):
    @abstractmethod
    def get_all_forum_posts(self) -> List[Forum]:
        """Obtiene todos los posts del foro."""
        pass

    @abstractmethod
    def get_forum_posts_by_user(self, product_id: str) -> List[Forum]:
        """Obtiene todos los posts del foro para un producto específico."""
        pass

    @abstractmethod
    def create_forum_post(self, forum_post: Forum) -> Forum:
        """Crea un nuevo post en el foro."""
        pass

    @abstractmethod
    def update_forum_post(self, user_id: str, product_id: str, new_critica: str) -> None:
        """Modifica la crítica de un usuario para un producto específico."""
        pass

    @abstractmethod
    def delete_forum_post(self, forum_id: str) -> None:
        """Elimina un post del foro por su ID."""
        pass
    
    @abstractmethod
    def get_forum_posts_by_artist(self, artist_id: int) -> List[Forum]:
        """Obtiene todos los posts del foro para productos cuyos autores sean el artista indicado."""
        pass