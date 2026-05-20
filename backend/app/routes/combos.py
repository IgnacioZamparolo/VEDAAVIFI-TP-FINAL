from flask import Blueprint, jsonify, request
from db_connection import get_connection 

combos = Blueprint("combos", __name__)

@combos.route("/combos", methods = ["GET"]) # cliente y admin
def ver_combo():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combos")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@combos.route("/combos/<int:id_combo>", methods=["PATCH"]) # admin
def actualizar_precio_combos(id_combo):
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute("UPDATE combo SET precio = %s WHERE id_combo = %s", (data["precio"], id_combo))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "combo actualizado correctamente"}), 200

@combos.route("/combos/<int:id_combo>", methods=["PUT"]) # admin
def actualizar_combos(id_combo):  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute("UPDATE combo SET nombre = %s, precio = %s WHERE id_combo = %s", (data["nombre"], data["precio"], id_combo)) 
    conn.commit()  

    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Combo actualizado correctamente"}), 200

@combos.route("/combos", methods=["POST"]) # admin
def agregar_combo():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute("INSERT INTO combo (nombre, precio,) VALUES (%s, %s)", (data["nombre"], data["precio"]))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo agregado correctamente"}), 201

@combos.route("/combos/<int:id_combo>", methods=["DELETE"]) # admin
def eliminar_combo(id_combo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM combo WHERE id_combo = %s", (id_combo,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo eliminado correctamente"}), 200