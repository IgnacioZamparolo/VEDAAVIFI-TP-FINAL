import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash

from services.productos import (
    obtener_productos_disponibles,
    obtener_producto_por_id,
    crear_producto,
)
from constants import CATEGORIAS_VALIDAS, MAX_FILE_SIZE_MB
from utils import token_actual, requiere_login

logger = logging.getLogger(__name__)

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos')
@requiere_login()
def index():
    """Página principal con listado de productos."""
    token = token_actual()
    productos = obtener_productos_disponibles(token)
    return render_template('editarMenuAdmi.html', productos=productos)


@productos_bp.route('/productos/nuevo', methods=['GET', 'POST'])
@requiere_login()
def nuevo_producto():
    """Formulario para registrar un nuevo producto."""
    token = token_actual()

    if request.method == 'GET':
        return render_template(
            'nuevo_producto.html',
            categorias=sorted(CATEGORIAS_VALIDAS),
        )

    # --- Procesar el POST ---
    errores = []

    nombre      = request.form.get('nombre', '').strip()
    descripcion = request.form.get('descripcion', '').strip()
    precio      = request.form.get('precio', '').strip()
    categoria   = request.form.get('categoria', '').strip()
    lactosa     = '1' if request.form.get('lactosa') else '0'
    vegetariano = '1' if request.form.get('vegetariano') else '0'
    vegano      = '1' if request.form.get('vegano') else '0'
    sin_tacc    = '1' if request.form.get('sin_tacc') else '0'
    archivo     = request.files.get('imagen')

    # Validaciones
    if not nombre:
        errores.append('El nombre es obligatorio.')
    if not descripcion:
        errores.append('La descripción es obligatoria.')
    if not precio:
        errores.append('El precio es obligatorio.')
    else:
        try:
            if float(precio) < 0:
                errores.append('El precio debe ser mayor o igual a 0.')
        except ValueError:
            errores.append('El precio debe ser un número.')
    if categoria.lower() not in CATEGORIAS_VALIDAS:
        errores.append('La categoría seleccionada no es válida.')
    if not archivo or not archivo.filename:
        errores.append('Debés seleccionar una imagen.')

    if errores:
        return render_template(
            'nuevo_producto.html',
            categorias=sorted(CATEGORIAS_VALIDAS),
            errores=errores,
            form=request.form,
        )

    form_data = {
        'nombre':      nombre,
        'descripcion': descripcion,
        'precio':      precio,
        'categoria':   categoria,
        'lactosa':     lactosa,
        'vegetariano': vegetariano,
        'vegano':      vegano,
        'sin_tacc':    sin_tacc,
    }

    resultado = crear_producto(form_data, archivo, token)

    if 'errores' in resultado:
        return render_template(
            'nuevo_producto.html',
            categorias=sorted(CATEGORIAS_VALIDAS),
            errores=resultado['errores'],
            form=request.form,
        )

    return redirect(url_for('productos.index'))