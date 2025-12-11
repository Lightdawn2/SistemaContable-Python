"""
Modelo para el Libro de Ventas
"""
from database.queries import execute_query, fetch_all


class LibroVentasModel:
    """Maneja las operaciones del Libro de Ventas"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las ventas"""
        query = """
            SELECT id, fecha, tipo_documento, numero_documento, rut_cliente, 
                   razon_social, neto, iva, total 
            FROM libro_ventas 
            ORDER BY fecha DESC
        """
        return fetch_all(query)
    
    @staticmethod
    def create(fecha, tipo_documento, numero_documento, rut_cliente, 
               razon_social, neto, iva, total):
        """Registra una nueva venta"""
        query = """
            INSERT INTO libro_ventas 
            (fecha, tipo_documento, numero_documento, rut_cliente, razon_social, neto, iva, total) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        return execute_query(query, (fecha, tipo_documento, numero_documento, 
                                     rut_cliente, razon_social, neto, iva, total))
    
    @staticmethod
    def delete(id_venta):
        """Elimina una venta"""
        query = "DELETE FROM libro_ventas WHERE id = ?"
        return execute_query(query, (id_venta,))
