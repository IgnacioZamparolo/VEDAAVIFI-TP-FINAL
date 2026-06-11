from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import requiere_admin


combos = Blueprint("combos", __name__)

@combos.route("/combos", methods = ["GET"]) # cliente y admin
def ver_combo():
    conn = None
    cursor = None
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM combos")
        resultado = cursor.fetchall()
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        


@combos.route("/combos/<int:id_combo>", methods=["PUT"]) # admin
@requiere_admin
def actualizar_combos(id_combo):  
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json() 

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["nombre", "precio"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400 

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo = cursor.fetchone()
        if combo is None:
            return jsonify({"error": "Combo no encontrado"}), 404
        
        cursor.execute("UPDATE combos SET nombre = %s, precio = %s WHERE id_combo = %s", (data["nombre"], data["precio"], id_combo)) 
        conn.commit()  

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo_actualizado = cursor.fetchone()
        return jsonify(combo_actualizado), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar el combo: {str(e)}"}), 500
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
 

@combos.route("/combos", methods=["POST"]) # admin
@requiere_admin
def agregar_combo():
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()

        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["nombre", "precio"]:
            if campo not in data:
                return jsonify({"error": f"Falta el campo requerido {campo}"}), 400

        cursor.execute("INSERT INTO combos (nombre, precio) VALUES (%s, %s)", (data["nombre"], data["precio"]))
        conn.commit()

        id_nuevo = cursor.lastrowid 

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_nuevo,))
        nuevo_combo = cursor.fetchone()

        return jsonify(nuevo_combo), 201
    except Exception as e:
        return jsonify({"error": f"Error al agregar el combo: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


@combos.route("/combos/<int:id_combo>", methods=["DELETE"]) # admin
@requiere_admin
def eliminar_combo(id_combo):
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo_eliminado = cursor.fetchone()

        if combo_eliminado is None:
            return jsonify({"error": "Combo no encontrado"}), 404

        cursor.execute("DELETE FROM combos WHERE id_combo = %s", (id_combo,))
        conn.commit()

        return jsonify(combo_eliminado), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar el combo: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@combos.route("/combos/con_productos", methods=["GET"])
def ver_combos_con_productos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combos")
        combos = cursor.fetchall()

        for combo in combos:
            cursor.execute("""
                SELECT p.nombre, p.descripcion
                FROM combo_detalle cd
                JOIN productos p ON cd.id_producto = p.id_producto
                WHERE cd.id_combo = %s
            """, (combo['id_combo'],))
            combo['productos'] = cursor.fetchall()
            cursor.execute("""
                SELECT descripcion, personas, precio
                FROM combo_version
                WHERE id_combo = %s
                    """, (combo['id_combo'],))
            combo['versiones'] = cursor.fetchall()

        return jsonify(combos), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener combos con productos: {str(e)}"}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()