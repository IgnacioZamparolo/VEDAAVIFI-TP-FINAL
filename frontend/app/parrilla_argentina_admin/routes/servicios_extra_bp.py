import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

servicios_bp = Blueprint('servicios', __name__)

@servicios_bp.route('/servicios_extra', methods = ["GET"]) #cliente
def mostrar():
    resultado = api.obtener_servicio_extra_cliente()

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('index.html', servicios=[])

    return render_template('index.html', servicios=resultado['data'])


@servicios_bp.route('/admin/servicios_extra', methods = ["GET"]) #admin
@requiere_login()
def mostrar_admi():
    resultado = api.obtener_servicio(token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('editarServiciosAdmi.html', servicios=[])
    
    return render_template('editarServiciosAdmi.html', servicios=resultado['data'])
    

@servicios_bp.route('/servicios_extra/<int:id_servicio>', methods = ["GET", "POST"]) #admin
@requiere_login()
def editar(id_servicio):
    resultado = api.obtener_servicio(token_actual())
    usuario = usuario_actual()

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('servicios.mostrar_admi'))

    servicio = None
    for s in resultado['data']:
        if s.get('id_servicio') == id_servicio:
            servicio = s

    if servicio is None:
        flash('Servicio no encontrado.', 'error')
        return redirect(url_for('servicios.mostrar_admi'))

    if request.method == 'POST':
        nombre      = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre or not descripcion:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('servicios.editar', id_servicio=id_servicio))

        datos = {'nombre': nombre, 'descripcion': descripcion}
        resultado = api.editar_servicio(id_servicio, datos, token_actual())

        if resultado.get('ok'):
            flash('Servicio actualizado correctamente.', 'success')
            return redirect(url_for('servicios.mostrar_admi'))

        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('servicios.editar', id_servicio=id_servicio))

    return render_template('editarServiciosAdmi.html', usuario=usuario, servicio=servicio)


@servicios_bp.route('/servicios_extra/agregar' , methods = ["GET", "POST"]) #admin
@requiere_login()
def agregar():
    usuario = usuario_actual()

    if request.method == 'POST':
        nombre      = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()

        if not nombre or not descripcion:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('servicios.agregar'))

        datos = {'nombre': nombre, 'descripcion': descripcion}
        resultado = api.agregar_servicio(datos, token_actual())
        
        if resultado.get('ok'):
            flash('Servicio agregado correctamente.', 'success')
            return redirect(url_for('servicios.mostrar_admi'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('servicios.agregar'))
        
    return render_template('editarServiciosAdmi.html', usuario=usuario)


@servicios_bp.route('/servicios_extra/<int:id_servicio>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar_admi(id_servicio):
    resultado = api.eliminar_servicio(id_servicio, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('servicios.mostrar_admi'))

    flash('Servicio eliminado correctamente.', 'success')
    return redirect(url_for('servicios.mostrar_admi'))

