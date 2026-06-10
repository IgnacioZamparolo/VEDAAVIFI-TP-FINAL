import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

combos_bp = Blueprint('combos', __name__)

@combos_bp.route('/combos/<int:id_combo>/editar', methods = ["GET", "POST"]) #admin
@requiere_login()
def editar(id_combo):
    resultado = api.obtener_combo(token_actual())
    usuario = usuario_actual()

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    combo = None
    for c in resultado['data']:
        if int(c.get('id_combo')) == id_combo:
            combo = c

    if combo is None:
        flash('Combo no encontrado.', 'error')
        return redirect(url_for('menu.mostrar'))

    if request.method == 'POST':
        nombre           = request.form.get('nombre', '').strip()
        precio           = request.form.get('precio', '').strip()


        if not nombre or not precio:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('combos.editar', id_combo=id_combo))

        try:
            datos = {'nombre': nombre, 'precio': float(precio)}
        except (TypeError, ValueError):
            flash('El precio ingresado no es válido.', 'error')
            return redirect(url_for('combos.editar', id_combo=id_combo))

        resultado = api.editar_combo(id_combo, datos, token_actual())

        if resultado.get('ok'):
            flash('Combo actualizado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))

        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('combos.editar', id_combo=id_combo))

    return render_template('editarMenuAdmi.html', usuario=usuario, combo=combo)

@combos_bp.route('/combos/agregar' , methods = ["GET", "POST"]) #admin
@requiere_login()
def agregar():
    usuario = usuario_actual()

    if request.method == 'POST':
        nombre           = request.form.get('nombre', '').strip()
        precio           = request.form.get('precio', '').strip()

        if not nombre or not precio:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('combos.agregar'))

        try:
            datos = {'nombre': nombre, 'precio': float(precio)}
        except (TypeError, ValueError):
            flash('El precio ingresado no es válido.', 'error')
            return redirect(url_for('combos.agregar'))

        resultado = api.agregar_combo(datos, token_actual())
        
        if resultado.get('ok'):
            flash('Combo agregado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('combos.agregar'))
        
    return render_template('editarMenuAdmi.html', usuario=usuario)

@combos_bp.route('/combos/<int:id_combo>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar(id_combo):
    resultado = api.eliminar_combo(id_combo, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    flash('Combo eliminado correctamente.', 'success')
    return redirect(url_for('menu.mostrar'))

@combos_bp.route('/combos', methods = ["GET"]) #cliente
def mostrar_cliente():
    resultado = api.obtener_combos_cliente()
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('menu.html', combos=[])
        
    return render_template('menu.html', combos=resultado['data'])