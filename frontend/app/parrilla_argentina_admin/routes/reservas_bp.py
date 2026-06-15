import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods = ["GET", "POST"]) #cliente
def crear():

    if request.method == 'POST':
        mail          = request.form.get('mail', '').strip()
        cant_personas = request.form.get('cant_personas', '').strip()
        horario       = request.form.get('horario', '').strip()
        dia           = request.form.get('dia', '').strip()

        if not mail or not cant_personas or not horario or not dia:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('reservas.crear'))

        try:
            datos = {
                'mail': mail,
                'cant_personas': int(cant_personas),
                'horario': horario,
                'dia': dia
            }
        except (TypeError, ValueError):
            flash('Los datos ingresados no son válidos.', 'error')
            return redirect(url_for('reservas.crear'))

        resultado = api.crear_reservas(datos)

        if resultado.get('ok'):
            flash('Reserva creada correctamente. En el momento que podamos asegurar un lugar para usted le enviaremos un mail.', 'success')
            return redirect(url_for('reservas.crear'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('reservas.crear'))
        
    return render_template('reserva.html')

@reservas_bp.route(
    "/reservas/<int:id_reserva>/finalizar", methods=["GET"])
@requiere_login()
def finalizar_desde_qr(id_reserva):
    resultado = api.finalizar_reservas(id_reserva)

    if resultado.get("ok"):
        mail_enviado = resultado["data"].get("mail_resenia_enviado",False)

        return redirect(url_for("reservas.mostrar_finalizacion", id_reserva=id_reserva, exito=1, mail_enviado=int(mail_enviado)))

    for mensaje in extraer_mensajes_error(resultado.get("error_response")):
        flash(mensaje, "error")

    return redirect(url_for("reservas.mostrar_finalizacion", id_reserva=id_reserva, exito=0))


@reservas_bp.route(
    "/reservas/<int:id_reserva>/finalizada", methods=["GET"])
def mostrar_finalizacion(id_reserva):
    exito = request.args.get("exito") == "1"
    mail_enviado = request.args.get("mail_enviado") == "1"

    return render_template("reserva_finalizada.html", id_reserva=id_reserva, exito=exito, mail_enviado=mail_enviado)


@reservas_bp.route('/reservas/<int:id_reserva>/cancelar', methods = ["GET", "POST"]) #cliente
def cancelar(id_reserva):
    resultado = api.obtener_reservas(token_actual())
    usuario = usuario_actual()

    if not resultado.get('ok'):
            for mensaje in extraer_mensajes_error(resultado.get('error_response')):
                flash(mensaje, 'error')
            return redirect('reserva_cancelada.html', usuario=usuario, mostrar_confirmacion=False, exito=False)

    reserva = None
    for r in resultado['data']:
        if r.get('id_reserva') == id_reserva:
            reserva = r

    if reserva is None:
        return render_template('reserva_cancelada.html', usuario=usuario, mostrar_confirmacion=False, exito=False)

    if request.method == 'POST':
        resultado_cancelar = api.cancelar_reservas(id_reserva)

        if resultado_cancelar.get('ok'):
            return render_template('reserva_cancelada.html', usuario=usuario, id_reserva=id_reserva, mostrar_confirmacion=False, exito=True)
        
        for mensaje in extraer_mensajes_error(resultado_cancelar.get('error_response')):
            flash(mensaje, 'error')

        return render_template('reserva_cancelada.html', usuario=usuario, mostrar_confirmacion=False, exito=False)

    return render_template('reserva_cancelada.html', usuario=usuario, id_reserva=id_reserva, mostrar_confirmacion=True)
        


@reservas_bp.route('/reservas/admin', methods = ["GET"]) #admin
@requiere_login()
def mostrar():
    resultado = api.obtener_reservas(token_actual())
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('reservas_admin.html', reservas=[])
        
    return render_template('reservas_admin.html', reservas=resultado['data'])


@reservas_bp.route('/reservas/<int:id_reserva>/admin', methods = ["GET", "POST"]) #admin
@requiere_login()
def actualizar(id_reserva):
    resultado = api.obtener_reservas(token_actual())
    usuario = usuario_actual()
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('reservas.mostrar'))
    
    reserva = None
    for r in resultado['data']:
        if r.get('id_reserva') == id_reserva:
            reserva = r

    if reserva is None:
        flash('Reserva no encontrada.', 'error')
        return redirect(url_for('reservas.mostrar'))
    
    if request.method == 'POST':
        mesa          = request.form.get('mesa', '').strip()
    
        if not mesa:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('reservas.actualizar', id_reserva=id_reserva))

        try:
            datos = {
                'cant_personas': int(reserva.get('cant_personas')),
                'horario': reserva.get('horario'),
                'dia': reserva.get('dia'),
                'mesa': int(mesa) if mesa else None
            }
        except (TypeError, ValueError):
            flash('Los datos ingresados no son válidos.', 'error')
            return redirect(url_for('reservas.actualizar', id_reserva=id_reserva))

        resultado = api.actualizar_reservas(id_reserva, datos, token_actual())
    
        if resultado.get('ok'):
            flash('Reserva actualizada correctamente.', 'success')
            return redirect(url_for('reservas.mostrar'))
    
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('reservas.actualizar', id_reserva=id_reserva))
    
    return render_template('reservas_admin.html', usuario=usuario, reserva=reserva)


@reservas_bp.route('/reservas/<int:id_reserva>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar(id_reserva):
    resultado = api.eliminar_reservas(id_reserva, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('reservas.mostrar'))

    flash('Reserva eliminada correctamente.', 'success')
    return redirect(url_for('reservas.mostrar'))


@reservas_bp.route('/reservas/<int:id_reserva>/confirmar', methods = ["POST"]) #admin
@requiere_login()
def confirmar(id_reserva):
    resultado = api.confirmar_reservas(id_reserva, token_actual())

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('reservas.mostrar'))

    flash('Reserva confirmada correctamente.', 'success')
    return redirect(url_for('reservas.mostrar'))