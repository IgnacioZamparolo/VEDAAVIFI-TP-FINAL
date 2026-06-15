from db_connection import get_connection 
from utils import contiene_malas_palabras

class ForbiddenError(Exception): pass  
class ConflictError(Exception): pass   

def obtener_todas_las_resenias():
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
        cursor.execute("SELECT * FROM resenias")
        return cursor.fetchall()
    except Exception as e:
        raise Exception(f"Error en la base de datos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def crear_nueva_resenia(data):
    conn = None
    cursor = None
    try:
        if data is None:
            raise ValueError("El body debe enviarse en formato JSON")
        
        if "descripcion" not in data or "id_reserva" not in data:
            raise ValueError("Faltan campos obligatorios: descripcion e id_reserva")
        
        descripcion = str(data["descripcion"]).strip()
        if not descripcion:
            raise ValueError("La descripcion no puede estar vacía")
        
        try:
            id_reserva = int(data["id_reserva"])
        except (TypeError, ValueError):
            raise ValueError("El id_reserva no es válido")
            
        if contiene_malas_palabras(descripcion):
            raise ValueError("La descripcion contiene palabras no permitidas")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_reserva, finalizada FROM reservas WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()

        if reserva is None:
            raise LookupError("La reserva no existe") 
        
        if not reserva["finalizada"]:
            raise ForbiddenError("Solo se puede dejar una reseña de una reserva finalizada") 
        
        cursor.execute("SELECT id_resenias FROM resenias WHERE id_reserva = %s", (id_reserva,))
        if cursor.fetchone() is not None:
            raise ConflictError("Esta reserva ya tiene una reseña") 
    
        cursor.execute("""INSERT INTO resenias (descripcion, id_reserva) VALUES (%s, %s)""", (descripcion, id_reserva))
        conn.commit()

        id_resenia = cursor.lastrowid 
        cursor.execute("SELECT * FROM resenias WHERE id_resenias = %s", (id_resenia,))
        return cursor.fetchone()

    except (ValueError, LookupError, ForbiddenError, ConflictError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al agregar resenia: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def eliminar_resenia_por_id(id_resenias):
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
          
        cursor.execute("SELECT * FROM resenias WHERE id_resenias = %s", (id_resenias,))
        resenia = cursor.fetchone()

        if resenia is None:
            raise LookupError(f"No existe una resenia con el id : {id_resenias}") 
    
        cursor.execute("DELETE FROM resenias where id_resenias=%s", (id_resenias,)) 
        conn.commit()

        return resenia

    except LookupError as le:
        raise le
    except Exception as e:
        raise Exception(f"Error al eliminar resenia: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()