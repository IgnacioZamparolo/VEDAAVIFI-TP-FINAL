from flask import Blueprint, jsonify, request
from db_connection import get_connection 

combo_version = Blueprint("combo_version", __name__)

@combo_version.route("/combo_version", methods = ["GET"]) # admin
def ver_combo_version():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combo_version")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@combo_version.route("/combo_version/<int:id_version>", methods=["PATCH"]) # admin
def actualizar_precio_combo_version(id_version):
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute("UPDATE combo_version SET precio = %s WHERE id_version = %s", (data["precio"], id_version))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo actualizado correctamente"}), 200

@combo_version.route("/combo_version/<int:id_version>", methods=["PUT"]) # admin
def actualizar_combos_version(id_version):  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute("UPDATE combo_version SET descripcion = %s, personas = %s, precio = %s WHERE id_version = %s", (data["descripcion"], data["personas"], data["precio"], id_version)) 
    conn.commit()  

    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Combo actualizado correctamente"}), 200

@combo_version.route("/combo_version", methods=["POST"]) # admin
def agregar_combo_version():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute("INSERT INTO combo_version (descripcion, personas, precio, id_combo) VALUES (%s, %s, %s, %s)", (data["descripcion"], data["personas"], data["precio"], data["id_combo"]))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo agregado correctamente"}), 201

@combo_version.route("/combo_version/<int:id_version>", methods=["DELETE"]) # admin
def eliminar_combo_version(id_version):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM combo_version WHERE id_version = %s", (id_version,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo_version eliminado correctamente"}), 200