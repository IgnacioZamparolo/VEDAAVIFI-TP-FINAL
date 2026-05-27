from flask import Blueprint, jsonify, request
from db_connection import get_connection 

servicios_extra = Blueprint("servicios_extra", __name__)

@servicios_extra.route("/servicios_extra", methods = ["GET"]) # cliente y admin
def ver_servicios():
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM servicios_extra")
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["PUT"]) # admin
def actualizar_servicio(id_servicio):  
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()  

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["nombre", "descripcion"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio = cursor.fetchone()
        if servicio is None:
            return jsonify({"error": "Servicio extra no encontrado"}), 404
        
        cursor.execute(""" UPDATE servicios_extra SET nombre = %s, descripcion = %s WHERE id_servicio = %s """, (data["nombre"], data["descripcion"], id_servicio)) 
        conn.commit()  

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio_actualizado = cursor.fetchone()
        return jsonify(servicio_actualizado), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el servicio: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
       

@servicios_extra.route("/servicios_extra", methods=["POST"]) # admin
def agregar_servicio():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["nombre", "descripcion"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400

        cursor.execute(""" INSERT INTO servicios_extra (nombre, descripcion) VALUES (%s, %s) """, (data["nombre"], data["descripcion"]))
        conn.commit()

        id_nuevo = cursor.lastrowid

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_nuevo,))
        nuevo_servicio = cursor.fetchone()
        return jsonify(nuevo_servicio), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar el servicio: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["DELETE"]) # admin
def eliminar_servicio(id_servicio):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio_eliminado = cursor.fetchone()
        if servicio_eliminado is None:
            return jsonify({"error": "Servicio extra no encontrado"}), 404

        cursor.execute("DELETE FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        conn.commit()
        return jsonify(servicio_eliminado), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el servicio: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


       