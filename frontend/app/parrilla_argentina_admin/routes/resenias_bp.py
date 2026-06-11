import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, token_actual, requiere_login

logger = logging.getLogger(__name__)

resenias_bp = Blueprint('resenias', __name__)

@resenias_bp.route('/resenias/admin', methods = ["GET"]) #admin
@requiere_login()
def mostrar():
    resultado = api.obtener_resenias(token_actual())
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('editarReseniasAdmi.html', resenias=[])
        
    return render_template('editarReseniasAdmi.html', resenias=resultado['data'])

@resenias_bp.route('/resenias/<int:id_resenia>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar(id_resenia):
    resultado = api.eliminar_resenia(id_resenia, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('resenias.mostrar'))

    flash('Reseña eliminada correctamente.', 'success')
    return redirect(url_for('resenias.mostrar'))

@resenias_bp.route('/resenias', methods = ["GET"]) #cliente
def mostrar_cliente():
    resultado = api.obtener_resenias_clientes()
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('index.html', resenias=[])
        
    return render_template('index.html', resenias=resultado['data'])

@resenias_bp.route('/resenias/crear', methods = ["GET", "POST"]) #cliente
def crear():

    if request.method == 'POST':
        id_reserva = request.form.get('id_reserva', type=int)
        descripcion   = request.form.get('descripcion', '').strip()


        if not descripcion:
            flash('Escribi un coentario antes de enviar la reseña.', 'error')
            return redirect(url_for('resenias.crear', id_reserva=id_reserva))
        
        if not id_reserva:
            flash('No se pudo identificar la reserva.', 'error')
            return redirect(url_for('resenias.crear'))

        datos = {'descripcion': descripcion, 'id_reserva': id_reserva}
        resultado = api.crear_resenias(datos)

        if resultado.get('ok'):
            flash('Reseña creada correctamente.', 'success')
            return redirect(url_for('resenias.crear', id_reserva=id_reserva, enviada=1))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('resenias.crear', id_reserva=id_reserva))
    
    id_reserva = request.args.get('id_reserva', type=int)
    enviada = request.args.get('enviada', type=int)
        
    return render_template('resenia.html', id_reserva=id_reserva, enviada=enviada)