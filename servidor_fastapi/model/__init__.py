import os
import json
import sqlite3
from model.dao.db_connection import DATABASE_PATH, get_db_connection

def initialize_database():
    """Inicializa la base de datos con el esquema definido y carga datos iniciales desde un JSON
    solo si la base de datos es nueva o las tablas están vacías."""

    db_exists = os.path.exists(DATABASE_PATH)
    if not db_exists:
        print(f"Creando nueva base de datos en {DATABASE_PATH}.")

    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Crear el esquema (tablas, etc.) si no existen
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        try:
            with open(schema_path, "r", encoding="utf-8") as schema_file:
                conn.executescript(schema_file.read())
            print("Esquema de la base de datos verificado/creado.")
        except Exception as e:
            print(f"Error al ejecutar el script del esquema: {e}")
            return

        # 2. Verificar si la tabla 'usuarios' está vacía antes de insertar datos iniciales
        try:
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            user_count = cursor.fetchone()[0]

            if user_count == 0:
                print("La tabla 'usuarios' está vacía. Insertando datos iniciales...")
                data_path = os.path.join(os.path.dirname(__file__), "initial_data.json")
                with open(data_path, "r", encoding="utf-8") as data_file:
                    data = json.load(data_file)

                # Insertar datos en la tabla 'usuarios'
                for user in data.get("usuarios", []):
                    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = ?", (user["id"],))
                    exists = cursor.fetchone()[0]

                    if exists == 0:
                        cursor.execute(
                            "INSERT INTO usuarios (id, username, email, tipo_usuario, nombre_banda) VALUES (?, ?, ?, ?, ?, ?)",
                            (
                                user["id"],
                                user["username"],
                                user["email"],
                                user["tipo_usuario"],
                                user.get("nombre_banda"),
                            )
                        )
                        print(f"Usuario insertado: {user['username']}")
                    else:
                        print(f"El usuario con ID {user['id']} ya existe. No se insertará.")

                conn.commit()
                print("Datos iniciales insertados correctamente.")
            else:
                print("La base de datos ya contiene datos en 'usuarios'. No se insertarán datos iniciales.")

        except sqlite3.Error as e:
            print(f"Error de SQLite al verificar/insertar datos: {e}")
            conn.rollback()
        except KeyError as e:
            print(f"Error: Falta la clave '{e}' en initial_data.json para alguna entrada.")
            conn.rollback()
        except Exception as e:
            print(f"Error inesperado durante la inicialización de datos: {e}")
            conn.rollback()

# Para poder ejecutar este script directamente si es necesario (opcional)
if __name__ == "__main__":
    initialize_database()