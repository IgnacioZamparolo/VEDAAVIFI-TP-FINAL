from db_connection import get_connection


def ver_combo_detalle():
    conn=None
    cursor=None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        cursor.execute("SELECT * FROM combo_detalle")
        resultado = cursor.fetchall()
    
        return resultado
    except Exception as e:
        raise Exception(f"Error al obtener los detalles de combos: {str(e)}")
    finally:
        if cursor :cursor.close()
        if conn:conn.close()

def agregar_combo_detalle(data):
    conn=None
    cursor=None
    try:

        if not data:
            raise ValueError({"error" : "Ingrese todos los datos"})

        for campo in ["id_combo", "id_producto"]:
            if campo not in data:
                raise ValueError({"error" : f"Falta el campo requerido: {campo}"})
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
     
               
        cursor.execute("SELECT id_combo FROM combos WHERE id_combo = %s", (data["id_combo"],))
        
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise ValueError({"error" : f"No existe un combo con id {data['id_combo']}"})
        
        cursor.execute ("SELECT id_producto FROM productos WHERE id_producto = %s", (data["id_producto"],))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise ValueError({"error" : f"No existe un producto con id {data['id_producto']}"})
                       
        cursor. execute ("SELECT * FROM combo_detalle WHERE id_combo = %s AND id_producto = %s", (data["id_combo"], data["id_producto"]))
        if cursor.fetchone() is not None:
            raise ValueError({"error": "Ese producto ya esta en ese combo"})
        
        cursor.execute(""" INSERT INTO combo_detalle (id_combo, id_producto) VALUES (%s, %s)""", (data["id_combo"], data["id_producto"]))
        conn.commit()
        
        cursor.execute( "SELECT * FROM combo_detalle WHERE id_combo = %s AND id_producto = %s", (data["id_combo"], data["id_producto"]))
        detalle_creado = cursor.fetchone ()
        return detalle_creado
        
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al agregar el detalle del combo: {str(e)}")
                       
    finally:
        if cursor:cursor.close()
        if conn:conn.close()