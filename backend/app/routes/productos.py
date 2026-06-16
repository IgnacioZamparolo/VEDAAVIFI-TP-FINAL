from flask import Blueprint, request
from utils import requiere_admin
from routes.auth import _ejecutar 

from services.services_productos import (
    obtener_todos_los_productos,
    crear_producto,
    actualizar_producto,
    borrar_producto
)

productos = Blueprint("productos", __name__)

@productos.route("/productos", methods=["GET"])
def endpoint_ver_productos():
    return _ejecutar(lambda body:obtener_todos_los_productos())

@productos.route("/productos", methods=["POST"])
@requiere_admin
def endpoint_crear_producto():
    return _ejecutar(lambda: crear_producto(
        request.form, 
        request.files.get("imagen")
    ))

@productos.route("/productos/<int:id_producto>", methods=["PUT"])
@requiere_admin
def endpoint_actualizar_producto(id_producto):
    return _ejecutar(lambda: actualizar_producto(
        id_producto, 
        request.form, 
        request.files.get("imagen")
    ))

@productos.route("/productos/<int:id_producto>", methods=["DELETE"])
@requiere_admin
def endpoint_borrar_producto(id_producto):
    return _ejecutar(lambda: borrar_producto(id_producto))