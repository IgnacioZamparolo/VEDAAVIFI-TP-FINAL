from flask import Blueprint, jsonify, request
from database import get_connection 

reservas = Blueprint("reservas", __name__)

@reservas.route("/reservas", methods = ["GET"]) # admin
def ver_reservas():
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("SELECT * FROM Reservas")
    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(resultado), 200

@reservas.route("/reservas", methods=["POST"]) #cliente
def crear_reserva():  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json()  
    
    if data is None: 
        return jsonify({"error" :"Ingrese todos los datos, por favor"}), 400

    if "id_usuario" not in data or "total_personas" not in data or "fecha" not in data or "hora" not in data: 
        return jsonify({"error" : "Datos no correspondientes"}), 400    
    
    cursor.execute(""" INSERT INTO Reservas(id_usuario, total_personas, fecha, hora) VALUES (%s, %s, %s, %s)""", (data["id_usuario"], data["total_personas"], data["fecha"], data["hora"]))
    
    conn.commit()  
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Reserva creada correctamente"}), 201

@reservas.route("/reservas/<int:id_reserva>", methods=["PATCH"]) # admin
def actualizar_reserva(id_reserva):  
    conn = get_connection()
    cursor = conn.cursor()
    data = request.get_json() 

    cursor.execute("""UPDATE Reservas SET mesa = %s WHERE id_reserva = %s """, (data["mesa"], id_reserva)) 
    conn.commit()  

    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Reserva actualizada correctamente"}), 200

@reservas.route("/reservas/<int:id_reserva>", methods=["DELETE"]) # admin
def eliminar_reserva(id_reserva):
    conn = get_connection() 
    cursor = conn.cursor() 

    cursor.execute("DELETE FROM Reservas WHERE id_reserva = %s", (id_reserva,))  
    conn.commit()

    cursor.close()
    conn.close()
    
    return jsonify({"mensaje": "Reserva eliminada correctamente"}), 200 