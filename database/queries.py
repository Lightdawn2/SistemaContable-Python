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
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    
    # Intentar obtener resultados si es un SELECT
    try:
        rows = c.fetchall()
    except:
        rows = []
    
    last_id = c.lastrowid
    conn.close()
    
    return rows if rows else last_id


def fetch_all(query, params=()):
    """Ejecuta una query y retorna todos los resultados"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows


def fetch_one(query, params=()):
    """Ejecuta una query y retorna un solo resultado"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    row = c.fetchone()
    conn.close()
    return row
