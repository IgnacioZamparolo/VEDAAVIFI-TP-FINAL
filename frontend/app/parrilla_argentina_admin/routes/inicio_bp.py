from flask import Blueprint, render_template
from ..services import api
from ..utils import extraer_mensajes_error

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/")
def home():
    return render_template("index.html")

@frontend_bp.route("/menu")

@frontend_bp.route("/menu")
def menu():
    productos = api.obtener_productos_cliente()
    combos = api.obtener_combos_con_productos()
    return render_template("menu.html",
        productos=productos.get('data', []),
        combos=combos.get('data', [])
    )


@frontend_bp.route("/reserva")
def reserva():
    return render_template("reserva.html")