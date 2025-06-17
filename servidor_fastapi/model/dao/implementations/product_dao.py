from typing import List
# from datetime import datetime # No se usa para actualizar fecha, se usa la del DTO
from model.dao.db_connection import get_db_connection
from model.dao.interfaces.product_dao_interface import ProductDAOInterface
from model.dto.product import Product # Importar el DTO actualizado
import sqlite3 # Para manejo de errores específicos si es necesario
import uuid # Si necesitas generar IDs

class ProductDAO(ProductDAOInterface):
    def __init__(self):
        pass

    def _map_row_to_product(self, row: sqlite3.Row) -> Product:
        """Mapea una fila de la base de datos a un objeto Product DTO."""
        if not row:
            return None
        try:
            product_data = {
                "id": str(row["id"]),
                "nombre": row["nombre"],
                "imagen": row["imagen"],
                "precio": row["precio"],
                "fecha": row["fecha"],
                "tipo": row["tipo"],
                "estilo": row["estilo"],
                "autor": str(row["autor"]) 
            }
            return Product.model_validate(product_data)
        except Exception as e:
            print(f"Error al mapear fila a Product DTO: {dict(row)}. Error: {e}")
            raise 

    def get_all_products(self) -> List[Product]:
        """Lee todos los productos de la BD y los convierte a DTO."""
        products: List[Product] = []
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, nombre, imagen, precio, fecha, tipo, estilo, autor
                      FROM productos
                    """
                )
                rows = cursor.fetchall()
                for row in rows:
                    try:
                        product = self._map_row_to_product(row)
                        if product:
                            products.append(product)
                    except Exception as map_error:
                        print(f"Error mapeando producto con ID {row['id']}: {map_error}")
                        continue 
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en get_all_products: {db_error}")
            raise db_error
        return products

    def get_product_by_id(self, product_id: str) -> Product:
        """Recupera un producto por su ID, lanza ValueError si no existe."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, nombre, imagen, precio, fecha, tipo, estilo, autor
                      FROM productos
                     WHERE id = ?
                    """,
                    (product_id,)
                )
                row = cursor.fetchone()
                if not row:
                    raise ValueError(f"Producto con ID '{product_id}' no encontrado")

                return self._map_row_to_product(row)
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en get_product_by_id para ID {product_id}: {db_error}")
            raise db_error

    def create_product(self, product: Product) -> Product:
        """Inserta un nuevo producto. Asume que el ID ya está en el objeto Product si no es autogenerado."""
        if not product.id:
             product.id = str(uuid.uuid4())
             print(f"Generado nuevo ID para producto: {product.id}")

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO productos
                      (id, nombre, imagen, precio, fecha, tipo, estilo, autor)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        product.id, # Usar el ID del DTO (generado o proporcionado)
                        product.nombre,
                        product.imagen,
                        float(product.precio),
                        product.fecha,
                        product.tipo, 
                        product.estilo,
                        product.autor,
                    ),
                )
                conn.commit()
            return product
        except sqlite3.IntegrityError as e:
             print(f"Error de integridad al crear producto (¿ID duplicado? ¿FK inválido?): {e}")
             raise ValueError(f"No se pudo crear el producto debido a una restricción: {e}") from e
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en create_product: {db_error}")
            raise db_error

    def update_product(self, product_id: str, product: Product) -> Product:
        """Actualiza un producto existente y devuelve el DTO actualizado."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE productos
                       SET nombre = ?, imagen = ?, precio = ?, fecha = ?, tipo = ?, estilo = ?, autor = ?
                     WHERE id = ?
                    """,
                    (
                        product.nombre,
                        product.imagen,
                        float(product.precio),
                        product.fecha, 
                        product.tipo, 
                        product.estilo,
                        product.autor,
                        product_id,
                    ),
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"Producto con ID '{product_id}' no encontrado para actualizar")
                conn.commit()
            product.id = product_id
            return product
        except sqlite3.IntegrityError as e:
             print(f"Error de integridad al actualizar producto ID {product_id} (¿FK inválido?): {e}")
             raise ValueError(f"No se pudo actualizar el producto debido a una restricción: {e}") from e
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en update_product para ID {product_id}: {db_error}")
            raise db_error

    def delete_product(self, product_id: str) -> None:
        """Elimina un producto de la BD."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (product_id,))
                if cursor.rowcount == 0:
                    print(f"Advertencia: Se intentó eliminar producto con ID '{product_id}' pero no se encontró.")
                conn.commit()
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en delete_product para ID {product_id}: {db_error}")
            raise db_error

    def get_product_by_user(self, user_id: str) -> List[Product]:
        """Recupera todos los productos cuyo 'autor' coincide con el user_id."""
        products: List[Product] = []
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, nombre, imagen, precio, fecha, tipo, estilo, autor
                      FROM productos
                     WHERE autor = ?
                    """,
                    (user_id,)
                )
                rows = cursor.fetchall()
                for row in rows:
                     try:
                        product = self._map_row_to_product(row)
                        if product:
                            products.append(product)
                     except Exception as map_error:
                        print(f"Error mapeando producto con ID {row['id']} para usuario {user_id}: {map_error}")
                        continue
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en get_product_by_user para usuario {user_id}: {db_error}")
            raise db_error
        return products

    def get_products_by_type(self, product_type: str) -> List[Product]:
        """Recupera todos los productos cuyo 'tipo' coincide con el tipo especificado."""
        products: List[Product] = []
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT id, nombre, imagen, precio, fecha, tipo, estilo, autor
                      FROM productos
                     WHERE tipo = ?
                    """,
                    (product_type,)
                )
                rows = cursor.fetchall()
                for row in rows:
                    try:
                        product = self._map_row_to_product(row)
                        if product:
                            products.append(product)
                    except Exception as map_error:
                        print(f"Error mapeando producto con ID {row['id']} para tipo {product_type}: {map_error}")
                        continue
        except sqlite3.Error as db_error:
            print(f"Error de base de datos en get_products_by_type para tipo {product_type}: {db_error}")
            raise db_error
        return products
    
    def get_product_by_author(self, author: str) -> List[Product]:
            """Recupera todos los productos cuyo 'autor' coincide con el parámetro author."""
            products: List[Product] = []
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT id, nombre, imagen, precio, fecha, tipo, estilo, autor
                        FROM productos
                        WHERE autor = ?
                        """,
                        (author,)
                    )
                    rows = cursor.fetchall()
                    for row in rows:
                        try:
                            product = self._map_row_to_product(row)
                            if product:
                                products.append(product)
                        except Exception as map_error:
                            print(f"Error mapeando producto con ID {row['id']} para autor {author}: {map_error}")
                            continue
            except sqlite3.Error as db_error:
                print(f"Error de base de datos en get_product_by_author para autor {author}: {db_error}")
                raise db_error
            return products