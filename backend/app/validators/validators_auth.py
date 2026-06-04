from constants import (
    ERROR_CODE_INVALID_BODY,
)
from utils import (
    construir_error_api,
    validar_string_no_vacio,
    validar_formato_email,
)

def _validar_body_presente(body):
    if body is None:
        raise ValueError(construir_error_api(
            code=ERROR_CODE_INVALID_BODY,
            message="Cuerpo de la solicitud invalido",
            description="El cuerpo debe ser un JSON valido con Content-Type application/json"
        ), 400)
 
def validar_body_login(body: dict):

    _validar_body_presente(body)
 
    errores = []
 
    mail = None
    try:
        mail = validar_formato_email(validar_string_no_vacio(body.get("mail"), "mail"))
    except ValueError as e:
        errores.append(e.args[0]["errors"][0])
 
    contrasenia = None
    try:
        contrasenia = validar_string_no_vacio(body.get("contraseña"), "contraseña")
    except ValueError as e:
        errores.append(e.args[0]["errors"][0])
 
    if errores:
        raise ValueError({"errors": errores}, 400)
 
    return {
        "mail":      mail,
        "contraseña": contrasenia,
    }