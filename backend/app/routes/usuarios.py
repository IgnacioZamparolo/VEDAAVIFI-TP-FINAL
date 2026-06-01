from flask import Blueprint, jsonify, request
 
from ..constants import ERROR_CODE_USUARIO_NOT_FOUND
from ..utils import construir_error_api, requiere_admin
from ..services.services_usuarios import buscar_usuario_por_id, construir_usuario_dto
 
usuarios = Blueprint("usuarios", __name__)
 
@usuarios.route("/usuarios/me", methods=["GET"])
@requiere_admin
def get_me():

    payload    = request.usuario_actual
    id_usuario = int(payload["sub"])
    usuario    = buscar_usuario_por_id(id_usuario)
 
    if not usuario:
        return jsonify(construir_error_api(
            code=ERROR_CODE_USUARIO_NOT_FOUND,
            message="Usuario no encontrado",
            description=f"No existe un usuario con id '{id_usuario}'"
        )), 404
 
    return jsonify(construir_usuario_dto(usuario)), 200