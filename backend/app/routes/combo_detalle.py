from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import requiere_admin

combo_detalle = Blueprint("combo_detalle", __name__)

@combo_detalle.route("/combo_detalle", methods = ["GET"]) # admin
@requiere_admin
def ver_combo_detalle():
    try:
        
        conn = get_connection() 
        cursor = conn.cursor() 
    
        cursor.execute("SELECT * FROM combo_detalle")
        resultado = cursor.fetchall()
    
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener los detalles de combos: {str(e)}"}), 500
    finally:
        cursor.close()
        conn.close()
        
@combo_detalle.route("/combo_detalle", methods=["POST"]) # admin
@requiere_admin
def agregar_combo_detalle():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["id_combo", "id_producto"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido: {campo}"}), 400
                
        cursor.execute("SELECT id_combo FROM combos WHERE id_combo = %s", (data["id_combo"],))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return jsonify({"error": f"No existe un combo con id {data['id_combo']}"}), 404
        
        cursor.execute ("SELECT id_producto FROM productos WHERE id_producto = %s", (data["id_producto"],))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            return jsonify({"error": f"No existe un producto con id {data['id_producto']}"}), 404
                       
        cursor. execute ("SELECT * FROM combo_detalle WHERE id_combo = %s AND id_producto = %s", (data["id_combo"], data["id_producto"]))
        if cursor.fetchone() is not None:
            return jsonify({"error": "Ese producto ya esta en ese combo"}), 400
        
        cursor.execute(""" INSERT INTO combo_detalle (id_combo, id_producto) VALUES (%s, %s)""", (data["id_combo"], data["id_producto"]))
        conn.commit()
        
        cursor.execute( "SELECT * FROM combo_detalle WHERE id_combo = %s AND id_producto = %s", (data["id_combo"], data["id_producto"]))
        detalle_creado = cursor.fetchone ()
        return jsonify (detalle_creado), 201
        
    except Exception as e:
        return jsonify({"error": f"Error al agregar el detalle del combo: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
