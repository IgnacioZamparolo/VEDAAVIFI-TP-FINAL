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