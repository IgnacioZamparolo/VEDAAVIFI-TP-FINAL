from .services_usuarios import buscar_usuario_por_mail, construir_usuario_dto
from ..utils import verificar_password, construir_error_api, generar_jwt
from ..constants import ERROR_CODE_CREDENCIALES
from ..validators.validators_auth import validar_body_login

 
 
def login_con_password(body: dict):
    datos = validar_body_login(body)
 
    usuario = buscar_usuario_por_mail(datos["mail"])

    if not usuario or not verificar_password(datos["contraseña"], usuario["contraseña"]):
        raise ValueError(construir_error_api(
            code=ERROR_CODE_CREDENCIALES,
            message="Credenciales invalidas",
            description="El mail o la contraseña son incorrectos."
        ), 401)
 
    token = generar_jwt(
        id_usuario=usuario["id_usuario"],
        mail=usuario["mail"],
    )
 
    return {
        "token":   token,
        "usuario": construir_usuario_dto(usuario),
    }