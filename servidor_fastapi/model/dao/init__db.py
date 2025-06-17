import os
import json
import sqlite3 # Import sqlite3 for specific error handling if needed
from model.dao.db_connection import DATABASE_PATH, get_db_connection

def initialize_database():
    """Inicializa la base de datos con el esquema definido y carga datos iniciales desde un JSON
    solo si la base de datos aún no existe."""

    # Verifica si la base de datos NO existe aún
    if not os.path.exists(DATABASE_PATH):
        print(f"La base de datos no existe en {DATABASE_PATH}. Creando e inicializando...")
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                # --- 1. Ejecutar schema.sql para crear las tablas ---
                schema_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "schema.sql"))
                try:
                    with open(schema_path, "r", encoding="utf-8") as schema_file:
                        conn.executescript(schema_file.read())
                    print("Esquema de la base de datos creado con éxito.")
                except FileNotFoundError:
                    print(f"Error: No se encontró el archivo de esquema en {schema_path}")
                    return # No continuar si no se puede crear el esquema
                except Exception as e:
                    print(f"Error al ejecutar el schema SQL desde {schema_path}: {e}")
                    return # No continuar si falla la creación del esquema

                # --- 2. Cargar datos iniciales desde el archivo JSON ---
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                data_path = os.path.join(BASE_DIR, "initial_data.json")
                try:
                    with open(data_path, "r", encoding="utf-8") as data_file:
                        data = json.load(data_file)
                    print(f"Datos iniciales cargados desde {data_path}.")
                except FileNotFoundError:
                    print(f"Advertencia: No se encontró el archivo de datos iniciales en {data_path}. Se creará una base de datos vacía.")
                    data = {} # Crear un diccionario vacío para evitar errores más adelante
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar el archivo JSON {data_path}: {e}")
                    return # No continuar si el JSON es inválido
                except Exception as e:
                    print(f"Error inesperado al leer {data_path}: {e}")
                    return

                # --- 3. Insertar datos en las tablas ---
                try:
                    # Insertar datos en la tabla 'usuarios'
                    for user in data.get("usuarios", []):
                        try:
                            cursor.execute(
                                "INSERT INTO usuarios (id, username, email, tipo_usuario, nombre_banda) VALUES (?, ?, ?, ?, ?)",
                                (
                                    user.get("id"), # Usar .get() para seguridad
                                    user.get("username"),
                                    user.get("email"),
                                    user.get("tipo_usuario"),
                                    user.get("nombre_banda"), # .get() maneja si la clave no existe
                                )
                            )
                            print(f"Usuario insertado: {user.get('username', 'ID Desconocido')}")
                        except KeyError as e:
                            print(f"Error de clave al insertar usuario: Falta la clave {e} en {user}")
                        except sqlite3.IntegrityError as e:
                             print(f"Error de integridad al insertar usuario {user.get('username', 'ID Desconocido')}: {e}")
                        except Exception as e:
                             print(f"Error inesperado al insertar usuario {user.get('username', 'ID Desconocido')}: {e}")


                    # Insertar datos en la tabla 'productos'
                    for producto in data.get("productos", []):
                        try:
                            cursor.execute(
                                "INSERT INTO productos (id, nombre, imagen, precio, fecha, tipo, estilo, autor) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                (
                                    producto.get("id"),
                                    producto.get("nombre"),
                                    producto.get("imagen"),
                                    producto.get("precio"),
                                    producto.get("fecha"),
                                    producto.get("tipo"),
                                    producto.get("estilo"),
                                    producto.get("autor"),
                                )
                            )
                            print(f"Producto insertado: {producto.get('nombre', 'ID Desconocido')}")
                        except KeyError as e:
                            print(f"Error de clave al insertar producto: Falta la clave {e} en {producto}")
                        except sqlite3.IntegrityError as e:
                             print(f"Error de integridad al insertar producto {producto.get('nombre', 'ID Desconocido')}: {e}")
                        except Exception as e:
                             print(f"Error inesperado al insertar producto {producto.get('nombre', 'ID Desconocido')}: {e}")

                    # Insertar datos en la tabla 'carrito'
                    for item in data.get("carrito", []):
                        try:
                            cursor.execute(
                                "INSERT INTO carrito (idUser, idProducto, cantidad) VALUES (?, ?, ?)",
                                (item.get("idUser"), item.get("idProducto"), item.get("cantidad"))
                            )
                            # print(f"Item de carrito insertado para usuario {item.get('idUser')}") # Opcional, puede ser mucho log
                        except KeyError as e:
                            print(f"Error de clave al insertar item de carrito: Falta la clave {e} en {item}")
                        except sqlite3.IntegrityError as e:
                             print(f"Error de integridad al insertar item de carrito para usuario {item.get('idUser')}: {e}")
                        except Exception as e:
                             print(f"Error inesperado al insertar item de carrito para usuario {item.get('idUser')}: {e}")

                    # Insertar datos en la tabla 'comentarios'
                    for comentario in data.get("comentarios", []):
                        try:
                            cursor.execute(
                                "INSERT INTO comentarios (id_producto, id_usuario, comentario) VALUES (?, ?, ?)",
                                (comentario.get("id_producto"), comentario.get("id_usuario"), comentario.get("comentario"))
                            )
                            # print(f"Comentario insertado para producto {comentario.get('id_producto')}")
                        except KeyError as e:
                            print(f"Error de clave al insertar comentario: Falta la clave {e} en {comentario}")
                        except sqlite3.IntegrityError as e:
                             print(f"Error de integridad al insertar comentario para producto {comentario.get('id_producto')}: {e}")
                        except Exception as e:
                             print(f"Error inesperado al insertar comentario para producto {comentario.get('id_producto')}: {e}")

                    # --- 4. Confirmar todos los cambios ---
                    conn.commit()
                    print("Datos iniciales confirmados (commit) en la base de datos.")

                except Exception as e:
                    print(f"Error durante la inserción de datos iniciales: {e}")
                    conn.rollback() # Deshacer cambios si algo falló durante la inserción
                    print("Rollback realizado debido a error en la inserción.")

        except sqlite3.Error as e:
            print(f"Error de SQLite al conectar o inicializar la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado al obtener la conexión a la base de datos: {e}")

    else:
        # Si la base de datos ya existe, no hacemos nada
        print(f"La base de datos ya existe en {DATABASE_PATH}. No se requiere inicialización.")