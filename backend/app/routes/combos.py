from flask import Blueprint 
from utils import requiere_admin
from routes.auth import _ejecutar 
from services.services_combos import (
    ver_combo, actualizar_combos, agregar_combo, eliminar_combo, ver_combos_con_productos
)
combos = Blueprint("combos", __name__)

@combos.route("/combos", methods = ["GET"]) # cliente y admin
def get_combo():
    return _ejecutar(lambda body:ver_combo())
        


@combos.route("/combos/<int:id_combo>", methods=["PUT"]) # admin
@requiere_admin
def put_combos(id_combo):  
    return _ejecutar(lambda body: actualizar_combos(id_combo, body))
 

@combos.route("/combos", methods=["POST"]) # admin
@requiere_admin
def post_combo():
    return _ejecutar(lambda body: agregar_combo(body), status_ok=201)


@combos.route("/combos/<int:id_combo>", methods=["DELETE"]) # admin
@requiere_admin
def delete_combo(id_combo):
    return _ejecutar(lambda body: eliminar_combo(id_combo))

@combos.route("/combos/con_productos", methods=["GET"])
def get_combos_con_productos():
    return _ejecutar(lambda body: ver_combos_con_productos())