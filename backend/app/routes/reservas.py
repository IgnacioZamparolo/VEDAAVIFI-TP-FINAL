from flask import Blueprint, request
from utils import requiere_admin
from routes.auth import _ejecutar 

from services.services_reservas import (
    obtener_todas_las_reservas,
    crear_nueva_reserva,
    modificar_estado_reserva,
    modificar_estado_reserva_por_qr,
    eliminar_reserva,
    confirmar_reserva,
    finalizar_reserva,
    cancelar_reserva_link
)

reservas = Blueprint("reservas", __name__)
CAPACIDAD_MAX = 10

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

@reservas.route("/reservas/<int:id_reserva>", methods=["DELETE"]) # admin
@requiere_admin  
def endpoint_eliminar_reserva(id_reserva):
    return _ejecutar(lambda: eliminar_reserva(id_reserva))

@reservas.route("/reservas/<int:id_reserva>/confirmar", methods=["PATCH"]) # admin
@requiere_admin  
def endpoint_confirmar_reserva(id_reserva):
    return _ejecutar(lambda: confirmar_reserva(id_reserva))

@reservas.route("/reservas/<int:id_reserva>/finalizar", methods=["PATCH"])
def endpoint_finalizar_reserva(id_reserva):
    return _ejecutar(lambda: finalizar_reserva(id_reserva))

@reservas.route("/reservas/<int:id_reserva>/cancelar", methods=["POST"])  # cliente via mail
def endpoint_cancelar_reserva_link(id_reserva):
    return _ejecutar(lambda: cancelar_reserva_link(id_reserva))