import logging
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
 
from ..services import api
from ..utils import guardar_sesion, limpiar_sesion, usuario_actual, token_actual, extraer_mensajes_error, requiere_login
 
logger = logging.getLogger(__name__)
 
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    if usuario_actual():
        return redirect(url_for('auth.dashboard'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if usuario_actual():
        return redirect(url_for('auth.dashboard'))
    
    if request.method == 'POST':
        mail     = request.form.get('mail', '').strip()
        password = request.form.get('password', '')

        if not mail or not password:
            flash('Completá email y contraseña.', 'error')
            return redirect(url_for('auth.login'))
        resultado = api.login(mail, password)
        
        if resultado.get('ok'):
            guardar_sesion(resultado['token'], resultado['usuario'])
            flash(f"¡Bienvenido, {resultado['usuario']['nombre']}!", 'success')
            return redirect(url_for('auth.dashboard'))
        
        for mensaje in extraer_mensajes_error(resultado.get('error_response')):
            flash(mensaje, 'error')

        return redirect(url_for('auth.login'))
 
    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    limpiar_sesion()
    flash('Cerraste sesión.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/dashboard')
@requiere_login()
def dashboard():
    usuario = usuario_actual()
    return render_template('dashboard.html', usuario=usuario)
 