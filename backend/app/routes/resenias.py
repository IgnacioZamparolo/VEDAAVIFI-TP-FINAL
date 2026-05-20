from flask import Blueprint, jsonify, request
from database import get_connection 

resenias = Blueprint("resenias", __name__)

@resenias.route("/resenias", methods = ["GET"]) # cliente y admin
def ver_resenias():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM resenias")
    resenias = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(resenias), 200

@resenias.route("/resenias", methods=["POST"])  # cliente 
def agregar_resenia():
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json() 

    cursor.execute("""INSERT INTO resenias (descripcion) VALUES (%s)""", (data["descripcion"],))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Reseña agregada correctamente"}), 201

@resenias.route("/resenias/<int:id_resenias>", methods = ["DELETE"]) # admin 
def eliminar_resenias(id_resenias):
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("DELETE FROM resenias where id_resenias=%s", (id_resenias,)) 
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Reseña eliminada correctamente"}), 200