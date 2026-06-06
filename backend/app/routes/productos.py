from services.storage import subir_imagen
from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import requiere_admin

def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS

productos = Blueprint("productos", __name__)

@productos.route("/productos", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = None
    cursor = None
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM productos")
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        


@productos.route("/productos/<int:id_producto>", methods=["PUT"]) # admin
@requiere_admin
def actualizar_productos(id_producto):  
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()  

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        campos_obligatorios = ["nombre", "descripcion", "precio", "categoria", "lactosa", "vegetariano", "vegano", "sin_tacc"]
        for campo in campos_obligatorios:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto = cursor.fetchone()
        if producto is None:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, lactosa = %s, vegetariano = %s, vegano = %s, sin_tacc = %s WHERE id_producto = %s", (data["nombre"], data["descripcion"], data["precio"], data["categoria"], data["lactosa"], data["vegetariano"], data["vegano"], data["sin_tacc"], id_producto)) 
        conn.commit()  

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto_actualizado = cursor.fetchone()
        return jsonify(producto_actualizado), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el producto: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@productos.route("/productos", methods=["POST"]) # admin
@requiere_admin
def agregar_producto():
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        data = request.form
        archivo_imagen = request.files.get("imagen") 

        if archivo_imagen:
            if not archivo_permitido(archivo_imagen.filename):
                return jsonify({"error": "Formato no permitido. Solo podés subir jpg, png, jpeg o webp"}), 400

        if not data:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        campos_obligatorios = ["nombre", "descripcion", "precio", "categoria", "lactosa", "vegetariano", "vegano", "sin_tacc"]
        for campo in campos_obligatorios:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400

        nombre_imagen_supabase = None
        if archivo_imagen:
            nombre_imagen_supabase = subir_imagen(archivo_imagen)
            if not nombre_imagen_supabase:
                return jsonify({"error": "Error al subir la imagen a Supabase o formato incorrecto"}), 400

        query = """
            INSERT INTO productos 
            (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc, imagen_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            data["nombre"], data["descripcion"], data["precio"], 
            data["categoria"], data["lactosa"], data["vegetariano"], 
            data["vegano"], data["sin_tacc"], nombre_imagen_supabase
        )
        
        cursor.execute(query, valores)
        conn.commit()

        id_nuevo = cursor.lastrowid

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_nuevo,))
        nuevo_producto = cursor.fetchone()
        return jsonify(nuevo_producto), 201
        
    except Exception as e:
        return jsonify({"error": f"Error al agregar el producto: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
   

@productos.route("/productos/<int:id_producto>", methods=["DELETE"]) # admin
@requiere_admin
def eliminar_producto(id_producto):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        producto_eliminado = cursor.fetchone()

        if producto_eliminado is None:
            return jsonify({"error": "Producto no encontrado"}), 404

        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conn.commit()
        return jsonify(producto_eliminado), 200
    
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el producto: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

        