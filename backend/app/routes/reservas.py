from flask import Blueprint, jsonify, request
from db_connection import get_connection
from utils import generar_qr, enviar_qr
from datetime import date, datetime, timedelta
from utils import requiere_admin

reservas = Blueprint("reservas", __name__)

CAPACIDAD_MAX = 10

@reservas.route("/reservas", methods=["GET"]) # admin
@requiere_admin  
def ver_reservas():
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        
        cursor.execute("SELECT id_reserva, mail, cant_personas, dia, horario, mesa FROM reservas")
        resultados = cursor.fetchall()
        
        lista_reservas = []
        
        for fila in resultados:
            
            if isinstance(fila, (tuple, list)):
                reserva = {
                    "id_reserva": fila[0],
                    "mail": fila[1],
                    "cant_personas": fila[2],
                    "dia": str(fila[3]),     
                    "horario": str(fila[4]), 
                    "mesa": fila[5]
                }
            
            else:
                reserva = {}
                for clave, valor in dict(fila).items():
                    if isinstance(valor, (date, datetime, timedelta)):
                        reserva[clave] = str(valor)
                    else:
                        reserva[clave] = valor
                        
            lista_reservas.append(reserva)
          
        return jsonify(lista_reservas), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener reservas: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()


@reservas.route("/reservas", methods=["POST"])  # cliente
def crear_reserva(): 
    try:
        # 🚨 CONTROL 1: Saber si la petición entró a la función
        print("\n" + "="*50)
        print("[BACKEND] ¡PETICIÓN POST DETECTADA EN /reservas!")
        print("="*50)
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()  
        # 🚨 CONTROL 2: Ver exactamente qué datos llegaron del front
        print(f"[BACKEND] Datos JSON recibidos: {data}")
        print(f"[BACKEND] Tipo de datos recibidos: {type(data)}")
        print("="*50 + "\n")
        if data is None: 
            return jsonify({"error": "Ingrese todos los datos, por favor"}), 400
    
        if "mail" not in data or "cant_personas" not in data or "dia" not in data or "horario" not in data: 
            return jsonify({"error": "Datos no correspondientes"}), 400
        
        
        try:
            data["cant_personas"] = int(data["cant_personas"])
        except (ValueError, TypeError):
            return jsonify({"error": "La cantidad de personas debe ser un número válido"}), 400


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

      
        cursor.execute(
            "INSERT INTO reservas(mail, cant_personas, dia, horario) VALUES (%s, %s, %s, %s)", 
            (data["mail"], data["cant_personas"], data["dia"], data["horario"])
        )
        id_reserva = cursor.lastrowid  
        
        
        conn.commit()

        
        try:
            qr_bytes = generar_qr(id_reserva)
            enviar_qr(data["mail"], qr_bytes, id_reserva)
        except Exception as mail_error:
            
            print(f"Advertencia: No se pudo enviar el correo: {str(mail_error)}")


        cursor.execute("SELECT id_reserva, mail, cant_personas, dia, horario FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva_creada = cursor.fetchone()
        
        
        if reserva_creada:
            
            if isinstance(reserva_creada, tuple):
                respuesta = {
                    "id_reserva": reserva_creada[0],
                    "mail": reserva_creada[1],
                    "cant_personas": reserva_creada[2],
                    "dia": str(reserva_creada[3]), 
                    "horario": str(reserva_creada[4])  
                }
       
            else:
                respuesta = dict(reserva_creada)
                respuesta["dia"] = str(respuesta["dia"])
                respuesta["horario"] = str(respuesta["horario"])
                
            return jsonify(respuesta), 201
            
        return jsonify({"error": "No se pudo recuperar la reserva creada"}), 500
                       
    except Exception as e:
   
        print(f"\n[🚨 BACKEND EXCEPCIÓN CRÍTICA]: {str(e)}\n")
        return jsonify({"error": f"Error al crear la reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@reservas.route("/reservas/<int:id_reserva>", methods=["PUT"]) # admin
def actualizar_reserva(id_reserva):  
    try:             
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)  
        data = request.get_json() 
            
 
        cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_reserva = %s", (id_reserva,))
        existe = cursor.fetchone()
        if existe is None or existe[0] == 0:
             return jsonify({"error": f"No existe reserva con ese id {id_reserva}"}), 404
        
        if data is None:
            return jsonify({"error": "Ingrese todos los datos"}), 400

   
        for campo in ["cant_personas", "horario", "dia" , "mesa"]:
            if campo not in data: 
                return jsonify({"error": f"Falta campo requerido {campo}"}), 400
                

        try:
            data["cant_personas"] = int(data["cant_personas"])
            data["mesa"] = int(data["mesa"])
        except (ValueError, TypeError):
            return jsonify({"error": "Los campos 'cant_personas' y 'mesa' deben ser números válidos"}), 400
    
    
        cursor.execute(
            "UPDATE reservas SET cant_personas = %s, horario = %s, dia = %s, mesa = %s WHERE id_reserva = %s",
            (data["cant_personas"], data["horario"], data["dia"], data["mesa"], id_reserva)
        )
        conn.commit()  
        
      
        cursor.execute("SELECT mail FROM reservas WHERE id_reserva = %s", (id_reserva,))
        fila_mail = cursor.fetchone()
        mail_reserva = fila_mail[0] if isinstance(fila_mail, (tuple, list)) else fila_mail["mail"]
        
      
        respuesta = {
            "id_reserva": id_reserva,
            "mail": mail_reserva,
            "cant_personas": data["cant_personas"],
            "dia": str(data["dia"]),
            "horario": str(data["horario"]),
            "mesa": data["mesa"]
        }
                
        return jsonify(respuesta), 200
    
    except Exception as e:
        return jsonify({"error": f"Error al actualizar reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()
    
       
@reservas.route("/reservas/<int:id_reserva>", methods=["DELETE"]) # admin
@requiere_admin  
def eliminar_reserva(id_reserva):
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
        
       
        cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_reserva = %s", (id_reserva,))
        existe = cursor.fetchone()
        
        if existe is None or existe[0] == 0:
             return jsonify({"error": f"No existe reserva con ese id {id_reserva}"}), 404
        
       
        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))  
        conn.commit()

        
        return jsonify({
            "mensaje": f"Reserva con id {id_reserva} eliminada correctamente",
            "id_reserva": id_reserva
        }), 200

    except Exception as e:
        return jsonify({"error": f"Error al eliminar reserva: {str(e)}"}), 500
                       
    finally:
        cursor.close()
        conn.close()

@reservas.route("/reservas/<int:id_reserva>/confirmar", methods=["PATCH"]) # admin
@requiere_admin  
def confirmar_reserva(id_reserva):
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_reserva = %s", (id_reserva,)) 
        existe = cursor.fetchone()
        
        if existe is None or existe[0] == 0: 
            return jsonify({"error": f"No existe reserva con ese id {id_reserva}"}), 404 
        
      
        cursor.execute(""" 
            UPDATE reservas 
            SET pendiente = FALSE, confirmada = TRUE 
            WHERE id_reserva = %s 
        """, (id_reserva,))
        conn.commit()
        
        cursor.execute("SELECT mail, cant_personas, dia, horario, mesa FROM reservas WHERE id_reserva = %s", (id_reserva,)) 
        fila = cursor.fetchone()
        
        
        if isinstance(fila, (tuple, list)):
            respuesta = {
                "id_reserva": id_reserva,
                "mail": fila[0],
                "cant_personas": fila[1],
                "dia": str(fila[2]),
                "horario": str(fila[3]),
                "mesa": fila[4],
                "pendiente": False,
                "confirmada": True
            }
        else:
            respuesta = {
                "id_reserva": id_reserva,
                "mail": fila["mail"],
                "cant_personas": fila["cant_personas"],
                "dia": str(fila["dia"]),
                "horario": str(fila["horario"]),
                "mesa": fila["mesa"],
                "pendiente": False,
                "confirmada": True
            }
            
        return jsonify(respuesta), 200 
     
    except Exception as e:
        return jsonify({"error": f"Error al confirmar reserva: {str(e)}"}), 500 
     
    finally: 
        cursor.close() 
        conn.close()

@reservas.route("/reservas/<int:id_reserva>/cancelar", methods=["GET"])  # cliente via mail
def cancelar_reserva_link(id_reserva):

    try:

        conn = get_connection()

        cursor = conn.cursor(dictionary=True)




        cursor.execute("SELECT dia, horario, mail FROM reservas WHERE id_reserva = %s", (id_reserva,))

        reserva = cursor.fetchone()



        if reserva is None:

            return jsonify({"error": f"No existe reserva con id {id_reserva}"}), 404



        

        if isinstance(reserva, (tuple, list)):

            fecha_reserva = reserva[0]

            horario_raw = reserva[1] # Esto viene como timedelta desde MariaDB

            mail_cliente = reserva[2]

        else:

            fecha_reserva = reserva["dia"]

            horario_raw = reserva["horario"]

            mail_cliente = reserva["mail"]



        

        

        if isinstance(horario_raw, timedelta):

            hora_time = (datetime.min + horario_raw).time()

        else:

            

            hora_time = datetime.strptime(str(horario_raw), "%H:%M:%S").time() if isinstance(horario_raw, str) else horario_raw



        horario_reserva = datetime.combine(fecha_reserva, hora_time)



        

        if datetime.now() >= horario_reserva - timedelta(hours=1):

            return jsonify({"error": "No se puede cancelar con menos de una hora de anticipación"}), 400



       

        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))

        conn.commit()




        return jsonify({

            "mensaje": "Reserva cancelada correctamente",

            "id_reserva": id_reserva,

            "mail": mail_cliente,

            "dia": str(fecha_reserva),

            "horario": str(horario_raw)

        }), 200



    except Exception as e:

        return jsonify({"error": f"Error al cancelar la reserva: {str(e)}"}), 500



    finally:

        cursor.close()

        conn.close()