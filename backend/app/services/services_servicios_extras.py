from db_connection import get_connection 


def ver_servicios():
    conn = None
    cursor = None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM servicios_extra")
        resultado = cursor.fetchall()
        return resultado
    
    except Exception as e:
        raise Exception(f"Error interno del servidor: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def actualizar_servicio(id_servicio, data):  
    conn = None
    cursor = None
    try:

        if not data:
            raise ValueError("Ingrese todos los datos")

        for campo in ["nombre", "descripcion"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio = cursor.fetchone()
        if servicio is None:
            raise LookupError({"error": "Servicio extra no encontrado"})        
        cursor.execute(""" UPDATE servicios_extra SET nombre = %s, descripcion = %s WHERE id_servicio = %s """, (data["nombre"], data["descripcion"], id_servicio)) 
        conn.commit()  

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio_actualizado = cursor.fetchone()
        return servicio_actualizado
    
    except (ValueError,LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar el servicio: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


def agregar_servicio(data):
    conn = None
    cursor = None
    try:
        if not data:
            raise ValueError("Ingrese todos los datos")

        for campo in ["nombre", "descripcion"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(""" INSERT INTO servicios_extra (nombre, descripcion) VALUES (%s, %s) """, (data["nombre"], data["descripcion"]))
        conn.commit()

        id_nuevo = cursor.lastrowid

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_nuevo,))
        nuevo_servicio = cursor.fetchone()
        return nuevo_servicio
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar el servicio: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def eliminar_servicio(id_servicio):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        servicio_eliminado = cursor.fetchone()
        if servicio_eliminado is None:
            raise LookupError({"error": "Servicio extra no encontrado"})
        cursor.execute("DELETE FROM servicios_extra WHERE id_servicio = %s", (id_servicio,))
        conn.commit()
        return servicio_eliminado
    except LookupError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar el servicio: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()