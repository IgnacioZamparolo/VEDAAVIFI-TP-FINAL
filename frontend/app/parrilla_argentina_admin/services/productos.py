import logging
import requests
from ..constants import API_BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def obtener_productos_disponibles(token: str) -> list[dict]:
    """Consume el endpoint del backend para obtener todos los productos."""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{API_BASE_URL}/productos',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()

        logger.error(f'Error al obtener productos: HTTP {response.status_code}')
        return []

    except requests.exceptions.ConnectionError:
        logger.error(f'No se pudo conectar con la API en {API_BASE_URL}')
        return []

    except requests.exceptions.Timeout:
        logger.error('Timeout al conectar con la API')
        return []

    except Exception as e:
        logger.error(f'Error inesperado al obtener productos: {e}')
        return []


def obtener_producto_por_id(id_producto: int, token: str) -> dict:
    """Consume el endpoint del backend para obtener un producto por id."""
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(
            f'{API_BASE_URL}/productos/{id_producto}',
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code == 200:
            return response.json()

        return {}

    except Exception as e:
        logger.error(f'Error al obtener producto {id_producto}: {e}')
        return {}


def crear_producto(form_data: dict, archivo, token: str) -> dict:
    """
    Envía los datos del formulario y la imagen al backend via multipart/form-data.
    Retorna el dict del producto creado, o un dict con 'errores' si falla.
    """
    try:
        headers = {'Authorization': f'Bearer {token}'}
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

        if response.status_code == 201:
            return response.json()

        try:
            error_data = response.json()
            return {'errores': [error_data.get('error', f'Error HTTP {response.status_code}')]}
        except Exception:
            return {'errores': [f'Error del servidor: HTTP {response.status_code}']}

    except requests.exceptions.ConnectionError:
        logger.error(f'No se pudo conectar con la API en {API_BASE_URL}')
        return {'errores': ['No se pudo conectar con el servidor. Verificá que la API esté corriendo.']}

    except requests.exceptions.Timeout:
        logger.error('Timeout al enviar producto a la API')
        return {'errores': ['La solicitud tardó demasiado. Intentá nuevamente.']}

    except Exception as e:
        logger.error(f'Error inesperado al crear producto: {e}')
        return {'errores': [f'Error inesperado: {e}']}