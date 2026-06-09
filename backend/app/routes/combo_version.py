from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import requiere_admin

combo_version = Blueprint("combo_version", __name__)

@combo_version.route("/combo_version", methods = ["GET"]) # admin
@requiere_admin
def ver_combo_version():
    try:
        
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        cursor.execute("SELECT * FROM combo_version")
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener las versiones del combo: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@combo_version.route("/combo_version/<int:id_version>", methods=["PUT"]) # admin
@requiere_admin
def actualizar_combos_version(id_version):  
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        if cursor.fetchone() is None:
            return jsonify({"error": f"No existe una version del combo con el id  {id_version}"}), 404
        
        data = request.get_json() 
        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400
            
        for campo in ["descripcion", "personas", "precio"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400
            
        if data["personas"] <= 0:
             return jsonify({"error": "La cantidad de personas debe ser mayor a 0"}), 400
        
        cursor.execute("UPDATE combo_version SET descripcion = %s, personas = %s, precio = %s WHERE id_version = %s", (data["descripcion"], data["personas"], data["precio"], id_version)) 
        conn.commit()  
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        version_actualizada = cursor.fetchone()
        return jsonify(version_actualizada), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la version del combo: {str(e)}"}), 500
                       
    finally:
         cursor.close()
         conn.close()
    

@combo_version.route("/combo_version", methods=["POST"]) # admin
@requiere_admin
def agregar_combo_version():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400
            
        for campo in ["descripcion", "personas", "precio", "id_combo"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400
            
        cursor.execute("SELECT id_combo FROM combos WHERE id_combo = %s", (data["id_combo"],))

        if cursor.fetchone() is None:
            return jsonify({"error": f"No existe un combo con el id {data['id_combo']}"}), 404
            
        if data["personas"] <= 0:
             return jsonify({"error": "La cantidad de personas debe ser mayor a 0"}), 400
        
        cursor.execute("INSERT INTO combo_version (descripcion, personas, precio, id_combo) VALUES (%s, %s, %s, %s)", (data["descripcion"], data["personas"], data["precio"], data["id_combo"]))
        conn.commit()

        nuevo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (nuevo_id,))
        version_creada = cursor.fetchone()
        return jsonify(version_creada), 201

    except Exception as e:
        return jsonify({"error": f"Error al agregar la version del combo: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@combo_version.route("/combo_version/<int:id_version>", methods=["DELETE"]) # admin
@requiere_admin
def eliminar_combo_version(id_version):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        version = cursor.fetchone()
        if version is None:
            return jsonify({"error": f"No existe una version del combo con el id  {id_version}"}), 404

        cursor.execute("DELETE FROM combo_version WHERE id_version = %s", (id_version,))
        conn.commit()
        return jsonify(version), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar la version del combo: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
    
