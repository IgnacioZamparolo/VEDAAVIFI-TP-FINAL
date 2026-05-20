from flask import Blueprint, jsonify, request
from database import get_connection 

productos = Blueprint("productos", __name__)

@productos.route("/productos", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM productos")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@productos.route("/combos", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combos")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@productos.route("/combo_detalle", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combo_detalle")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@productos.route("/combo_version", methods = ["GET"]) # cliente y admin
def ver_menu():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combo_version")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@productos.route("/productos/<int:id_producto>", methods=["PATCH"]) # admin
def actualizar_precio(id_producto):
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute("UPDATE productos SET precio = %s WHERE id_producto = %s", (data["precio"], id_producto))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Precio actualizado correctamente"}), 200

@productos.route("/productos/<int:id_producto>", methods=["PUT"]) # admin
def actualizar_productos(id_producto):  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute(""" UPDATE productos SET nombre = %s, descripcion = %s, precio = %s, categoria = %s, lactosa = %s, vegetariano = %s, vegano = %s, sin_tacc = %s WHERE id_producto = %s """, (data["nombre"], data["descripcion"], data["precio"], data["categoria"], data["lactosa"], data["vegetariano"], data["vegano"], data["sin_tacc"], id_producto)) 
    conn.commit()  

    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

@productos.route("/productos", methods=["POST"]) # admin
def agregar_producto():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute(""" INSERT INTO productos (nombre, descripcion, precio, categoria, lactosa, vegetariano, vegano, sin_tacc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """, (data["nombre"], data["descripcion"], data["precio"], data["categoria"], data["lactosa"], data["vegetariano"], data["vegano"], data["sin_tacc"]))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Producto agregado correctamente"}), 201

@productos.route("/productos/<int:id_producto>", methods=["DELETE"]) # admin
def eliminar_producto(id_producto):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200