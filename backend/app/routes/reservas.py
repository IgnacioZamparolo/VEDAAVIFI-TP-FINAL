from flask import Blueprint, request
from utils import requiere_admin
from routes.auth import _ejecutar 

from services.services_reservas import (
    obtener_todas_las_reservas,
    crear_nueva_reserva,
    modificar_estado_reserva,
    modificar_estado_reserva_por_qr
)

reservas = Blueprint("reservas", __name__)

@reservas.route("/reservas", methods=["GET"])
@requiere_admin
def endpoint_ver_reservas():
    return _ejecutar(obtener_todas_las_reservas)

@reservas.route("/reservas", methods=["POST"])
def endpoint_crear_reserva():
    return _ejecutar(lambda: crear_nueva_reserva(request.json))

@reservas.route("/reservas/<int:id_reserva>", methods=["PUT"])
@requiere_admin
def endpoint_actualizar_estado(id_reserva):
    return _ejecutar(lambda: modificar_estado_reserva(
        id_reserva, 
        request.json.get("estado")
    ))

@reservas.route("/reservas/qr/<string:token_qr>", methods=["PUT"])
@requiere_admin
def endpoint_actualizar_estado_qr(token_qr):
    return _ejecutar(lambda: modificar_estado_reserva_por_qr(
        token_qr, 
        request.json.get("estado")
    ))
CAPACIDAD_MAX = 10
       
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
