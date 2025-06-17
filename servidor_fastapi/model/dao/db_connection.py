import sqlite3
from sqlite3 import Connection

DATABASE_PATH = "./model/dao/midb.sqlite3" # Ruta actualizada del archivo SQLite

def get_db_connection() -> Connection:
    """Crea y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
    return conn