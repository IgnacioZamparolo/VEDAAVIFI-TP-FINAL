from flask import Blueprint, jsonify, request
from db_connection import get_connection 
from utils import enviar_mail_resenia, contiene_malas_palabras
from utils import requiere_admin


resenias = Blueprint("resenias", __name__)

@resenias.route("/resenias", methods = ["GET"]) # cliente y admin
def ver_resenias():
    try:
        conn = get_connection() 
        cursor = conn.cursor() 
    
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
    try:
        conn = get_connection()
        cursor = conn.cursor()
        data = request.get_json() 
         
        if data is None or "descripcion" not in data:
            return jsonify({"error": f"Falta el campo requerido: descripcion"}), 400
        
        cursor.execute("SELECT * FROM reservas WHERE mail = %s AND finalizada = TRUE", (data["mail"],))
        if cursor.fetchone() is None:
            return jsonify({"error": "Solo se puede dejar una reseña si tenes una reserva finalizada"}), 403
        
        if contiene_malas_palabras(data["descripcion"]):
            return jsonify({"mensaje": "Tu reseña no pudo ser publicada por contener contenido inadecuado"}), 200
        
        cursor.execute("""INSERT INTO resenias (descripcion) VALUES (%s)""", (data["descripcion"],))
        conn.commit()

        enviar_mail_resenia(data["mail"])

        id_resenia = cursor.lastrowid 
        cursor.execute("SELECT * FROM resenias WHERE id_resenias = %s", (id_resenia,))
        resenia_creada = cursor.fetchone()
        return jsonify(resenia_creada), 201
         
    except Exception as e:
        return jsonify({"error": f"Error al agregar resenia: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@resenias.route("/resenias/<int:id_resenias>", methods = ["DELETE"]) # admin 
@requiere_admin
def eliminar_resenias(id_resenias):
    try:
        conn = get_connection() 
        cursor = conn.cursor() 
          
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
    
        
