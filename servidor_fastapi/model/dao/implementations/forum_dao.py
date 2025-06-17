import sqlite3
from typing import List
from model.dao.db_connection import get_db_connection
from model.dao.interfaces.forum_dao_interface import ForumDAOInterface
from model.dto.forum import Forum

class ForumDAO(ForumDAOInterface):
    def get_all_forum_posts(self) -> List[Forum]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, idUser, idProducto, critica FROM foro")
        rows = cur.fetchall()
        posts = [Forum(id=row["id"], idUser=row["idUser"], idProducto=row["idProducto"], critica=row["critica"]) for row in rows]
        conn.close()
        return posts

    def get_forum_posts_by_user(self, user_id: str) -> List[Forum]:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, idUser, idProducto, critica FROM foro WHERE idUser = ?", (user_id,))
        rows = cur.fetchall()
        posts = [Forum(id=row["id"], idUser=row["idUser"], idProducto=row["idProducto"], critica=row["critica"]) for row in rows]
        conn.close()
        return posts

    def create_forum_post(self, forum_post: Forum) -> Forum:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO foro (idUser, idProducto, critica) VALUES (?, ?, ?)",
            (forum_post.idUser, forum_post.idProducto, forum_post.critica),
        )
        conn.commit()
        forum_post.id = cur.lastrowid
        conn.close()
        return forum_post

    def update_forum_post(self, user_id: str, product_id: str, new_critica: str) -> None:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE foro SET critica = ? WHERE idUser = ? AND idProducto = ?",
            (new_critica, user_id, product_id),
        )
        conn.commit()
        conn.close()

    def delete_forum_post(self, forum_id: str) -> None:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM foro WHERE id = ?", (forum_id,))
        conn.commit()
        conn.close()

    def get_forum_posts_by_artist(self, artist_id: int) -> List[Forum]:
        """
        Devuelve todos los posts del foro para productos cuyo autor es el artista indicado.
        Se realiza un JOIN entre la tabla foro y la tabla productos.
        """
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT f.id, f.idUser, f.idProducto, f.critica
            FROM foro f
            JOIN productos p ON f.idProducto = p.id
            WHERE p.autor = ?
        """
        cur.execute(query, (artist_id,))
        rows = cur.fetchall()
        posts = [
            Forum(
                id=row["id"],
                idUser=row["idUser"],
                idProducto=row["idProducto"],
                critica=row["critica"],
            )
            for row in rows
        ]
        conn.close()
        return posts