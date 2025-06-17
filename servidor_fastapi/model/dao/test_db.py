from model.dao.db_connection import get_db_connection

def check_data():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Verificar usuarios
        print("Usuarios:")
        for row in cursor.execute("SELECT * FROM usuarios"):
            print(dict(row))
        
        # Verificar productos
        print("\nProductos:")
        for row in cursor.execute("SELECT * FROM productos"):
            print(dict(row))
        
        # Verificar carrito
        print("\nCarrito:")
        for row in cursor.execute("SELECT * FROM carrito"):
            print(dict(row))
        
        # Verificar comentarios
        print("\nComentarios:")
        for row in cursor.execute("SELECT * FROM comentarios"):
            print(dict(row))

if __name__ == "__main__":
    check_data()