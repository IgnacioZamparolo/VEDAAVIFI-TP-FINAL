from flask import Blueprint, render_template, request, redirect, url_for, flash

from ..services import api
from ..utils import token_actual, requiere_login, extraer_mensajes_error


reservas_bp = Blueprint("reservas_admin", __name__)


@reservas_bp.route("/reservas")
@requiere_login()
def listar_reservas():
    resultado = api.obtener_reservas(token_actual())

    if not resultado.get("ok"):
        for mensaje in extraer_mensajes_error(
            resultado.get("error_response")
        ):
            flash(mensaje, "error")

        return render_template(
            "reservas_admin.html",
            reservas=[]
        )

    return render_template(
        "reservas_admin.html",
        reservas=resultado["data"]
    )


@reservas_bp.route("/reservas/<int:id_reserva>/editar", methods=["POST"])
@requiere_login()
def editar_reserva(id_reserva):
    try:
        mesa = request.form.get("mesa", "").strip()

        datos = {
            "cant_personas": int(request.form.get("cant_personas")),
            "dia": request.form.get("dia"),
            "horario": request.form.get("horario"),
            "mesa": int(mesa) if mesa else None
        }

    except (TypeError, ValueError):
        flash("Los datos ingresados no son válidos.", "error")
        return redirect(url_for("reservas_admin.listar_reservas"))

    resultado = api.actualizar_reserva(
        id_reserva,
        datos,
        token_actual()
    )

    if resultado.get("ok"):
        flash("Reserva actualizada correctamente.", "success")
    else:
        for mensaje in extraer_mensajes_error(
            resultado.get("error_response")
        ):
            flash(mensaje, "error")

    return redirect(url_for("reservas_admin.listar_reservas"))


@reservas_bp.route("/reservas/<int:id_reserva>/confirmar", methods=["POST"])
@requiere_login()
def confirmar_reserva(id_reserva):
    resultado = api.confirmar_reserva(
        id_reserva,
        token_actual()
    )

    if resultado.get("ok"):
        flash("Reserva confirmada correctamente.", "success")
    else:
        for mensaje in extraer_mensajes_error(
            resultado.get("error_response")
        ):
            flash(mensaje, "error")

    return redirect(url_for("reservas_admin.listar_reservas"))


@reservas_bp.route("/reservas/<int:id_reserva>/eliminar", methods=["POST"])
@requiere_login()
def eliminar_reserva(id_reserva):
    resultado = api.eliminar_reserva(
        id_reserva,
        token_actual()
    )

    if resultado.get("ok"):
        flash("Reserva eliminada correctamente.", "success")
    else:
        for mensaje in extraer_mensajes_error(
            resultado.get("error_response")
        ):
            flash(mensaje, "error")

    return redirect(url_for("reservas_admin.listar_reservas"))