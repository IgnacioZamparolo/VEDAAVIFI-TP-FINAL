from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from ..services import api
from ..utils import token_actual, requiere_login 
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


#ABM RESEÑAS
@frontend_bp.route("/admin/editarReseniasAdmi")
@requiere_login()
def editar_resenias():
    token = token_actual()
    resenias = api.obtener_resenias(token)['data']
    return render_template("editarReseniasAdmi.html", resenias=resenias)

@frontend_bp.route("/admin/eliminarReseniasAdmi", methods=['POST'])
@requiere_login()
def eliminar_resenias():
    token = token_actual()
    resenia = request.form.get('id_resenias')
    api.eliminar_resenia(int(resenia), token)
    return redirect(url_for('frontend.editar_resenias'))



#ABM SERVICIOS EXTRAS

@frontend_bp.route("/admin/editarServiciosAdmi")
@requiere_login()
def editar_SEAdmi():
    token = token_actual()
    servicios = api.obtener_servicio(token)['data']
    return render_template("editarServiciosAdmi.html", servicios=servicios)


@frontend_bp.route("/admin/editarServicio", methods=['POST'])
@requiere_login()
def editar_ServiciosExtras():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion')
    }
    id_servicio = request.form.get('id_servicio')
    api.editar_servicio(int(id_servicio),datos, token)
    return redirect(url_for('frontend.editar_SEAdmi'))

@frontend_bp.route("/admin/agregarServicio", methods=['POST'])
@requiere_login()
def agregar_ServiciosExtras():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion')
    }
    api.agregar_servicio(datos, token)
    return redirect(url_for('frontend.editar_SEAdmi'))

@frontend_bp.route("/admin/eliminarSEAdmi", methods=['POST'])
@requiere_login()
def eliminar_servicio():
    token = token_actual()
    servicio = request.form.get('id')
    api.eliminar_servicio(int(servicio), token)
    return redirect(url_for('frontend.editar_SEAdmi'))



#ABM MENU
@frontend_bp.route("/admin/editarMenuAdmi")
@requiere_login()
def editar_menu():
    token = token_actual()
    productos = api.obtener_productos(token)['data']
    combos = api.obtener_combo(token)['data']
    combos_version = api.obtener_combo_version(token)['data']
    combos_detalle = api.obtener_combo_detalle(token)['data']
    return render_template("editarMenuAdmi.html", productos=productos, combos=combos, combos_version = combos_version, combos_detalle = combos_detalle)

#ABM PRODUCTOS
@frontend_bp.route("/admin/agregarProducto", methods=['POST'])
@requiere_login()
def agregar_producto():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion'),
        'precio': request.form.get('precio'),
        'categoria': request.form.get('categoria'),
        'lactosa': request.form.get('lactosa') == 'on',
        'vegetariano': request.form.get('vegetariano') == 'on',
        'vegano': request.form.get('vegano') == 'on',
        'sin_tacc': request.form.get('sin_tacc') == 'on'
    }
    api.agregar_producto(datos, token)
    return redirect(url_for('frontend.editar_menu'))

@frontend_bp.route("/admin/eliminarProducto", methods=['POST'])
@requiere_login()
def eliminar_producto():
    token = token_actual()
    producto = request.form.get('id')
    api.eliminar_producto(int(producto), token)
    return redirect(url_for('frontend.editar_menu'))


@frontend_bp.route("/admin/editarProducto", methods=['POST'])
@requiere_login()
def editar_producto():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion'),
        'precio': request.form.get('precio'),
        'categoria': request.form.get('categoria'),
        'lactosa': request.form.get('lactosa') == 'on',
        'vegetariano': request.form.get('vegetariano') == 'on',
        'vegano': request.form.get('vegano') == 'on',
        'sin_tacc': request.form.get('sin_tacc') == 'on'
    }
    id_producto = request.form.get('id_producto')
    api.editar_producto(int(id_producto),datos, token)
    return redirect(url_for('frontend.editar_menu'))


#ABM COMBOS
@frontend_bp.route("/admin/agregarCombo", methods=['POST'])
@requiere_login()
def agregar_combo():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'precio': request.form.get('precio')
    }
    api.agregar_combo(datos, token)
    return redirect(url_for('frontend.editar_menu'))

@frontend_bp.route("/admin/eliminarCombo", methods=['POST'])
@requiere_login()
def eliminar_combo():
    token = token_actual()
    combo = request.form.get('id')
    api.eliminar_combo(int(combo), token)
    return redirect(url_for('frontend.editar_menu'))

@frontend_bp.route("/admin/editarCombo", methods=['POST'])
@requiere_login()
def editar_combo():
    token = token_actual()
    datos = {
        'nombre': request.form.get('nombre'),
        'precio': request.form.get('precio')
    }
    id_combo = request.form.get('id_combo')
    api.editar_combo(int(id_combo),datos, token)
    return redirect(url_for('frontend.editar_menu'))


#ABM COMBOS VERSION
@frontend_bp.route("/admin/agregarComboVersion", methods=['POST'])
@requiere_login()
def agregar_combo_version():
    token = token_actual()
    datos = {
        'descripcion': request.form.get('descripcion'),
        'personas': request.form.get('personas'),
        'precio': request.form.get('precio'),
        'id_combo': request.form.get('id_combo')
    }
    api.agregar_combo_version(datos, token)
    return redirect(url_for('frontend.editar_menu'))

@frontend_bp.route("/admin/eliminarComboVersion", methods=['POST'])
@requiere_login()
def eliminar_combo_version():
    token = token_actual()
    combo = request.form.get('id_version')
    api.eliminar_combo_version(int(combo), token)
    return redirect(url_for('frontend.editar_menu'))

@frontend_bp.route("/admin/editarComboVersion", methods=['POST'])
@requiere_login()
def editar_combo_version():
    token = token_actual()
    datos = {
        'descripcion': request.form.get('descripcion'),
        'personas': request.form.get('personas'),
        'precio': request.form.get('precio'),
        'id_combo': request.form.get('id_combo')
    }
    id_combo_version = request.form.get('id_combo_version')
    api.editar_combo_version(int(id_combo_version),datos, token)
    return redirect(url_for('frontend.editar_menu'))

#ABM COMBOS DETALLE
@frontend_bp.route("/admin/editarComboDetalle", methods=['POST'])
@requiere_login()
def agregar_combo_detalle():
    token = token_actual()
    datos = {
        'id_combo': request.form.get('id_combo'),
        'id_producto': request.form.get('id_producto')
    }
    
    api.agregar_combo_detalle(datos, token)
    return redirect(url_for('frontend.editar_menu'))  


@frontend_bp.route("/admin/reportes/estadisticas")
def obtener_estadisticas_reportes():
    try:
        response = requests.get("http://127.0.0.1:5000/reportes/estadisticas")

        if response.status_code != 200:
            return jsonify({"error": "No se pudieron obtener las estadísticas"}), response.status_code

        return jsonify(response.json()), 200

    except Exception as e:
        return jsonify({"error": f"Error al conectar con el backend: {str(e)}"}), 500

