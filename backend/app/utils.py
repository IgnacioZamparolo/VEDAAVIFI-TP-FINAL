from db_connection import get_connection
import qrcode
import io
import re
import smtplib
import hashlib
import secrets
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from apscheduler.schedulers.background import BackgroundScheduler
from malas_palabras import MALAS_PALABRAS

import jwt 
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import request, jsonify

from constants import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXP_HORAS,
    ROL_ADMIN,
    ERROR_CODE_TOKEN_FALTANTE,
    ERROR_CODE_TOKEN_INVALIDO,
    ERROR_CODE_TOKEN_EXPIRADO,
    ERROR_CODE_ACCESO_NO_AUTORIZADO,
    ERROR_CODE_INVALID_MIN_VALUE,
    ERROR_CODE_INVALID_MAX_VALUE,
    ERROR_CODE_INVALID_EMAIL,
)

logger = logging.getLogger(__name__)

REGEX_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def contiene_malas_palabras(texto):
    texto_lower = texto.lower()
    for palabra in MALAS_PALABRAS:
        if palabra in texto_lower:
            return True
        return False
    
PASSWORD_RESET_TOKEN_BYTES = 32
LOGIN_CODE_LEN = 6

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


# Errores
def construir_error_api(code: str, message: str, description: str):
    """Construye un payload de error uniforme para toda la API."""
    return {
        "errors": [{
            "code":        code,
            "message":     message,
            "description": description,
        }]
    }

# Validaciones genericas
def validar_entero(valor, nombre: str = "numero"):
    try:
        return int(str(valor))
    except (ValueError, TypeError):
        raise ValueError(construir_error_api(
            code=f"invalid.{nombre}.format",
            message=f"Formato de '{nombre}' invalido",
            description=f"El valor '{valor}' no puede convertirse a un numero entero"
        ))
 
 
def validar_minimo(valor: int, minimo: int, nombre: str):
    if valor < minimo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message="Valor por debajo del minimo permitido",
            description=f"El campo '{nombre}' debe ser mayor o igual a {minimo}. Se recibio: {valor}"
        ))
    return valor
 
 
def validar_string_no_vacio(valor, nombre: str):
    if valor is None or not str(valor).strip():
        raise ValueError(construir_error_api(
            code=f"required.{nombre}",
            message=f"Campo requerido: '{nombre}'",
            description=f"El campo '{nombre}' es obligatorio y no puede estar vacio"
        ))
    return str(valor).strip()
 
 
def validar_largo_string(valor: str, minimo: int, maximo: int, nombre: str):
    if len(valor) < minimo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MIN_VALUE,
            message=f"Longitud minima no alcanzada en '{nombre}'",
            description=f"El campo '{nombre}' debe tener al menos {minimo} caracteres"
        ))
    if len(valor) > maximo:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_MAX_VALUE,
            message=f"Longitud maxima superada en '{nombre}'",
            description=f"El campo '{nombre}' debe tener como maximo {maximo} caracteres"
        ))
    return valor
 
 
def validar_formato_email(email: str):
    if not REGEX_EMAIL.match(email):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_EMAIL,
            message="Formato de 'mail' invalido",
            description=f"El valor '{email}' no es un mail valido"
        ))
    return email.lower()

def hashear_password(password):
    
    hash_string = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hash_string


def verificar_password(password, password_hash):
    
    try:
        return hashear_password(password) == password_hash
    except (ValueError, TypeError):
        return False

def generar_reset_token():
    
    return secrets.token_urlsafe(PASSWORD_RESET_TOKEN_BYTES)

def generar_codigo_login():

    maximo = 10 ** LOGIN_CODE_LEN
    numero = secrets.randbelow(maximo)

    return str(numero).zfill(LOGIN_CODE_LEN)

def hashear_token(valor):

    return hashlib.sha256(valor.encode('utf-8')).hexdigest()


# JWT
def generar_jwt(id_usuario: int, mail: str):
    ahora = datetime.now(timezone.utc)
    payload = {
        "sub":  str(id_usuario),
        "mail": mail,
        "rol":  ROL_ADMIN,
        "iat":  ahora,
        "exp":  ahora + timedelta(hours=JWT_EXP_HORAS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
 
 
def decodificar_jwt(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_TOKEN_EXPIRADO,
            message="Token expirado",
            description="El token de autenticacion expiro. Vuelva a iniciar sesion."
        ), 401)
    except jwt.InvalidTokenError:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_TOKEN_INVALIDO,
            message="Token invalido",
            description="El token de autenticacion no es valido."
        ), 401)
 
 
def extraer_jwt_del_header():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_TOKEN_FALTANTE,
            message="Token de autenticacion faltante",
            description='Debe enviarse el header Authorization con el formato "Bearer <token>"'
        ), 401)
    return header[len("Bearer "):].strip()
 
 
def requiere_admin(funcion):
    """
    Decorador que valida el JWT del header Authorization,
    verifica que el rol sea 'admin' e inyecta el payload
    en request.usuario_actual.
    """
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        try:
            token   = extraer_jwt_del_header()
            payload = decodificar_jwt(token)
        except ValueError as e:
            status = e.args[1] if len(e.args) > 1 else 401
            return jsonify(e.args[0]), status
 
        if payload.get("rol") != ROL_ADMIN:
            return jsonify(construir_error_api(
                code=ERROR_CODE_ACCESO_NO_AUTORIZADO,
                message="Acceso no autorizado",
                description="Solo los administradores pueden acceder a este recurso."
            )), 403
 
        request.usuario_actual = payload
        return funcion(*args, **kwargs)
 
    return wrapper

