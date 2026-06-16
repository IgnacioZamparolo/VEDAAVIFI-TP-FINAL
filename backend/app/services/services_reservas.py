import os
import uuid
import qrcode
from datetime import datetime, timedelta
from db_connection import get_connection

try:
    from utils import generar_qr, enviar_qr, enviar_mail_resenia
except ImportError:
    def generar_qr(id_reserva): return b""
    def enviar_qr(mail, qr_bytes, id_reserva): return True
    def enviar_mail_resenia(mail, id_reserva): return True

def _serializar_reserva(reserva):
    """Convierte objetos date y timedelta de MySQL a texto para que Flask no falle al enviarlos."""
    if not reserva:
        return reserva
    if "dia" in reserva and reserva["dia"]:
        reserva["dia"] = str(reserva["dia"])
    if "horario" in reserva and reserva["horario"]:
        reserva["horario"] = str(reserva["horario"])
    return reserva

def obtener_todas_las_reservas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservas ORDER BY dia DESC, horario DESC")
        reservas = cursor.fetchall()
        return [_serializar_reserva(r) for r in reservas]
    except Exception as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def crear_nueva_reserva(data):
    conn = None
    cursor = None
    try:
        if not data:
            raise ValueError("Ingrese todos los datos para la reserva")

        mail = data.get("mail") or data.get("email")
        dia = data.get("dia") or data.get("fecha")
        horario = data.get("horario") or data.get("hora")
        cant_personas = data.get("cant_personas") or data.get("cantidad_personas")

        if not mail or not dia or not horario or not cant_personas:
            raise ValueError("Faltan campos requeridos (mail, dia, horario, cant_personas)")

        personas = int(cant_personas)
        if personas <= 0 or personas > 8:
            raise ValueError("Cantidad de personas no permitida (Máximo 8)")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO reservas 
            (mail, dia, horario, cant_personas, pendiente, confirmada, cancelada, finalizada, vencida) 
            VALUES (%s, %s, %s, %s, TRUE, FALSE, FALSE, FALSE, FALSE)
        """
        cursor.execute(query, (mail, dia, horario, personas))
        conn.commit()

        id_nueva = cursor.lastrowid
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(str(id_nueva)) 
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")

        nombre_imagen = f"reserva_{id_nueva}.png"
        carpeta_qrs = os.path.join("static", "qrs")
        if not os.path.exists(carpeta_qrs):
            os.makedirs(carpeta_qrs)
            
        ruta_guardado = os.path.join(carpeta_qrs, nombre_imagen)
        img_qr.save(ruta_guardado)

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_nueva,))
        reserva_creada = cursor.fetchone()
        
        reserva_serializada = _serializar_reserva(reserva_creada)
        if reserva_serializada:
            reserva_serializada['qr_imagen_url'] = f"/static/qrs/{nombre_imagen}"
        
        return reserva_serializada

    except ValueError as ve:
        raise ValueError(str(ve))
    except Exception as e:
        raise Exception(f"Error al registrar la reserva: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def modificar_estado_reserva(id_reserva, estado_nuevo):
    conn = None
    cursor = None
    try:
        estados_validos = ["pendiente", "confirmada", "cancelada", "finalizada", "vencida"]
        if estado_nuevo not in estados_validos:
            raise ValueError("Estado inválido")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        if cursor.fetchone() is None:
            raise LookupError(f"La reserva no existe")

        pendiente = (estado_nuevo == "pendiente")
        confirmada = (estado_nuevo == "confirmada")
        cancelada = (estado_nuevo == "cancelada")
        finalizada = (estado_nuevo == "finalizada")
        vencida = (estado_nuevo == "vencida")

        query = """
            UPDATE reservas 
            SET pendiente = %s, confirmada = %s, cancelada = %s, finalizada = %s, vencida = %s 
            WHERE id_reserva = %s
        """
        cursor.execute(query, (pendiente, confirmada, cancelada, finalizada, vencida, id_reserva))
        conn.commit()

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva_actualizada = cursor.fetchone()
        return _serializar_reserva(reserva_actualizada)
    except (ValueError, LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar estado por ID: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def modificar_estado_reserva_por_qr(token_qr, estado_nuevo):
    try:
        id_reserva = int(token_qr)
        return modificar_estado_reserva(id_reserva, estado_nuevo)
    except ValueError:
        raise LookupError("El código QR escaneado no contiene un ID numérico válido")

def eliminar_reserva(id_reserva):
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor() 
        
        cursor.execute("SELECT COUNT(*) FROM reservas WHERE id_reserva = %s", (id_reserva,))
        existe = cursor.fetchone()
        
        if existe is None or existe[0] == 0:
            raise ValueError(f"No existe reserva con ese id {id_reserva}")
        
        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))  
        conn.commit()

        return {
            "mensaje": f"Reserva con id {id_reserva} eliminada correctamente",
            "id_reserva": id_reserva
        }
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def confirmar_reserva(id_reserva):
    conn = None
    cursor = None
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,)) 
        reserva = cursor.fetchone()
        
        if reserva is None:
            raise ValueError(f"No existe reserva con ese id {id_reserva}")
        if reserva["cancelada"]:
            raise ValueError("No se puede confirmar una reserva cancelada")
        if reserva["vencida"]:
            raise ValueError("No se puede confirmar una reserva vencida")
        if reserva["finalizada"]:
            raise ValueError("No se puede confirmar una reserva finalizada")
        if reserva["confirmada"]:
            raise ValueError("La reserva ya fue confirmada")
        
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
        except Exception as mail_error:
            print(f"Error al generar o enviar el QR de la reserva {id_reserva}: {str(mail_error)}")

        return {
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
    finally: 
        if cursor: cursor.close() 
        if conn: conn.close()

def finalizar_reserva(id_reserva):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()

        if reserva is None:
            raise ValueError("La reserva no existe")
        if reserva["cancelada"]:
            raise ValueError("No se puede finalizar una reserva cancelada")
        if reserva["vencida"]:
            raise ValueError("No se puede finalizar una reserva vencida")
        if reserva["finalizada"]:
            raise ValueError("La reserva ya fue finalizada")
        if not reserva["confirmada"]:
            raise ValueError("La reserva todavía no fue confirmada")

        cursor.execute("""
            UPDATE reservas 
            SET pendiente = FALSE, confirmada = FALSE, finalizada = TRUE, cancelada = FALSE, vencida = FALSE 
            WHERE id_reserva = %s
        """, (id_reserva,))
        conn.commit()

        mail_enviado = enviar_mail_resenia(reserva["mail"], id_reserva)

        return {
            "mensaje": "Reserva finalizada correctamente", 
            "id_reserva": id_reserva, 
            "mail_resenia_enviado": mail_enviado
        }
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def cancelar_reserva_link(id_reserva):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT dia, horario, mail FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()

        if reserva is None:
            raise ValueError(f"No existe reserva con id {id_reserva}")

        fecha_reserva = reserva["dia"]
        horario_raw = reserva["horario"]
        mail_cliente = reserva["mail"]

        if isinstance(horario_raw, timedelta):
            hora_time = (datetime.min + horario_raw).time()
        else:
            hora_time = datetime.strptime(str(horario_raw), "%H:%M:%S").time() if isinstance(horario_raw, str) else horario_raw

        horario_reserva = datetime.combine(fecha_reserva, hora_time)

        if datetime.now() >= horario_reserva - timedelta(hours=1):
            raise ValueError("No se puede cancelar con menos de una hora de anticipación")

        cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        
        return {
            "mensaje": "Reserva cancelada correctamente",
            "id_reserva": id_reserva,
            "mail": mail_cliente,
            "dia": str(fecha_reserva),
            "horario": str(horario_raw)
        }
    finally:
        if cursor: cursor.close()
        if conn: conn.close()