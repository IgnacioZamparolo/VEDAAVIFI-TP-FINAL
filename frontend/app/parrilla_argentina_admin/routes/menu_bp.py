import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/admin/menu', methods = ["GET"])
@requiere_login()
def mostrar():
    productos = api.obtener_productos(token_actual())
    combos = api.obtener_combo(token_actual())
    combos_version = api.obtener_combo_version(token_actual())
    combos_detalle = api.obtener_combo_detalle(token_actual())
    print("COMBO DETALLE:", combos_detalle)

    if not productos.get('ok'):
        for mensaje in extraer_mensajes_error(productos.get('error_response')):
            flash(mensaje, 'error')

    if not combos.get('ok'):
        for mensaje in extraer_mensajes_error(combos.get('error_response')):
            flash(mensaje, 'error')

    if not combos_version.get('ok'):
        for mensaje in extraer_mensajes_error(combos_version.get('error_response')):
            flash(mensaje, 'error')

    if not combos_detalle.get('ok'):
        for mensaje in extraer_mensajes_error(combos_detalle.get('error_response')):
            flash(mensaje, 'error')
    
    return render_template('editarMenuAdmi.html',
        productos=productos.get('data', []),
        combos=combos.get('data', []),
        combos_version=combos_version.get('data', []),
        combos_detalle=combos_detalle.get('data', [])
    )

@menu_bp.route('/menu', methods = ["GET"])
def mostrar_cliente():
    productos = api.obtener_productos_cliente()
    print("PRODUCTOS CLIENTE:", productos)
    combos = api.obtener_combos_cliente()
    if not productos.get('ok'):
        for mensaje in extraer_mensajes_error(productos.get('error_response')):
            flash(mensaje, 'error')

    if not combos.get('ok'):
        for mensaje in extraer_mensajes_error(combos.get('error_response')):
            flash(mensaje, 'error')
    
    return render_template('menu.html',
        productos=productos.get('data', []),
        combos=combos.get('data', []),

    )