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
            WHERE p.elemento IN ('Activos', 'Pasivos', 'Patrimonio')
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
            WHERE p.elemento IN ('Ingresos', 'Gastos')
            GROUP BY p.codigo, p.nombre, p.elemento, p.categoria
            ORDER BY p.codigo
        """
        return fetch_all(query)
    
    @staticmethod
    def calcular_utilidad_impuesto():
        """Calcula la utilidad del ejercicio y el impuesto por pagar"""
        from config import IMPUESTO_RENTA_RATE
        
        cuentas = ReportesModel.get_estado_resultados()
        
        total_ingresos = 0
        total_costos = 0
        total_gastos = 0
        
        for codigo, nombre, elemento, categoria, debe, haber in cuentas:
            if elemento == 'Ingresos':
                # Ingresos: naturaleza acreedora (Haber - Debe)
                total_ingresos += (haber - debe)
            elif elemento == 'Gastos':
                # Gastos: naturaleza deudora (Debe - Haber)
                # En el nuevo sistema, los costos están incluidos en Gastos
                if 'Costo de Ventas' in categoria:
                    total_costos += (debe - haber)
                else:
                    total_gastos += (debe - haber)
        
        # Cálculo según estructura NIIF:
        # Utilidad Bruta = Ingresos - Costos
        # Resultado Operacional = Utilidad Bruta - Gastos Operacionales
        # Resultado antes de impuesto = Resultado Operacional - Gastos Financieros - Otros
        utilidad_antes_impuesto = total_ingresos - total_costos - total_gastos
        
        # Impuesto solo si hay utilidad
        impuesto = utilidad_antes_impuesto * IMPUESTO_RENTA_RATE if utilidad_antes_impuesto > 0 else 0
        
        # Utilidad neta
        utilidad_ejercicio = utilidad_antes_impuesto - impuesto
        
        return {
            'utilidad_antes_impuesto': utilidad_antes_impuesto,
            'impuesto': impuesto,
            'utilidad_ejercicio': utilidad_ejercicio,
            'total_ingresos': total_ingresos,
            'total_costos': total_costos,
            'total_gastos': total_gastos,
            'utilidad_bruta': total_ingresos - total_costos
        }
