"""
Funciones de utilidad para ejecutar queries en la base de datos
"""
from .db_manager import get_connection


def execute_query(query, params=()):
    """
    Ejecuta una query que modifica datos (INSERT, UPDATE, DELETE)
    Retorna las filas afectadas si hay resultado
    """
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        
        # Intentar obtener resultados si es un SELECT
        try:
            rows = c.fetchall()
        except:
            rows = []
        
        last_id = c.lastrowid
        result = rows if rows else last_id
        c.close()
        return result
    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        raise e
    finally:
        try:
            conn.close()
        except:
            pass


def fetch_all(query, params=()):
    """Ejecuta una query y retorna todos los resultados"""
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute(query, params)
        rows = c.fetchall()
        c.close()
        return rows
    finally:
        conn.close()


def fetch_one(query, params=()):
    """Ejecuta una query y retorna un solo resultado"""
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute(query, params)
        row = c.fetchone()
        c.close()
        return row
    finally:
        conn.close()


def clear_all_data_except_plan_cuentas():
    """Elimina todos los datos operativos y deja intacto el plan de cuentas"""
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys = ON")

        def _count(table):
            c.execute(f"SELECT COUNT(*) FROM {table}")
            return c.fetchone()[0]

        counts_before = {
            "detalle_comprobantes": _count("detalle_comprobantes"),
            "libro_compras": _count("libro_compras"),
            "libro_ventas": _count("libro_ventas"),
            "comprobantes": _count("comprobantes"),
        }

        c.execute("DELETE FROM detalle_comprobantes")
        c.execute("DELETE FROM libro_compras")
        c.execute("DELETE FROM libro_ventas")
        c.execute("DELETE FROM comprobantes")
        conn.commit()

        return counts_before
    except Exception as e:
        try:
            conn.rollback()
        except:
            pass
        raise e
    finally:
        try:
            conn.close()
        except:
            pass
