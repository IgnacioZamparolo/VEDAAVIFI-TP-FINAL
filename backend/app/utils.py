from db_connection import get_connection
import qrcode
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from apscheduler.schedulers.background import BackgroundScheduler
from malas_palabras import MALAS_PALABRAS
from datetime import datetime

def contiene_malas_palabras(texto):
    texto_lower = texto.lower()
    for palabra in MALAS_PALABRAS:
        if palabra in texto_lower:
            return True
        return False
    
def generar_qr(id_reserva):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(id_reserva)
    qr.make(fit=True)

    img=qr.make_image(fill_color="black", back_color="white")

    buffer =io.BytesIO()
    img.save(buffer, format="PNG")
    qr_bytes = buffer.getvalue()
    return qr_bytes

def enviar_qr(mail, qr_bytes):
    try:
        msg = MIMEMultipart("related")
        msg["Subject"]="Confirmación reserva - Parrilla Argentina"
        msg["From"]="apestana@fi.uba.ar"
        msg["To"]= mail

        msg.attach(MIMEText("<h1>Tu Reserva</h1><h3>Gracias por elegirnos, te esperamos!</h3><img src='cid:qr'>","html"))
        imagen = MIMEImage(qr_bytes, subtype="png")
        imagen.add_header("Content-ID","<qr>")
        msg.attach(imagen)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("apestana@fi.uba.ar", "jcny mame egnq eqsh")
            server.sendmail("apestana@fi.uba.ar", mail, msg.as_string())
        return True
    except Exception as e:
        print(f"Error al enviar mail: {e}")
        return False
    
def enviar_mail_resenia(mail):
    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = "¡Dejanos tu reseña! - Parrilla Argentina"
        msg["From"] = "apestana@fi.uba.ar"
        msg["To"] = mail
        msg.attach(MIMEText("<h1>¡Gracias por visitarnos!</h1><h3>Nos encantaría conocer tu experiencia. Podés enviarnos tu reseña respondiendo este mail.</h3>", "html"))
        
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("apestana@fi.uba.ar", "jcny mame egnq eqsh")
            server.sendmail("apestana@fi.uba.ar", mail, msg.as_string())
        return True
    
    except Exception as e:
        print(f"Error al enviar mail de reseña: {e}")
        return False

def actualizar_estados():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        ahora = datetime.now()

        cursor.execute("""UPDATE reservas SET pendiente = FALSE, vencida = TRUE WHERE pendiente = TRUE AND TIMESTAMP(dia, horario) < %s """, (ahora,))

        cursor.execute("""UPDATE reservas SET confirmada = FALSE, finalizada = TRUE WHERE confirmada = TRUE AND TIMESTAMP(dia, horario) < %s """, (ahora,))

        conn.commit()
    
    except Exception as e:
        print(f"Error al actualizar estados: {e}")
    
    finally:
        cursor.close()
        conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(actualizar_estados, "interval", minutes=1)
scheduler.start()