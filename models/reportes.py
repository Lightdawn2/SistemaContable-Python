"""
Modelo para generar reportes financieros
"""
from database.queries import fetch_all


class ReportesModel:
    """Maneja la generación de reportes contables"""
    
    @staticmethod
    def get_saldos_cuentas(elemento=None):
        """
        Obtiene los saldos de las cuentas
        Si elemento es None, obtiene todas las cuentas
        """
        if elemento:
            query = """
                SELECT 
                    p.codigo,
                    p.nombre,
                    p.elemento,
                    p.categoria,
                    COALESCE(SUM(d.debe), 0) as total_debe,
                    COALESCE(SUM(d.haber), 0) as total_haber
                FROM plan_cuentas p
                LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
                WHERE p.elemento = ?
                GROUP BY p.codigo, p.nombre, p.elemento, p.categoria
                ORDER BY p.codigo
            """
            return fetch_all(query, (elemento,))
        else:
            query = """
                SELECT 
                    p.codigo,
                    p.nombre,
                    p.elemento,
                    p.categoria,
                    COALESCE(SUM(d.debe), 0) as total_debe,
                    COALESCE(SUM(d.haber), 0) as total_haber
                FROM plan_cuentas p
                LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
                GROUP BY p.codigo, p.nombre, p.elemento, p.categoria
                ORDER BY p.codigo
            """
            return fetch_all(query)
    
    @staticmethod
    def get_estado_situacion_financiera():
        """Obtiene datos para el Estado de Situación Financiera"""
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                p.elemento,
                p.categoria,
                COALESCE(SUM(d.debe), 0) as total_debe,
                COALESCE(SUM(d.haber), 0) as total_haber
            FROM plan_cuentas p
            LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
            WHERE p.elemento IN ('Activo', 'Pasivo', 'Patrimonio')
            GROUP BY p.codigo, p.nombre, p.elemento, p.categoria
            ORDER BY p.codigo
        """
        return fetch_all(query)
    
    @staticmethod
    def get_estado_resultados():
        """Obtiene datos para el Estado de Resultados"""
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                p.elemento,
                p.categoria,
                COALESCE(SUM(d.debe), 0) as total_debe,
                COALESCE(SUM(d.haber), 0) as total_haber
            FROM plan_cuentas p
            LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
            WHERE p.elemento IN ('Ingreso', 'Costo', 'Gasto')
            GROUP BY p.codigo, p.nombre, p.elemento, p.categoria
            ORDER BY p.codigo
        """
        return fetch_all(query)
