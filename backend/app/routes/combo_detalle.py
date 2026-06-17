from flask import Blueprint
from utils import requiere_admin
from routes.auth import _ejecutar 
from services.services_combo_detalle import (
    ver_combo_detalle, agregar_combo_detalle
)


combo_detalle = Blueprint("combo_detalle", __name__)

@combo_detalle.route("/combo_detalle", methods = ["GET"]) # admin
@requiere_admin
def get_combo_detalle():
    return _ejecutar(lambda body: ver_combo_detalle())
    
        
@combo_detalle.route("/combo_detalle", methods=["POST"]) # admin
@requiere_admin
def post_combo_detalle():
    return _ejecutar(lambda body: agregar_combo_detalle(body), status_ok=201)