from flask import Blueprint, render_template, jsonify
import requests

frontend_bp = Blueprint("frontend", __name__)

@frontend_bp.route("/")
def home():
    return render_template("index.html")

@frontend_bp.route("/menu")
def menu():
    return render_template("menu.html")

@frontend_bp.route("/reserva")
def reserva():
    return render_template("reserva.html")

@frontend_bp.route("/admin/reportes")
def reportes():
    return render_template("reportes.html")


@frontend_bp.route("/admin/reportes/estadisticas")
def obtener_estadisticas_reportes():
    try:
        response = requests.get("http://127.0.0.1:5000/reportes/estadisticas")

        if response.status_code != 200:
            return jsonify({"error": "No se pudieron obtener las estadísticas"}), response.status_code

        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({"error": f"Error al conectar con el backend: {str(e)}"}), 500