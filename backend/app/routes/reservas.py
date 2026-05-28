from flask import Blueprint, jsonify, request
from db_connection import get_connection
from utils import generar_qr, enviar_qr
from datetime import date, datetime

reservas = Blueprint("reservas", __name__)

CAPACIDAD_MAX = 20

@reservas.route("/reservas", methods = ["GET"]) # admin
def ver_reservas():
    
    try:
        conn = get_connection() 
        cursor = conn.cursor() 
    
        cursor.execute("SELECT * FROM reservas")
        resultado = cursor.fetchall()
          
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener reservas: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()


@reservas.route("/reservas", methods=["POST"]) #cliente
def crear_reserva(): 
    try:
        
        conn = get_connection()
        cursor = conn.cursor()
        data = request.get_json()  
        
        if data is None: 
            return jsonify({"error" :"Ingrese todos los datos, por favor"}), 400
    
        if "mail" not in data or "cant_personas" not in data or "dia" not in data or "horario" not in data: 
            return jsonify({"error" : "Datos no correspondientes"}), 400
        try:
            fecha_reserva = datetime.strptime(data["dia"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Formato de fecha invalido"}), 400
        
        if fecha_reserva < date.today():
            return jsonify({"error": "No se puede reservar para una fecha que ya paso"}), 400
                            
        if data["cant_personas"] <= 0:
            return jsonify({"error": "La cantidad de personas debe ser mayor a 0"}), 400

        if data["cant_personas"] > CAPACIDAD_MAX:
            return jsonify({"error": f"La cantidad de personas no puede superar {CAPACIDAD_MAX}"}), 400

        id_reserva = cursor.lastrowid
    
        cursor.execute(""" INSERT INTO reservas(mail, cant_personas, dia, horario) VALUES (%s, %s, %s)""", (data["mail"], data["cant_personas"], data["dia"], data["horario"]))
        conn.commit()

        id_reserva = cursor.lastrowid 
        
        qr_bytes = generar_qr(id_reserva)
        enviar_qr(data["mail"], qr_bytes)
    
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva_creada = cursor.fetchone()
        return jsonify(reserva_creada), 201
                       
    except Exception as e:
        return jsonify({"error": f"Error al crear la reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@reservas.route("/reservas/<int:id_reserva>", methods=["PUT"]) # admin
def actualizar_reserva(id_reserva):  
    try:             
        conn = get_connection()
        cursor = conn.cursor()
        data = request.get_json() 
            
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        if cursor.fetchone() is None:
             return jsonify({"error": f"No exite reserva con ese id {id_reserva}"}), 404
        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

        for campo in ["cant_personas", "horario", "dia" ,"mesa"]:
            if campo not in data: 
                return jsonify({"error": f"Falta campo requerido  {campo}"}), 400
    
        cursor.execute(""""UPDATE reservas SET cant_personas = %s, horario = %s, dia = %s, mesa = %s WHERE id_reserva = %s"""",
            (data["cant_personas"], data["horario"], data["dia"], data["mesa"], id_reserva))
         
        conn.commit()  
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva_actualizada = cursor.fetchone()
        return jsonify(reserva_actualizada), 200
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
    
       
@reservas.route("/reservas/<int:id_reserva>", methods=["DELETE"]) # admin
def eliminar_reserva(id_reserva):
    try:
        conn = get_connection() 
        cursor = conn.cursor() 
        
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()
        
        if reserva is None:
             return jsonify({"error": f"No exite reserva con ese id {id_reserva}"}), 404
        
        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))  
        conn.commit()

        return jsonify(reserva), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
   
    
