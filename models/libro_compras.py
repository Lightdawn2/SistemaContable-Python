"""
Modelo para el Libro de Compras
"""
from database.queries import execute_query, fetch_all


class LibroComprasModel:
    """Maneja las operaciones del Libro de Compras"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las compras"""
        query = """
            SELECT id, fecha, tipo_documento, numero_documento, rut_proveedor, 
                   razon_social, neto, iva, total 
            FROM libro_compras 
            ORDER BY fecha DESC
        """
        return fetch_all(query)
    
    @staticmethod
    def create(fecha, tipo_documento, numero_documento, rut_proveedor, 
               razon_social, neto, iva, total):
        """Registra una nueva compra"""
        query = """
            INSERT INTO libro_compras 
            (fecha, tipo_documento, numero_documento, rut_proveedor, razon_social, neto, iva, total) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (fecha, tipo_documento, numero_documento, 
                                     rut_proveedor, razon_social, neto, iva, total))
    
    @staticmethod
    def delete(id_compra):
        """Elimina una compra"""
        query = "DELETE FROM libro_compras WHERE id = ?"
        return execute_query(query, (id_compra,))
