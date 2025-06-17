from abc import ABC, abstractmethod
from typing import List
from model.dto.product import Product

class ProductDAOInterface(ABC):
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        """Obtiene todos los productos"""
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Product:
        """Obtiene un producto por su ID"""
        pass

    @abstractmethod
    def create_product(self, product: Product) -> Product:
        """Crea un nuevo producto"""
        pass

    @abstractmethod
    def update_product(self, product_id: str, product: Product) -> Product:
        """Actualiza un producto existente"""
        pass

    @abstractmethod
    def delete_product(self, product_id: str) -> None:
        """Elimina un producto por su ID"""
        pass

    @abstractmethod
    def get_products_by_type(self, product_type: str) -> List[Product]:
        """Obtiene todos los productos de un tipo específico"""
        pass

    @abstractmethod
    def get_product_by_user(self, user_id: str) -> List[Product]:
        """Obtiene todos los productos creados por un usuario específico"""
        pass

    @abstractmethod
    def get_product_by_author(self, author: str) -> List[Product]:
        """Obtiene todos los productos cuyo autor coincida con el parámetro"""
        pass