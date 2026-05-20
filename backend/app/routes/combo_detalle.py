from flask import Blueprint, jsonify, request
from db_connection import get_connection 

combo_detalle = Blueprint("combo_detalle", __name__)

@combo_detalle.route("/combo_detalle", methods = ["GET"]) # admin
def ver_combo_detalle():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM combo_detalle")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@combo_detalle.route("/combo_detalle", methods=["POST"]) # admin
def agregar_combo_detalle():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute(""" INSERT INTO combo_detalle (id_combo, id_producto) VALUES (%s, %s)""", (data["id_combo"], data["id_producto"]))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Combo agregado correctamente"}), 201