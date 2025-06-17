from typing import List
from model.dao.db_connection import get_db_connection
from model.dao.interfaces.user_dao_interface import UserDAOInterface
from model.dto.user_profile import UserProfile
from model.dao.exceptions import EntityNotFoundError

class UserDAO(UserDAOInterface):
    def get_all_users(self) -> List[UserProfile]:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, email, tipo_usuario, nombre_banda FROM usuarios")
            rows = cursor.fetchall()
            return [
                UserProfile(
                    id=str(row["id"]),
                    username=row["username"],
                    email=row["email"],
                    tipo_usuario=row["tipo_usuario"],
                    nombre_banda=row["nombre_banda"]
                )
                for row in rows
            ]

    def get_user_by_id(self, user_id: str) -> UserProfile:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email, tipo_usuario, nombre_banda FROM usuarios WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return UserProfile(
                    id=str(row["id"]),
                    username=row["username"],
                    email=row["email"],
                    tipo_usuario=row["tipo_usuario"],
                    nombre_banda=row["nombre_banda"]
                )
        raise EntityNotFoundError(f"Usuario con ID {user_id} no encontrado")

    def create_user(self, user: UserProfile) -> UserProfile:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuarios (id, username, email, tipo_usuario, nombre_banda)
                VALUES (?, ?, ?, ?, ?)
                """,
                (user.id, user.username, user.email, user.tipo_usuario, user.nombre_banda)
            )
            conn.commit()
        return user

    def update_user(self, user_id: str, user: UserProfile) -> UserProfile:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE usuarios
                SET username = ?
                WHERE id = ?
                """,
                (user.username, user_id)  # Solo se pasan los parámetros necesarios
            )
            if cursor.rowcount == 0:
                raise EntityNotFoundError(f"Usuario con ID {user_id} no encontrado")
            conn.commit()
        return user
    
    def update_user_artist(self, user_id: str, user: UserProfile) -> UserProfile:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE usuarios
                SET username = ?, nombre_banda = ?
                WHERE id = ?
                """,
                (user.username,user.nombre_banda, user_id)  # Solo se pasan los parámetros necesarios
            )
            if cursor.rowcount == 0:
                raise EntityNotFoundError(f"Usuario con ID {user_id} no encontrado")
            conn.commit()
        return user
    
    def delete_user(self, user_id: str) -> None:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
            if cursor.rowcount == 0:
                raise EntityNotFoundError(f"Usuario con ID {user_id} no encontrado")
            conn.commit()

    def get_user_type(self, user_id: str) -> str:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT tipo_usuario FROM usuarios WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return row["tipo_usuario"]
        raise EntityNotFoundError(f"Usuario con ID {user_id} no encontrado")