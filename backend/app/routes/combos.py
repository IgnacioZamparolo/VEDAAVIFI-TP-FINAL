from flask import Blueprint, jsonify, request
from db_connection import get_connection 

combos = Blueprint("combos", __name__)

@combos.route("/combos", methods = ["GET"]) # cliente y admin
def ver_combo():
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 

    cursor.execute("SELECT * FROM combos")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200


@combos.route("/combos/<int:id_combo>", methods=["PUT"]) # admin
def actualizar_combos(id_combo):  
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()  

    cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
    combo = cursor.fetchone()
    if not combo:
        cursor.close()
        conn.close()
        return jsonify({"error": "Combo no encontrado"}), 404
    
    cursor.execute("UPDATE combos SET nombre = %s, precio = %s WHERE id_combo = %s", (data["nombre"], data["precio"], id_combo)) 
    conn.commit()  

    cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
    combo_actualizado = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return jsonify(combo_actualizado), 200

@combos.route("/combos", methods=["POST"]) # admin
def agregar_combo():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    cursor.execute("INSERT INTO combos (nombre, precio) VALUES (%s, %s)", (data["nombre"], data["precio"]))
    conn.commit()

    id_nuevo = cursor.lastrowid 

    cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_nuevo,))
    nuevo_combo = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(nuevo_combo), 201

@combos.route("/combos/<int:id_combo>", methods=["DELETE"]) # admin
def eliminar_combo(id_combo):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
    combo_eliminado = cursor.fetchone()

    if not combo_eliminado:
        cursor.close()
        conn.close()
        return jsonify({"error": "Combo no encontrado"}), 404

    cursor.execute("DELETE FROM combos WHERE id_combo = %s", (id_combo,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify(combo_eliminado), 200