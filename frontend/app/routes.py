from flask import Blueprint, render_template

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
