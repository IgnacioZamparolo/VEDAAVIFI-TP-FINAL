from flask import Blueprint, jsonify, request
from db_connection import get_connection 

productos = Blueprint("productos", __name__)

@productos.route("/productos", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 

    cursor.execute("SELECT * FROM productos")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200


@productos.route("/productos/<int:id_producto>", methods=["PUT"]) # admin
def actualizar_productos(id_producto):  
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()  

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto = cursor.fetchone()
    if not producto:
        cursor.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404
    
    cursor.execute("UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, lactosa = %s, vegetariano = %s, vegano = %s, sin_tacc = %s WHERE id_producto = %s", (data["nombre"], data["descripcion"], data["precio"], data["categoria"], data["lactosa"], data["vegetariano"], data["vegano"], data["sin_tacc"], id_producto)) 
    conn.commit()  

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto_actualizado = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return jsonify(producto_actualizado), 200

@productos.route("/productos", methods=["POST"]) # admin
def agregar_producto():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    cursor.execute("INSERT INTO productos (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (data["nombre"], data["descripcion"], data["precio"], data["categoria"], data["lactosa"], data["vegetariano"], data["vegano"], data["sin_tacc"]))
    conn.commit()

    id_nuevo = cursor.lastrowid

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_nuevo,))
    nuevo_producto = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(nuevo_producto), 201

@productos.route("/productos/<int:id_producto>", methods=["DELETE"]) # admin
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
    producto_eliminado = cursor.fetchone()

    if not producto_eliminado:
        cursor.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify(producto_eliminado), 200