from db_connection import get_connection
 
 
def construir_usuario_dto(usuario: dict):
    """DTO publico de un usuario (sin contraseña)."""
    return {
        "id_usuario": usuario["id_usuario"],
        "nombre":     usuario["nombre"],
        "mail":       usuario["mail"],
    }
 
 
def buscar_usuario_por_mail(mail: str):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_usuario, nombre, mail, password FROM usuarios WHERE mail = %s",
            (mail,)
        )
        resultado = cursor.fetchone()
        return resultado if resultado else None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
 
 
def buscar_usuario_por_id(id_usuario: int):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id_usuario, nombre, mail FROM usuarios WHERE id_usuario = %s",
            (id_usuario,)
        )
        resultado = cursor.fetchone()
        return resultado if resultado else {}
    finally:
        if cursor: cursor.close()
        if conn:   conn.close()
 
 