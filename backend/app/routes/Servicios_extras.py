from flask import Blueprint, jsonify, request
from database import get_connection 

servicios_extra = Blueprint("servicios_extra", __name__)

@servicios_extra.route("/servicios_extra", methods = ["GET"]) # cliente y admin
def ver_servicios():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM Servicios_extra")
    resultado = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["PUT"]) # admin
def actualizar_servicio(id_servicio):  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    cursor.execute(""" UPDATE Servicios_extra SET nombre = %s, descripcion = %s WHERE id_servicio = %s """, (data["nombre"], data["descripcion"], id_servicio)) 
    conn.commit()  

    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Servicios extra actualizado correctamente"}), 200

@servicios_extra.route("/servicios_extra", methods=["POST"]) # admin
def agregar_servicio():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()

    cursor.execute(""" INSERT INTO Servicios_extra (nombre, descripcion) VALUES (%s, %s) """, (data["nombre"], data["descripcion"]))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Servicio extra agregado correctamente"}), 201

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["DELETE"]) # admin
def eliminar_servicio(id_servicio):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Servicios_extra WHERE id_servicio = %s", (id_servicio,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Servicio extra eliminado correctamente"}), 200