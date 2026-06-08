import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

combo_detalle_bp = Blueprint('combo_detalle', __name__)

@combo_detalle_bp.route('/combo_detalle/agregar' , methods = ["GET", "POST"]) #admin
@requiere_login()
def agregar():
    usuario = usuario_actual()

    if request.method == 'POST':
        id_producto      = request.form.get('id_producto', '').strip()
        id_combo         = request.form.get('id_combo', '').strip()

        if not id_producto or not id_combo:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('combo_detalle.agregar'))

        datos = {'id_producto': id_producto, 'id_combo':id_combo}
        resultado = api.agregar_combo_detalle(datos, token_actual())
        
        if resultado.get('ok'):
            flash('Combo_detalle agregado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('combo_detalle.agregar'))
        
    return render_template('editarMenuAdmi.html', usuario=usuario)