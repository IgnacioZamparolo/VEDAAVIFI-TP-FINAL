import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

combo_version_bp = Blueprint('combo_version', __name__)


@combo_version_bp.route('/combo_version/<int:id_version>/editar', methods = ["GET", "POST"]) #admin
@requiere_login()
def editar(id_version):
    resultado = api.obtener_combo_version(token_actual())
    usuario = usuario_actual()

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))
    combo_version = None
    for v in resultado['data']:
        if int(v.get('id_version')) == id_version:
            combo_version = v

    if combo_version is None:
        flash('Combo no encontrado.', 'error')
        return redirect(url_for('menu.mostrar'))

    if request.method == 'POST':
        descripcion      = request.form.get('descripcion', '').strip()
        personas         = request.form.get('personas', '').strip()
        precio           = request.form.get('precio', '').strip()
        id_combo         = request.form.get('id_combo', '').strip()


        if not descripcion or not personas or not precio:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('menu.mostrar'))

        try:
            datos = {'descripcion': descripcion, 'personas': int(personas), 'precio': float(precio)}
        except (TypeError, ValueError):
            flash('Personas o precio tienen un formato inválido.', 'error')
            return redirect(url_for('menu.mostrar'))

        resultado = api.editar_combo_version(id_version, datos, token_actual())

        if resultado.get('ok'):
            flash('Combo_version actualizado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))

        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    return render_template('editarMenuAdmi.html', usuario=usuario, combo_version=combo_version)

@combo_version_bp.route('/combo_version/agregar' , methods = ["GET", "POST"]) #admin
@requiere_login()
def agregar():
    usuario = usuario_actual()

    if request.method == 'POST':
        descripcion      = request.form.get('descripcion', '').strip()
        personas         = request.form.get('personas', '').strip()
        precio           = request.form.get('precio', '').strip()
        id_combo    = request.form.get('id_combo', '').strip()

        if not descripcion or not personas or not precio or not id_combo:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('menu.mostrar'))

        try:
            datos = {'descripcion': descripcion, 'personas': int(personas), 'precio': float(precio), 'id_combo': int(id_combo)}
        except (TypeError, ValueError):
            flash('El precio ingresado no es válido.', 'error')
            return redirect(url_for('menu.mostrar'))
        
        resultado = api.agregar_combo_version(datos, token_actual())
        
        if resultado.get('ok'):
            flash('Combo_version agregado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))
        
    return render_template('editarMenuAdmi.html', usuario=usuario)

@combo_version_bp.route('/combo_version/<int:id_version>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar(id_version):
    resultado = api.eliminar_combo_version(id_version, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    flash('Combo_version eliminado correctamente.', 'success')
    return redirect(url_for('menu.mostrar'))
