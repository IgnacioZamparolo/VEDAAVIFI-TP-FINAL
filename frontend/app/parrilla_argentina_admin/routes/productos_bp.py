import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash
 
from ..services import api
from ..utils import extraer_mensajes_error, usuario_actual, token_actual, requiere_login

logger = logging.getLogger(__name__)

productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos/<int:id_producto>/editar', methods = ["GET", "POST"]) #admin
@requiere_login()
def editar(id_producto):
    resultado = api.obtener_productos(token_actual())
    usuario = usuario_actual()

    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    producto = None
    for p in resultado['data']:
        if p.get('id_producto') == id_producto:
            producto = p

    if producto is None:
        flash('Producto no encontrado.', 'error')
        return redirect(url_for('menu.mostrar'))

    if request.method == 'POST':
        nombre           = request.form.get('nombre', '').strip()
        descripcion      = request.form.get('descripcion', '').strip()
        precio           = request.form.get('precio', '').strip()
        categoria        = request.form.get('categoria', '').strip()
        lactosa          = request.form.get('lactosa', '') == 'on'
        vegetariano      = request.form.get('vegetariano', '') == 'on'
        vegano           = request.form.get('vegano', '') == 'on'
        sin_tacc         = request.form.get('sin_tacc', '') == 'on'

        archivo_imagen = request.files.get('imagen')

        if not nombre or not descripcion or not precio or not categoria :
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('menu.mostrar'))

        try:
            datos = {'nombre': nombre, 'descripcion': descripcion, 'precio': float(precio), 'categoria': categoria, 'lactosa': lactosa, 'vegetariano': vegetariano, 'vegano': vegano, 'sin_tacc': sin_tacc}
        except (TypeError, ValueError):
            flash('El precio ingresado no es válido.', 'error')
            return redirect(url_for('menu.mostrar'))

        resultado = api.editar_producto(id_producto, datos, token_actual(), archivo_imagen)

        if resultado.get('ok'):
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))

        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    return render_template('editarMenuAdmi.html', usuario=usuario, producto=producto)

@productos_bp.route('/productos/<int:id_producto>/eliminar', methods = ["POST"]) #admin
@requiere_login()
def eliminar(id_producto):
    resultado = api.eliminar_producto(id_producto, token_actual())
    print("RESULTADO ELIMINAR:", resultado)
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))

    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('menu.mostrar'))

@productos_bp.route('/productos/agregar' , methods = ["GET", "POST"]) #admin
@requiere_login()
def agregar():
    usuario = usuario_actual()

    if request.method == 'POST':
        nombre           = request.form.get('nombre', '').strip()
        descripcion      = request.form.get('descripcion', '').strip()
        precio           = request.form.get('precio', '').strip()
        categoria        = request.form.get('categoria', '').strip()
        lactosa          = request.form.get('lactosa', '') == 'on'
        vegetariano      = request.form.get('vegetariano', '') == 'on'
        vegano           = request.form.get('vegano', '') == 'on'
        sin_tacc         = request.form.get('sin_tacc', '') == 'on'

        archivo_imagen = request.files.get('imagen')

        if not nombre or not descripcion or not precio or not categoria:
            flash('Completá todos los campos.', 'error')
            return redirect(url_for('menu.mostrar'))

        try:
            datos = {'nombre': nombre, 'descripcion': descripcion, 'precio': float(precio), 'categoria': categoria, 'lactosa': lactosa, 'vegetariano': vegetariano, 'vegano': vegano, 'sin_tacc': sin_tacc}
        except (TypeError, ValueError):
            flash('El precio ingresado no es válido.', 'error')
            return redirect(url_for('menu.mostrar'))
        
        resultado = api.agregar_producto(datos, token_actual(), archivo_imagen)
        
        if resultado.get('ok'):
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('menu.mostrar'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return redirect(url_for('menu.mostrar'))
        
    return render_template('editarMenuAdmi.html', usuario=usuario)

@productos_bp.route('/productos', methods = ["GET"]) #cliente
def mostrar_cliente():
    resultado = api.obtener_productos_cliente()
    
    if not resultado.get('ok'):
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')
        return render_template('menu.html', productos=[])
        
    return render_template('menu.html', productos=resultado['data'])