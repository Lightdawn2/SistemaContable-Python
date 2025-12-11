"""
Modelo para el Plan de Cuentas
"""
from database.queries import execute_query, fetch_all, fetch_one


class PlanCuentasModel:
    """Maneja las operaciones CRUD del Plan de Cuentas"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las cuentas"""
        query = "SELECT codigo, nombre, elemento, categoria, subcategoria, grupo FROM plan_cuentas ORDER BY codigo"
        return fetch_all(query)
    
    @staticmethod
    def get_by_codigo(codigo):
        """Obtiene una cuenta por su código"""
        query = "SELECT codigo, nombre, elemento, categoria, subcategoria, grupo FROM plan_cuentas WHERE codigo = ?"
        return fetch_one(query, (codigo,))
    
    @staticmethod
    def create(codigo, nombre, elemento, categoria, subcategoria=None, grupo=None):
        """Crea una nueva cuenta"""
        query = """
            INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (codigo, nombre, elemento, categoria, subcategoria, grupo))
    
    @staticmethod
    def update(codigo, nombre, elemento, categoria, subcategoria=None, grupo=None):
        """Actualiza una cuenta existente"""
        query = """
            UPDATE plan_cuentas 
            SET nombre = ?, elemento = ?, categoria = ?, subcategoria = ?, grupo = ? 
            WHERE codigo = ?
        """
        return execute_query(query, (nombre, elemento, categoria, subcategoria, grupo, codigo))
    
    @staticmethod
    def delete(codigo):
        """Elimina una cuenta"""
        query = "DELETE FROM plan_cuentas WHERE codigo = ?"
        return execute_query(query, (codigo,))
    
    @staticmethod
    def get_for_combo():
        """Obtiene cuentas en formato para combobox (codigo - nombre)"""
        query = "SELECT codigo, nombre FROM plan_cuentas ORDER BY codigo"
        cuentas = fetch_all(query)
        return {f"{c[0]} - {c[1]}": c[0] for c in cuentas}
