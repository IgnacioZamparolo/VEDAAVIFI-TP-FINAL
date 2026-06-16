from flask import Blueprint
from utils import requiere_admin
from routes.auth import _ejecutar 
from services.services_reportes import obtener_reporte_estadisticas

reportes = Blueprint("reportes", __name__)

@reportes.route("/reportes/estadisticas", methods=["GET"])
@requiere_admin
def obtener_estadisticas():
    return _ejecutar(lambda body:obtener_reporte_estadisticas())