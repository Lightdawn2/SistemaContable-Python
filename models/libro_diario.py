"""
Modelo para el Libro Diario
"""
from database.queries import fetch_all


class LibroDiarioModel:
    """Maneja las operaciones del Libro Diario"""
    
    @staticmethod
    def get_movimientos(fecha_desde=None, fecha_hasta=None):
        """
        Obtiene todos los movimientos del libro diario en orden cronológico
        con detalle de cada transacción
        """
        query = """
            SELECT 
                c.fecha,
                c.numero,
                c.glosa,
                d.codigo_cuenta,
                p.nombre as nombre_cuenta,
                d.debe,
                d.haber
            FROM comprobantes c
            INNER JOIN detalle_comprobantes d ON c.numero = d.numero_comprobante
            INNER JOIN plan_cuentas p ON d.codigo_cuenta = p.codigo
        """
        
        params = []
        if fecha_desde and fecha_hasta:
            query += " WHERE c.fecha BETWEEN ? AND ?"
            params = [fecha_desde, fecha_hasta]
        elif fecha_desde:
            query += " WHERE c.fecha >= ?"
            params = [fecha_desde]
        elif fecha_hasta:
            query += " WHERE c.fecha <= ?"
            params = [fecha_hasta]
        
        query += " ORDER BY c.fecha, c.numero, d.id"
        
        if params:
            return fetch_all(query, params)
        return fetch_all(query)
    
    @staticmethod
    def get_totales_generales(fecha_desde=None, fecha_hasta=None):
        """Obtiene los totales generales de debe y haber"""
        query = """
            SELECT 
                COALESCE(SUM(d.debe), 0) as total_debe,
                COALESCE(SUM(d.haber), 0) as total_haber
            FROM detalle_comprobantes d
            INNER JOIN comprobantes c ON d.numero_comprobante = c.numero
        """
        
        params = []
        if fecha_desde and fecha_hasta:
            query += " WHERE c.fecha BETWEEN ? AND ?"
            params = [fecha_desde, fecha_hasta]
        elif fecha_desde:
            query += " WHERE c.fecha >= ?"
            params = [fecha_desde]
        elif fecha_hasta:
            query += " WHERE c.fecha <= ?"
            params = [fecha_hasta]
        
        if params:
            result = fetch_all(query, params)
        else:
            result = fetch_all(query)
            
        if result:
            return result[0]
        return (0, 0)
