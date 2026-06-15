import uuid
import os
import qrcode 
from db_connection import get_connection

def obtener_todas_las_reservas():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reservas ORDER BY fecha DESC")
        return cursor.fetchall()
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

        campos_obligatorios = ["email", "fecha", "hora", "cantidad_personas"]
        for campo in campos_obligatorios:
            if campo not in data or str(data[campo]).strip() == "":
                raise ValueError(f"Falta el campo requerido: {campo}")

        personas = int(data["cantidad_personas"])
        if personas <= 0 or personas > 8:
            raise ValueError("Cantidad de personas no permitida (Máximo 8)")

        token_reserva = str(uuid.uuid4())

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(token_reserva)
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white")

        nombre_imagen = f"qr_{token_reserva}.png"
        
        carpeta_qrs = os.path.join("static", "qrs")
        if not os.path.exists(carpeta_qrs):
            os.makedirs(carpeta_qrs)
            
        ruta_guardado = os.path.join(carpeta_qrs, nombre_imagen)
        img_qr.save(ruta_guardado) 
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO reservas 
            (email, fecha, hora, cantidad_personas, estado, qr_codigo, qr_imagen_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        valores = (data["email"], data["fecha"], data["hora"], personas, "pendiente", token_reserva, nombre_imagen)
        
        cursor.execute(query, valores)
        conn.commit()

        id_nueva = cursor.lastrowid
        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_nueva,))
        reserva_creada = cursor.fetchone()
        
        if reserva_creada and reserva_creada.get('qr_imagen_url'):
            reserva_creada['qr_imagen_url'] = f"/static/qrs/{reserva_creada['qr_imagen_url']}"
        
        return reserva_creada

    except ValueError as ve:
        raise ValueError(str(ve))
    except Exception as e:
        raise Exception(f"Error al registrar la reserva con QR: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def modificar_estado_reserva(id_reserva, estado_nuevo):
    conn = None
    cursor = None
    try:
        estados_validos = ["pendiente", "confirmada", "cancelada", "vencida"]
        if estado_nuevo not in estados_validos:
            raise ValueError("Estado inválido")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        if cursor.fetchone() is None:
            raise LookupError(f"La reserva no existe")

        cursor.execute("UPDATE reservas SET estado = %s WHERE id_reserva = %s", (estado_nuevo, id_reserva))
        conn.commit()

        cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva_actualizada = cursor.fetchone()
        
        if reserva_actualizada and reserva_actualizada.get('qr_imagen_url'):
            reserva_actualizada['qr_imagen_url'] = f"/static/qrs/{reserva_actualizada['qr_imagen_url']}"
            
        return reserva_actualizada
    except (ValueError, LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar estado por ID: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
        
def modificar_estado_reserva_por_qr(token_qr, estado_nuevo):
    conn = None
    cursor = None
    try:
        estados_validos = ["pendiente", "confirmada", "cancelada", "vencida"]
        if estado_nuevo not in estados_validos:
            raise ValueError("Estado inválido")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM reservas WHERE qr_codigo = %s", (token_qr,))
        reserva = cursor.fetchone()
        
        if reserva is None:
            raise LookupError(f"La reserva con el código QR provisto no existe")

        cursor.execute("UPDATE reservas SET estado = %s WHERE qr_codigo = %s", (estado_nuevo, token_qr))
        conn.commit()

        cursor.execute("SELECT * FROM reservas WHERE qr_codigo = %s", (token_qr,))
        reserva_actualizada = cursor.fetchone()
        
        if reserva_actualizada and reserva_actualizada.get('qr_imagen_url'):
            reserva_actualizada['qr_imagen_url'] = f"/static/qrs/{reserva_actualizada['qr_imagen_url']}"
            
        return reserva_actualizada
    except (ValueError, LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar estado por QR: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()