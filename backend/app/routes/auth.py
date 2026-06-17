from flask import Blueprint, jsonify, request
from services.services_auth import login_con_password
 
auth = Blueprint("auth", __name__)
 
 
def _ejecutar(funcion, status_ok=200):
    """Toma el body JSON, invoca la funcion del service y maneja errores. """
    body = request.get_json(silent=True)
 
    try:
        resultado = funcion(body)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]), status
    except LookupError as e:
        return jsonify(e.args[0]), 404
 
    return jsonify(resultado), status_ok
 
 
@auth.route("/login", methods=["POST"])
def post_login():
    return _ejecutar(login_con_password)
 