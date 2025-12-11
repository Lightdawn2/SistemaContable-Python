"""
Módulo de base de datos
"""
from .db_manager import init_db, get_connection
from .queries import execute_query, fetch_all, fetch_one

__all__ = ['init_db', 'get_connection', 'execute_query', 'fetch_all', 'fetch_one']
