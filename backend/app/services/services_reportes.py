from db_connection import get_connection

def obtener_reporte_estadisticas():
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM reservas")
        total_reservas = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM productos")
        total_productos = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM resenias")
        total_resenias = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM combos")
        total_combos = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                SUM(pendiente = TRUE),
                SUM(confirmada = TRUE),
                SUM(cancelada = TRUE),
                SUM(finalizada = TRUE),
                SUM(vencida = TRUE)
            FROM reservas
        """)
        estados = cursor.fetchone()

        reservas_por_estado = {
            "pendientes": int(estados[0] or 0),
            "confirmadas": int(estados[1] or 0),
            "canceladas": int(estados[2] or 0),
            "finalizadas": int(estados[3] or 0),
            "vencidas": int(estados[4] or 0)
        }
        
        cursor.execute("""
            SELECT categoria, COUNT(*)
            FROM productos
            GROUP BY categoria
        """)
        productos_por_categoria = [
            {
                "categoria": fila[0],
                "cantidad": fila[1]
            }
            for fila in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT dia, COUNT(*)
            FROM reservas
            GROUP BY dia
            ORDER BY dia
        """)
        reservas_por_dia = [
            {
                "dia": fila[0].isoformat(),
                "cantidad": fila[1]
            }
            for fila in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT horario, COUNT(*)
            FROM reservas
            GROUP BY horario
            ORDER BY COUNT(*) DESC
            LIMIT 1
        """)
        horario = cursor.fetchone()

        horario_mas_reservado = None
        if horario is not None:
            horario_mas_reservado = {
                "horario": str(horario[0]),
                "cantidad": horario[1]
            }

        estadisticas = {
            "total_reservas": total_reservas,
            "total_productos": total_productos,
            "total_resenias": total_resenias,
            "total_combos": total_combos,
            "reservas_por_estado": reservas_por_estado,
            "productos_por_categoria": productos_por_categoria,
            "reservas_por_dia": reservas_por_dia,
            "horario_mas_reservado": horario_mas_reservado
        }

        return estadisticas

    except Exception as e:
        raise Exception(f"Error al obtener estadísticas: {str(e)}")

    finally:
        if cursor is not None: cursor.close()
        if conn is not None: conn.close()