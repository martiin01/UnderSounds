from typing import List
import sqlite3
from model.dao.db_connection import get_db_connection
from model.dao.interfaces.cart_dao_interface import CartDAOInterface
from model.dto.cart_item import CartItem
from model.dto.add_to_cart_input import AddToCartInput

class CartDAO(CartDAOInterface):
    def get_cart_for_user(self, user_id: str) -> List[CartItem]:
        cart_items = []
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT p.id, p.nombre, p.imagen, p.precio, p.fecha, 
                           p.tipo, p.estilo, p.autor, c.cantidad
                    FROM carrito c
                    JOIN productos p ON c.idProducto = p.id
                    WHERE c.idUser = ?
                    """,
                    (user_id,)
                )
                rows = cursor.fetchall()
                for row in rows:
                    try:
                        # Se mapea la fila a un objeto CartItem
                        cart_item = CartItem(
                            id=row["id"],
                            nombre=row["nombre"],
                            imagen=row["imagen"],
                            precio=row["precio"],
                            fecha=row["fecha"],
                            tipo=row["tipo"],
                            estilo=row["estilo"],
                            autor=row["autor"],
                            cantidad=row["cantidad"]
                        )
                        if cart_item:
                            cart_items.append(cart_item)
                    except Exception as map_error:
                        print(f"Error mapeando producto con ID {row['id']}: {map_error}")
                        continue  # Saltar al siguiente producto
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en get_cart_for_user: {db_error}")
            raise db_error
        return cart_items

    def add_to_cart(self, user_id: str, add_to_cart: AddToCartInput) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM carrito WHERE idUser = ? AND idProducto = ?",
                (user_id, add_to_cart.product_id)
            )
            row = cursor.fetchone()
            if row:
                new_quantity = row["cantidad"] + add_to_cart.quantity
                cursor.execute(
                    "UPDATE carrito SET cantidad = ? WHERE idUser = ? AND idProducto = ?",
                    (new_quantity, user_id, add_to_cart.product_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO carrito (idUser, idProducto, cantidad) VALUES (?, ?, ?)",
                    (user_id, add_to_cart.product_id, add_to_cart.quantity)
                )
            conn.commit()

    def update_cart_item(self, user_id: str, product_id: str, quantity: int) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE carrito SET cantidad = ? WHERE idUser = ? AND idProducto = ?",
                (quantity, user_id, product_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("Producto no encontrado en el carrito")
            conn.commit()

    def delete_cart_item(self, user_id: str, product_id: str) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM carrito WHERE idUser = ? AND idProducto = ?",
                (user_id, product_id)
            )
            if cursor.rowcount == 0:
                raise ValueError("Producto no encontrado en el carrito")
            conn.commit()

    def clear_cart(self, user_id: str) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM carrito WHERE idUser = ?",
                (user_id,)
            )
            conn.commit()

    def subtract_from_cart(self, user_id: str, product_id: str, quantity: int) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cantidad FROM carrito WHERE idUser = ? AND idProducto = ?",
                (user_id, product_id)
            )
            row = cursor.fetchone()
            if row:
                current_quantity = row["cantidad"]
                if current_quantity > 1:
                    # Calcula la nueva cantidad, sin dejarla por debajo de 1  
                    new_quantity = current_quantity - quantity
                    if new_quantity < 1:
                        new_quantity = 1
                    cursor.execute(
                        "UPDATE carrito SET cantidad = ? WHERE idUser = ? AND idProducto = ?",
                        (new_quantity, user_id, product_id)
                    )
                    conn.commit()
                else:
                    # La cantidad ya es 1: no se realiza ninguna modificación
                    print(f"La cantidad del producto {product_id} para el usuario {user_id} ya es 1; no se puede restar.")
            else:
                print(f"No se encontró el producto {product_id} para el usuario {user_id} en el carrito.")