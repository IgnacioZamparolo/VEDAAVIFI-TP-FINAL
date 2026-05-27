from db_connection import get_connection
import qrcode
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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

    
    



