from flask import Blueprint, request
from utils import requiere_admin
from routes.auth import _ejecutar 

from services.services_resenias import (
    obtener_todas_las_resenias,
    crear_nueva_resenia,
    eliminar_resenia_por_id
)

resenias = Blueprint("resenias", __name__)

@resenias.route("/resenias", methods=["GET"])
def ver_resenias():
    return _ejecutar(lambda body:obtener_todas_las_resenias())

@resenias.route("/resenias", methods=["POST"])
def agregar_resenia():
    return _ejecutar(lambda: crear_nueva_resenia(request.get_json(silent=True)))

@resenias.route("/resenias/<int:id_resenias>", methods=["DELETE"])
@requiere_admin
def eliminar_resenias(id_resenias):
    return _ejecutar(lambda: eliminar_resenia_por_id(id_resenias))
        
