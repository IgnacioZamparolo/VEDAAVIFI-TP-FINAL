from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import contiene_malas_palabras
from utils import requiere_admin


resenias = Blueprint("resenias", __name__)

@resenias.route("/resenias", methods = ["GET"]) # cliente y admin
def ver_resenias():
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        cursor.execute("SELECT * FROM resenias")
        lista_resenias = cursor.fetchall()
        return jsonify(lista_resenias), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener resenias: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@resenias.route("/resenias", methods=["POST"])  # cliente 
def agregar_resenia():
    conn = None
    cursor = None

    try:
        data = request.get_json(silent=True)
         
        if data is None:
            return jsonify({"errors": [{"description": "El body debe enviarse en formato JSON"}]}), 400
        
        if "descripcion" not in data or "id_reserva" not in data:
            return jsonify({"errors": [{"description": "Faltan campos obligatorios: descripcion e id_reserva"}]}), 400
        
        descripcion = str(data["descripcion"]).strip()

        if not descripcion:
            return jsonify({"errors": [{"description": "La descripcion no puede estar vacía"}]}), 400
        
        try:
            id_reserva = int(data["id_reserva"])
        except (TypeError, ValueError):
            return jsonify({"errors": [{"description": "El id_reserva no es válido"}]}), 400
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_reserva, finalizada FROM reservas WHERE id_reserva = %s", (id_reserva,))

        reserva = cursor.fetchone()

        if reserva is None:
            return jsonify({"errors": [{"description": "La reserva no existe"}]}), 404
        
        if not reserva["finalizada"]:
            return jsonify({"errors": [{"description": "Solo se puede dejar una reseña de una reserva finalizada"}]}), 403
        
        cursor.execute("SELECT id_resenias FROM resenias WHERE id_reserva = %s", (id_reserva,))

        if cursor.fetchone() is not None:
            return jsonify({"errors": [{"description": "Esta reserva ya tiene una reseña"}]}), 409
        
        if contiene_malas_palabras(descripcion):
            return jsonify({"errors": [{"description": "La descripcion contiene palabras no permitidas"}]}), 400
        
        cursor.execute("""INSERT INTO resenias (descripcion, id_reserva) VALUES (%s, %s)""", (descripcion, id_reserva))
        conn.commit()

        id_resenia = cursor.lastrowid 
        cursor.execute("SELECT * FROM resenias WHERE id_resenias = %s", (id_resenia,))
        resenia_creada = cursor.fetchone()
        
        return jsonify(resenia_creada), 201
    
    except Exception as e:
        return jsonify({"errors": [{"description": f"Error al agregar resenia: {str(e)}"}]}), 500
                       
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@resenias.route("/resenias/<int:id_resenias>", methods = ["DELETE"]) # admin 
@requiere_admin
def eliminar_resenias(id_resenias):
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
          
        cursor.execute("SELECT * FROM resenias WHERE id_resenias = %s", (id_resenias,))
        resenia = cursor.fetchone()

        if resenia is None:
            return jsonify({"error": f"No existe una resenia con el id : {id_resenias}"}), 404
    
        cursor.execute("DELETE FROM resenias where id_resenias=%s", (id_resenias,)) 
        conn.commit()

        return jsonify(resenia), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar resenia: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
    
        
