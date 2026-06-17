from flask import Blueprint
from utils import requiere_admin
from routes.auth import _ejecutar 
from services.services_combo_version import(
    ver_combo_version, actualizar_combo_version, agregar_combo_version, eliminar_combo_version
)

combo_version = Blueprint("combo_version", __name__)

@combo_version.route("/combo_version", methods = ["GET"]) # admin
@requiere_admin
def get_combo_version():
    return _ejecutar(lambda body:ver_combo_version())
    

@combo_version.route("/combo_version/<int:id_version>", methods=["PUT"]) # admin
@requiere_admin
def put_combos_version(id_version):  
    return _ejecutar(lambda body: actualizar_combo_version(id_version, body))
    

@combo_version.route("/combo_version", methods=["POST"]) # admin
@requiere_admin
def post_combo_version():
    return _ejecutar(lambda body: agregar_combo_version(body), status_ok=201)

@combo_version.route("/combo_version/<int:id_version>", methods=["DELETE"]) # admin
@requiere_admin
def delete_combo_version(id_version):
    return _ejecutar(lambda body: eliminar_combo_version(id_version))