from flask import Blueprint, jsonify, request
from db_connection import get_connection
from utils import generar_qr, enviar_qr
from datetime import date, datetime, timedelta
from utils import requiere_admin, enviar_mail_resenia

reservas = Blueprint("reservas", __name__)

CAPACIDAD_MAX = 10

@reservas.route("/reservas", methods=["GET"]) # admin
@requiere_admin  
def ver_reservas():
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        
        cursor.execute("SELECT id_reserva, mail, cant_personas, dia, horario, mesa, pendiente, confirmada, cancelada, finalizada, vencida FROM reservas")
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
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        data = request.get_json()  
        
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

        if fecha_reserva == date.today():
            hora_reserva = datetime.strptime(data["horario"], "%H:%M").time()
            if hora_reserva < datetime.now().time():
                return jsonify({"error": "El horario seleccionado ya no está disponible para el día de hoy"}), 400
                    
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
            data["mesa"] = int(data["mesa"]) if data["mesa"] else None
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
        cursor = conn.cursor() 
        
       
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
    conn = None
    cursor = None
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True)

        
        cursor.execute("SELECT id_reserva, mail, cant_personas, dia, horario, mesa, pendiente, confirmada, cancelada, finalizada, vencida FROM reservas WHERE id_reserva = %s", (id_reserva,)) 
        reserva = cursor.fetchone()
        
        if reserva is None:
            return jsonify({"error": f"No existe reserva con ese id {id_reserva}"}), 404 
        
        if reserva["cancelada"]:
            return jsonify({"error": "No se puede confirmar una reserva cancelada"}), 409
        
        if reserva["vencida"]:
            return jsonify({"error": "No se puede confirmar una reserva vencida"}), 409
        
        if reserva["finalizada"]:
            return jsonify({"error": "No se puede confirmar una reserva finalizada"}), 409
        
        if reserva["confirmada"]:
            return jsonify({"error": "La reserva ya fue confirmada"}), 409
        
      
        cursor.execute(""" 
            UPDATE reservas 
            SET pendiente = FALSE, confirmada = TRUE 
            WHERE id_reserva = %s 
        """, (id_reserva,))
        conn.commit()

        qr_enviado = False
        try:
            qr_bytes = generar_qr(id_reserva) 
            qr_enviado = enviar_qr(reserva["mail"], qr_bytes, id_reserva)

            if not qr_enviado:
                print(f"No se pudo enviar el código QR para la reserva {id_reserva}")

        except Exception as mail_error:
            print(f"Error al generar o enviar el de la reserva {id_reserva}: {str(mail_error)}")

        respuesta = {
            "id_reserva": id_reserva,
            "mail": reserva["mail"],
            "cant_personas": reserva["cant_personas"],
            "dia": str(reserva["dia"]),
            "horario": str(reserva["horario"]),
            "mesa": reserva["mesa"],
            "pendiente": False,
            "confirmada": True,
            "qr_enviado": qr_enviado
        }
        return jsonify(respuesta), 200
    
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": f"Error al confirmar reserva: {str(e)}"}), 500 
     
    finally: 
        cursor.close() 
        conn.close()

@reservas.route(
    "/reservas/<int:id_reserva>/finalizar",
    methods=["PATCH"]
)
def finalizar_reserva(id_reserva):
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""SELECT id_reserva, mail, pendiente, confirmada, cancelada, finalizada, vencida FROM reservas WHERE id_reserva = %s""",(id_reserva,))

        reserva = cursor.fetchone()

        if reserva is None:
            return jsonify({"errors": [{"description": "La reserva no existe"}]}), 404

        if reserva["cancelada"]:
            return jsonify({"errors": [{"description": "No se puede finalizar una reserva cancelada"}]}), 409

        if reserva["vencida"]:
            return jsonify({"errors": [{"description": "No se puede finalizar una reserva vencida"}]}), 409

        if reserva["finalizada"]:
            return jsonify({"errors": [{"description": "La reserva ya fue finalizada"}]}), 409

        if not reserva["confirmada"]:
            return jsonify({"errors": [{"description": "La reserva todavía no fue confirmada"}]}), 409

        cursor.execute("""UPDATE reservas SET pendiente = FALSE, confirmada = FALSE, finalizada = TRUE, cancelada = FALSE, vencida = FALSE WHERE id_reserva = %s""", (id_reserva,))

        conn.commit()

        mail_enviado = enviar_mail_resenia(
            reserva["mail"],
            id_reserva
        )

        respuesta = {"mensaje": "Reserva finalizada correctamente", "id_reserva": id_reserva, "mail_resenia_enviado": mail_enviado}

        return jsonify(respuesta), 200

    except Exception as e:
        if conn:
            conn.rollback()

        return jsonify({"errors": [{"description": (f"Error al finalizar la reserva: {str(e)}")}]}), 500

    finally:
        if cursor:
            cursor.close()

        if conn:
            conn.close()

@reservas.route("/reservas/<int:id_reserva>/cancelar", methods=["POST"])  # cliente via mail
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