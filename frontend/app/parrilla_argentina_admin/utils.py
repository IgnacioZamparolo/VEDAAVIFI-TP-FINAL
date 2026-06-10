from functools import wraps
from flask import session, redirect, url_for, flash


def usuario_actual() -> dict:
    return session.get('usuario') or {}


def token_actual() -> str:
    return session.get('token') or ''


def guardar_sesion(token: str, usuario: dict) -> None:
    session['token']   = token
    session['usuario'] = usuario


def limpiar_sesion() -> None:
    session.pop('token', None)
    session.pop('usuario', None)


def extraer_mensajes_error(api_response: dict) -> list[str]:
    response = api_response or {}
    errores = response.get('errors', [])
    if errores:
        return [e.get('description') or e.get('message') or 'Error desconocido' for e in errores]
    error_simple = response.get('error')
    if error_simple:
        return [error_simple]
    return ['Error desconocido']


def requiere_login():
    def decorador(funcion):
        @wraps(funcion)
        def wrapper(*args, **kwargs):
            if not usuario_actual() or not token_actual():
                flash('Iniciá sesión para continuar.', 'error')
                return redirect(url_for('auth.login'))
            return funcion(*args, **kwargs)
        return wrapper
    return decorador