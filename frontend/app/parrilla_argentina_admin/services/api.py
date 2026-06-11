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


#ABM RESERVAS
def obtener_reservas(token: str) -> dict:
    response = _get('/reservas', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def actualizar_reservas(id_reserva, datos: dict, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
        
    try:
        response = requests.put(
            f'{API_BASE_URL}/reservas/{id_reserva}',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
            )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def eliminar_reservas(id_reserva, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/reservas/{id_reserva}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def confirmar_reservas(id_reserva, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.patch(
            f'{API_BASE_URL}/reservas/{id_reserva}/confirmar',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

#CLIENTES RESERVAS
def crear_reservas(datos: dict) -> dict:
    response = _post('/reservas', datos)
    if response is None:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def cancelar_reservas(id_reserva: int) -> dict:
    response = _get(f'/reservas/{id_reserva}/cancelar')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def finalizar_reservas(id_reserva: int) -> dict:
    try:
        response = requests.patch(f'{API_BASE_URL}/reservas/{id_reserva}/finalizar', timeout=REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM RESEÑAS 
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

#CLIENTE RESEÑAS
def obtener_resenias_clientes() -> dict:
    response = _get ('/resenias')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def crear_resenias(datos: dict) -> dict:
    response = _post('/resenias', datos)
    if response is None:
            return _error_conexion()
    if response.status_code == 201:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM SERVICIOS EXTRAS
def editar_servicio(id_servicio: int, datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.put(
            f'{API_BASE_URL}/servicios_extra/{id_servicio}',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def eliminar_servicio(id_servicio: int, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/servicios_extra/{id_servicio}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def agregar_servicio(datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(
            f'{API_BASE_URL}/servicios_extra',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True}
    return _respuesta_error(response)

def obtener_servicio(token:str) -> dict:
    response = _get(f'/servicios_extra', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#CLIENTE SERVICIOS EXTRA
def obtener_servicio_extra_cliente() -> dict:
    response = _get ('/servicios_extra')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM PRODUCTOS
def editar_producto(id_producto: int, datos: dict, token:str, archivo=None) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        files = {}
    
        if archivo and archivo.filename:
            files['imagen'] = (archivo.filename, archivo.stream, archivo.content_type)

        response = requests.put(
            f'{API_BASE_URL}/productos/{id_producto}',
            headers=headers,
            data=datos,                                     
            files=files if files else None,                 
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def eliminar_producto(id_producto: int, token: str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/productos/{id_producto}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def agregar_producto(form_data: dict, token: str, archivo=None) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        files = {}
        if archivo and archivo.filename:
            files['imagen'] = (archivo.filename, archivo.stream, archivo.content_type)

        response = requests.post(
            f'{API_BASE_URL}/productos',
            headers=headers,
            data=form_data,          
            files=files if files else None,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def obtener_productos(token:str) -> dict:
    response = _get(f'/productos', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#CLIENTE PRODUCTOS
def obtener_productos_cliente() -> dict:
    response = _get('/productos')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM COMBOS
def editar_combo(id_combo: int, datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.put(
            f'{API_BASE_URL}/combos/{id_combo}',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def agregar_combo(datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(
            f'{API_BASE_URL}/combos',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True}
    return _respuesta_error(response)

def eliminar_combo(id_combo: int, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/combos/{id_combo}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def obtener_combo(token:str) -> dict:
    response = _get(f'/combos', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#CLIENTE COMBOS
def obtener_combos_cliente() -> dict:
    response = _get('/combos')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM COMBOS VERSION
def editar_combo_version(id_version: int, datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.put(
            f'{API_BASE_URL}/combo_version/{id_version}',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def agregar_combo_version(datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(
            f'{API_BASE_URL}/combo_version',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True}
    return _respuesta_error(response)

def eliminar_combo_version(id_version: int, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.delete(
            f'{API_BASE_URL}/combo_version/{id_version}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True}
    return _respuesta_error(response)

def obtener_combo_version(token:str) -> dict:
    response = _get(f'/combo_version', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

#ABM Combo Detalle
def obtener_combo_detalle(token:str) -> dict:
    response = _get(f'/combo_detalle', token=token)
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)

def agregar_combo_detalle(datos: dict, token:str) -> dict:
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.post(
            f'{API_BASE_URL}/combo_detalle',
            headers=headers,
            json=datos,
            timeout=REQUEST_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return _error_conexion()
    if response.status_code == 201:
        return {'ok': True}
    return _respuesta_error(response)

def obtener_combos_con_productos() -> dict:
    response = _get('/combos/con_productos')
    if response is None:
        return _error_conexion()
    if response.status_code == 200:
        return {'ok': True, 'data': response.json()}
    return _respuesta_error(response)
