from db_connection import get_connection


def ver_combo():
    conn = None
    cursor = None
    try: 
        conn = get_connection() 
        cursor = conn.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM combos")
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        raise Exception(f"Error interno del servidor: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def actualizar_combos(id_combo, data):  
    conn = None
    cursor = None
    try: 
        if not data:
            raise ValueError("Ingrese todos los datos")
        for campo in ["nombre", "precio"]:
            if campo not in data:
                raise ValueError (f"Falta el campo requerido {campo}")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
           
      
        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo = cursor.fetchone()
        if combo is None:
            raise LookupError ("Combo no encontrado")
        
        cursor.execute("UPDATE combos SET nombre = %s, precio = %s WHERE id_combo = %s", (data["nombre"], data["precio"], id_combo)) 
        conn.commit()  

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo_actualizado = cursor.fetchone()
        return combo_actualizado
    except (ValueError, LookupError) as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al actualizar el combo: {str(e)}")
    
    
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
 
def agregar_combo(data):
    conn = None
    cursor = None
    try: 
        if not data:
            raise ("Ingrese todos los datos")

        for campo in ["nombre", "precio"]:
            if campo not in data:
                raise ValueError(f"Falta el campo requerido {campo}")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
                
        cursor.execute("INSERT INTO combos (nombre, precio) VALUES (%s, %s)", (data["nombre"], data["precio"]))
        conn.commit()

        id_nuevo = cursor.lastrowid 

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_nuevo,))
        nuevo_combo = cursor.fetchone()

        return nuevo_combo
    except ValueError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al agregar el combo: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def eliminar_combo(id_combo):
    conn = None
    cursor = None
    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combos WHERE id_combo = %s", (id_combo,))
        combo_eliminado = cursor.fetchone()

        if combo_eliminado is None:
            raise LookupError("Combo no encontrado")

        cursor.execute("DELETE FROM combos WHERE id_combo = %s", (id_combo,))
        conn.commit()

        return combo_eliminado
    except LookupError as e:
        raise e
    except Exception as e:
        raise Exception(f"Error al eliminar el combo: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def ver_combos_con_productos():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM combos")
        combos = cursor.fetchall()

        for combo in combos:
            cursor.execute("""
                SELECT p.nombre, p.descripcion
                FROM combo_detalle cd
                JOIN productos p ON cd.id_producto = p.id_producto
                WHERE cd.id_combo = %s
            """, (combo['id_combo'],))
            combo['productos'] = cursor.fetchall()
            cursor.execute("""
                SELECT descripcion, personas, precio
                FROM combo_version
                WHERE id_combo = %s
                    """, (combo['id_combo'],))
            combo['versiones'] = cursor.fetchall()

        return combos
    except Exception as e:
        raise Exception(f"Error al obtener combos con productos: {str(e)}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()