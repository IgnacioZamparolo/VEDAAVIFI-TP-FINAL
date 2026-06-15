import os
from db_connection import get_connection
from services.storage import subir_imagen

def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in ['jpg', 'png', 'jpeg', 'webp']

def obtener_todos_los_productos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM productos")
        resultado = cursor.fetchall()
        
        url_base = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/{os.getenv('SUPABASE_BUCKET')}"
        for producto in resultado:
            if producto.get('imagen_url'):
                producto['imagen_url'] = f"{url_base}/{producto['imagen_url']}"
        return resultado
    except Exception as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def crear_producto(data, archivo_imagen):
    conn = None
    cursor = None
    try:
        if not data:
            raise ValueError("Ingrese todos los datos")

        campos_obligatorios = ["nombre", "descripcion", "precio", "categoria"]
        for campo in campos_obligatorios:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")

        if archivo_imagen and not archivo_permitido(archivo_imagen.filename):
            raise ValueError("Formato no permitido. Solo podés subir jpg, png, jpeg o webp")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        lactosa     = 1 if data.get("lactosa")     else 0
        vegetariano = 1 if data.get("vegetariano") else 0
        vegano      = 1 if data.get("vegano")      else 0
        sin_tacc    = 1 if data.get("sin_tacc")    else 0

        nombre_imagen_supabase = None
        if archivo_imagen:
            nombre_imagen_supabase = subir_imagen(archivo_imagen)
            if not nombre_imagen_supabase:
                raise Exception("Error al subir la imagen a Supabase")

        query = """
            INSERT INTO productos 
            (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc, imagen_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (data["nombre"], data["descripcion"], data["precio"], data["categoria"], lactosa, vegetariano, vegano, sin_tacc, nombre_imagen_supabase)
        
        cursor.execute(query, valores)
        conn.commit()

        id_nuevo = cursor.lastrowid
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_nuevo,))
        return cursor.fetchone()
    except ValueError as ve:
        raise ValueError(str(ve)) # Errores de validación (400)
    except Exception as e:
        raise Exception(f"Error al agregar el producto: {str(e)}") # Errores de BD (500)
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def actualizar_producto(id_producto, data, archivo_imagen):
    conn = None
    cursor = None
    try:
        if not data:
            raise ValueError("Ingrese todos los datos")

        campos_obligatorios = ["nombre", "descripcion", "precio", "categoria", "lactosa", "vegetariano", "vegano", "sin_tacc"]
        for campo in campos_obligatorios:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        if cursor.fetchone() is None:
            raise LookupError("Producto no encontrado") # Provoca un 404

        lactosa     = 1 if data.get('lactosa') == 'True' else 0
        vegetariano = 1 if data.get('vegetariano') == 'True' else 0
        vegano      = 1 if data.get('vegano') == 'True' else 0
        sin_tacc    = 1 if data.get('sin_tacc') == 'True' else 0
        
        nombre_imagen_supabase = None
        if archivo_imagen and archivo_imagen.filename:
            if not archivo_permitido(archivo_imagen.filename):
                raise ValueError("Formato no permitido. Solo podés subir jpg, png, jpeg o webp")
            nombre_imagen_supabase = subir_imagen(archivo_imagen)
            if not nombre_imagen_supabase:
                raise Exception("Error al subir la imagen.")

        if nombre_imagen_supabase:
            cursor.execute(
                "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, lactosa = %s, vegetariano = %s, vegano = %s, sin_tacc = %s, imagen_url = %s WHERE id_producto = %s",
                (data["nombre"], data["descripcion"], data["precio"], data["categoria"], lactosa, vegetariano, vegano, sin_tacc, nombre_imagen_supabase, id_producto)
            )
        else:
            cursor.execute(
                "UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, lactosa = %s, vegetariano = %s, vegano = %s, sin_tacc = %s WHERE id_producto = %s",
                (data["nombre"], data["descripcion"], data["precio"], data["categoria"], lactosa, vegetariano, vegano, sin_tacc, id_producto)
            )
        conn.commit()

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        return cursor.fetchone()
    except (ValueError, LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar el producto: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def borrar_producto(id_producto):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto_eliminado = cursor.fetchone()

        if producto_eliminado is None:
            raise LookupError("Producto no encontrado")

        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conn.commit()
        return producto_eliminado
    except LookupError as le:
        raise le
    except Exception as e:
        raise Exception(f"Error al eliminar el producto: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()