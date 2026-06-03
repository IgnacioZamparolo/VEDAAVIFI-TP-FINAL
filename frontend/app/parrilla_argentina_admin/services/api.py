import logging
import requests
from ..constants import API_BASE_URL, REQUEST_TIMEOUT
 
logger = logging.getLogger(__name__)

def _error_conexion() -> dict:
    return {
        'ok': False,
        'status': 0,
        'error_response': {'errors': [{'description': 'No se pudo conectar con la API. Verificá que esté corriendo.'}]},
    }

def _respuesta_error(response) -> dict:
    try:
        cuerpo = response.json()
    except Exception:
        cuerpo = {'errors': [{'description': f'Error del servidor: HTTP {response.status_code}'}]}
    return {'ok': False, 'status': response.status_code, 'error_response': cuerpo} 

def _post(path: str, body: dict):
    try:
        return requests.post(f'{API_BASE_URL}{path}', json=body, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        logger.error(f'No se pudo conectar con la API en {API_BASE_URL}')
        return None

def _get(path: str, token: str = ''):
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    try:
        return requests.get(f'{API_BASE_URL}{path}', headers=headers, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        logger.error(f'No se pudo conectar con la API en {API_BASE_URL}')
        return None
    
def login(mail: str, password: str) -> dict:
    response = _post('/login', {'mail': mail, 'contraseña': password})
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        data = response.json()
        return {'ok': True, 'token': data['token'], 'usuario': data['usuario']}
    return _respuesta_error(response)

def obtener_reservas(token: str) -> dict:
    response = _get('/reservas', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def obtener_resenias(token: str) -> dict:
    response = _get('/resenias', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)
 
 
def eliminar_resenia(id_resenia: int, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/resenias/{id_resenia}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)
 
def obtener_estadisticas(token: str) -> dict:
    response = _get('/reportes/estadisticas', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)