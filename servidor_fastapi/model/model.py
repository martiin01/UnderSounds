from model.dao.implementations.product_dao import ProductDAO
from model.dao.implementations.user_dao import UserDAO
from model.dao.implementations.cart_dao import CartDAO
from model.dao.implementations.forum_dao import ForumDAO

from model.dto.product import Product
from model.dto.user_profile import UserProfile
from model.dto.forum import Forum # ¡Asegúrate que este DTO use user_id: str!
from model.dto.add_to_cart_input import AddToCartInput
from model.dto.cart_item import CartItem # Import CartItem

class Model:
    def __init__(self):
        # Inicialización de los DAO individuales
        self.product_dao = ProductDAO()
        self.user_dao = UserDAO()
        self.cart_dao = CartDAO()
        self.forum_dao = ForumDAO()

    # --- Métodos para Productos ---
    def get_all_products(self) -> list[Product]:
        return self.product_dao.get_all_products()

    def get_product_by_id(self, product_id: str) -> Product: # Mantenido como int
        return self.product_dao.get_product_by_id(product_id)

    def create_product(self, product: Product) -> Product:
        """Inserta un nuevo producto en la base de datos."""
        # Asegúrate que product.autor sea str (Firebase UID)
        return self.product_dao.create_product(product)

    def update_product(self, product_id: str, product: Product) -> Product: # Mantenido como int
        """Actualiza un producto existente en la base de datos."""
        # Asegúrate que product.autor sea str (Firebase UID)
        return self.product_dao.update_product(product_id, product)

    def delete_product(self, product_id: str) -> None: # Mantenido como int
        """Elimina un producto de la base de datos."""
        self.product_dao.delete_product(product_id)
        
    def get_product_by_user(self, user_id: str) -> list[Product]:
        """Obtiene todos los productos creados por un usuario específico."""
        return self.product_dao.get_products_by_user(user_id)

    def get_products_by_type(self, product_type: str) -> list[Product]:
        """Obtiene todos los productos de un tipo específico."""
        return self.product_dao.get_products_by_type(product_type)
    
    
    

    # --- Métodos para Usuarios ---
    def get_all_users(self) -> list[UserProfile]:
        return self.user_dao.get_all_users()

    def get_user_by_id(self, user_id: str) -> UserProfile: # Correcto como str
        return self.user_dao.get_user_by_id(user_id)

    def create_user(self, user: UserProfile) -> UserProfile:
        """Inserta un nuevo usuario en la base de datos."""
        return self.user_dao.create_user(user)

    def update_user(self, user_id: str, username: str) -> None:
        """Actualiza el nombre de usuario en la base de datos."""
        user_profile = self.get_user_by_id(user_id)  # Obtener el perfil actual del usuario
        user_profile.username = username  # Actualizar solo el nombre de usuario
        self.user_dao.update_user(user_id, user_profile)

    def update_artist(self, user_id: str, username: str,  bandname: str) -> None:
        """Actualiza el nombre de usuario en la base de datos."""
        user_profile = self.get_user_by_id(user_id)  # Obtener el perfil actual del usuario
        user_profile.username = username  # Actualizar solo el nombre de usuario
        user_profile.nombre_banda = bandname  # Actualizar solo el nombre de la banda
        # Asegúrate que el DAO actualice ambos campos
        self.user_dao.update_user_artist(user_id, user_profile)

    def delete_user(self, user_id: str) -> None: # Correcto como str
        """Elimina un usuario de la base de datos."""
        self.user_dao.delete_user(user_id)

    def get_user_type(self, user_id: str) -> str: # Correcto como str
        """Obtiene el tipo de usuario por su ID"""
        return self.user_dao.get_user_type(user_id)
    
    def get_products_by_author(self, author: str) -> list[Product]:
        """Obtiene todos los productos cuyo autor coincida con el parámetro."""
        return self.product_dao.get_product_by_author(author)
    
    

    # --- Métodos para Carrito ---
    def get_cart_for_user(self, user_id: str) -> list[CartItem]:
        """Obtiene los elementos del carrito para un usuario específico."""
        return self.cart_dao.get_cart_for_user(user_id)

    def add_to_cart(self, user_id: str, add_to_cart: AddToCartInput): # user_id: str, product_id: int
        """Agrega un producto al carrito para el usuario indicado."""
        # add_to_cart debe contener product_id como int
        self.cart_dao.add_to_cart(user_id, add_to_cart)

    def update_cart_item(self, user_id: str, product_id: int, quantity: int): # user_id: str, product_id: int
        """Actualiza la cantidad de un producto en el carrito para un usuario."""
        self.cart_dao.update_cart_item(user_id, product_id, quantity)

    def delete_cart_item(self, user_id: str, product_id: int): # user_id: str, product_id: int
        """Elimina un producto del carrito para un usuario."""
        self.cart_dao.delete_cart_item(user_id, product_id)

    def clear_cart(self, user_id: str): # Correcto como str
        """Vacía el carrito para un usuario."""
        self.cart_dao.clear_cart(user_id)

    def subtract_from_cart(self, user_id: str, product_id: str, quantity: int):
        self.cart_dao.subtract_from_cart(user_id, product_id, quantity)


    # --- Métodos para Foro ---
    def get_forum_posts_by_user(self, user: str) -> list[Forum]: # Cambiado a int
        return self.forum_dao.get_forum_posts_by_user(user)

    def get_forum_posts_by_artist(self, artist_id: str) -> list[Forum]: # Correcto como str (asumiendo artist_id es user_id)
        # ¡Importante! Asegúrate que ForumDAO use str para artist_id si es necesario
        return self.forum_dao.get_forum_posts_by_artist(artist_id)

    def create_forum_post(self, forum_post: Forum) -> Forum:
        # ¡Importante! Asegúrate que el DTO Forum use user_id: str y product_id: int
        return self.forum_dao.create_forum_post(forum_post)

    def update_forum_post(self, forum_id: int, forum_post: Forum) -> Forum: # Mantenido como int
        self.forum_dao.update_forum_post(forum_id, forum_post) # Pasar int al DAO   

    def delete_forum_post(self, forum_id: int) -> None: # Mantenido como int
        self.forum_dao.delete_forum_post(forum_id) # Pasar int al DAO