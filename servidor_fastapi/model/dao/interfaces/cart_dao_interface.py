from abc import ABC, abstractmethod
from typing import List
from model.dto.cart_item import CartItem
from model.dto.add_to_cart_input import AddToCartInput

class CartDAOInterface(ABC):
    @abstractmethod
    def get_cart_for_user(self, user_id: str) -> List[CartItem]:
        """Obtiene los elementos del carrito para un usuario dado."""
        pass

    @abstractmethod
    def add_to_cart(self, user_id: str, add_to_cart: AddToCartInput) -> None:
        """Añade un producto al carrito para un usuario."""
        pass

    @abstractmethod
    def update_cart_item(self, user_id: str, product_id: str, quantity: int) -> None:
        """Actualiza la cantidad de un producto en el carrito para un usuario."""
        pass

    @abstractmethod
    def delete_cart_item(self, user_id: str, product_id: str) -> None:
        """Elimina un producto del carrito para un usuario."""
        pass

    @abstractmethod
    def clear_cart(self, user_id: str) -> None:
        """Vacía el carrito para un usuario."""
        pass