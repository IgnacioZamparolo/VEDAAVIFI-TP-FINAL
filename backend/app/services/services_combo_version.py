from db_connection import get_connection


def ver_combo_version():
    conn=None
    cursor=None
    try:
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 
    
        cursor.execute("SELECT * FROM combo_version")
        resultado = cursor.fetchall()
        return resultado
        
    except Exception as e:
        raise Exception(f"Error al obtener las versiones del combo: {str(e)}")
                       
    finally:
        if cursor : cursor.close()
        if conn : conn.close()

def actualizar_combo_version(id_version, data):
    conn=None
    cursor=None
    try:
        if not data:
            raise ValueError("Ingrese todos los datos")
            
        for campo in ["descripcion", "personas", "precio"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")
            
        if data["personas"] <= 0:
            raise("La cantidad de personas debe ser mayor a 0")
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        if cursor.fetchone() is None:
            raise ValueError(f"No existe una version del combo con el id  {id_version}")
   
            
        for campo in ["descripcion", "personas", "precio"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")
            
        if data["personas"] <= 0:
            raise("La cantidad de personas debe ser mayor a 0")
        
        cursor.execute("UPDATE combo_version SET descripcion = %s, personas = %s, precio = %s WHERE id_version = %s", (data["descripcion"], data["personas"], data["precio"], id_version)) 
        conn.commit()  
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        version_actualizada = cursor.fetchone()
        return (version_actualizada)
    
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar la version del combo: {str(e)}")
                       
    finally:
        if cursor : cursor.close()
        if conn : conn.close()

def agregar_combo_version(data):
    conn=None
    cursor=None
    try:
        if not data:
            raise("Ingrese todos los datos")
            
        for campo in ["descripcion", "personas", "precio", "id_combo"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")
            

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id_combo FROM combos WHERE id_combo = %s", (data["id_combo"],))


        if cursor.fetchone() is None:
            raise ValueError(f"No existe un combo con el id {data['id_combo']}")
            
        if data["personas"] <= 0:
            raise ValueError("La cantidad de personas debe ser mayor a 0")
        
        cursor.execute("INSERT INTO combo_version (descripcion, personas, precio, id_combo) VALUES (%s, %s, %s, %s)", (data["descripcion"], data["personas"], data["precio"], data["id_combo"]))
        conn.commit()

        nuevo_id = cursor.lastrowid
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (nuevo_id,))
        version_creada = cursor.fetchone()
        return version_creada

    except ValueError as e:
        raise e

    except Exception as e:
        raise Exception(f"Error al agregar la version del combo: {str(e)}")
                       
    finally:
        if cursor : cursor.close()
        if conn : conn.close()

def eliminar_combo_version(id_version):
    conn=None
    cursor=None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM combo_version WHERE id_version = %s", (id_version,))
        version = cursor.fetchone()
        if version is None:
            raise ValueError(f"No existe una version del combo con el id  {id_version}")

        cursor.execute("DELETE FROM combo_version WHERE id_version = %s", (id_version,))
        conn.commit()
        return version

    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al eliminar el combo: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()