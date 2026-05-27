from flask import Blueprint, jsonify, request
from db_connection import get_connection 

servicios_extra = Blueprint("servicios_extra", __name__)

@servicios_extra.route("/servicios_extra", methods = ["GET"]) # cliente y admin
def ver_servicios():
    conn = get_connection() 
    cursor = conn.cursor(dictionary=True) 

    cursor.execute("SELECT * FROM servicios_extra")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["PUT"]) # admin
def actualizar_servicio(id_servicio):  
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()  

    cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
    servicio = cursor.fetchone()
    if not servicio:
        cursor.close()
        conn.close()
        return jsonify({"error": "Servicio extra no encontrado"}), 404
    
    cursor.execute(""" UPDATE servicios_extra SET nombre = %s, descripcion = %s WHERE id_servicio = %s """, (data["nombre"], data["descripcion"], id_servicio)) 
    conn.commit()  

    cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
    servicio_actualizado = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return jsonify(servicio_actualizado), 200

@servicios_extra.route("/servicios_extra", methods=["POST"]) # admin
def agregar_servicio():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    data = request.get_json()

    cursor.execute(""" INSERT INTO servicios_extra (nombre, descripcion) VALUES (%s, %s) """, (data["nombre"], data["descripcion"]))
    conn.commit()

    id_nuevo = cursor.lastrowid

    cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_nuevo,))
    nuevo_servicio = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify(nuevo_servicio), 201

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["DELETE"]) # admin
def eliminar_servicio(id_servicio):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
    servicio_eliminado = cursor.fetchone()

    if not servicio_eliminado:
        cursor.close()
        conn.close()
        return jsonify({"error": "Servicio extra no encontrado"}), 404

    cursor.execute("DELETE FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify(servicio_eliminado), 200