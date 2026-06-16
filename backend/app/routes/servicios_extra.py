from flask import Blueprint
from utils import requiere_admin
from routes.auth import _ejecutar 
from services.services_servicios_extras import (
    ver_servicios, actualizar_servicio, agregar_servicio, eliminar_servicio
)

servicios_extra = Blueprint("servicios_extra", __name__)

@servicios_extra.route("/servicios_extra", methods = ["GET"]) # cliente y admin
def get_servicios():
    return _ejecutar (lambda body:ver_servicios())
        

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["PUT"]) # admin
@requiere_admin
def put_servicio(id_servicio):  
    return _ejecutar(lambda body:actualizar_servicio(id_servicio, body))
       

@servicios_extra.route("/servicios_extra", methods=["POST"]) # admin
@requiere_admin
def post_servicio():
    return _ejecutar(lambda body:agregar_servicio(body), status_ok=201)
        

@servicios_extra.route("/servicios_extra/<int:id_servicio>", methods=["DELETE"]) # admin
@requiere_admin
def delete_servicio(id_servicio):
    return _ejecutar(lambda body: eliminar_servicio(id_servicio))


       