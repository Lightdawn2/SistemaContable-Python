"""
Modelo para el Balance de Comprobación
"""
from database.queries import fetch_all


class BalanceComprobacionModel:
    """Maneja las operaciones del Balance de Comprobación"""
    
    @staticmethod
    def get_balance(fecha_desde=None, fecha_hasta=None):
        """
        Obtiene el balance de comprobación con:
        - Saldo inicial
        - Movimientos del período (debe/haber)
        - Saldo final
        """
        # Query para obtener movimientos por cuenta
        query = """
            SELECT 
                p.codigo,
                p.nombre,
                p.elemento,
                COALESCE(SUM(d.debe), 0) as total_debe,
                COALESCE(SUM(d.haber), 0) as total_haber
            FROM plan_cuentas p
            LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
            LEFT JOIN comprobantes c ON d.numero_comprobante = c.numero
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
        
        query += """
            GROUP BY p.codigo, p.nombre, p.elemento
            HAVING (total_debe > 0 OR total_haber > 0)
            ORDER BY p.codigo
        """
        
        if params:
            resultados = fetch_all(query, params)
        else:
            resultados = fetch_all(query)
        
        # Calcular saldos según naturaleza de la cuenta
        balance = []
        for codigo, nombre, elemento, debe, haber in resultados:
            # Calcular saldo según naturaleza
            if elemento in ['Activo', 'Gasto', 'Costo']:
                # Naturaleza Deudora: Saldo = Debe - Haber
                saldo = debe - haber
                saldo_deudor = saldo if saldo > 0 else 0
                saldo_acreedor = abs(saldo) if saldo < 0 else 0
            else:  # Pasivo, Patrimonio, Ingreso
                # Naturaleza Acreedora: Saldo = Haber - Debe
                saldo = haber - debe
                saldo_acreedor = saldo if saldo > 0 else 0
                saldo_deudor = abs(saldo) if saldo < 0 else 0
            
            balance.append({
                'codigo': codigo,
                'nombre': nombre,
                'elemento': elemento,
                'debe': debe,
                'haber': haber,
                'saldo_deudor': saldo_deudor,
                'saldo_acreedor': saldo_acreedor
            })
        
        return balance
    
    @staticmethod
    def get_totales(balance):
        """Calcula los totales del balance"""
        total_debe = sum(item['debe'] for item in balance)
        total_haber = sum(item['haber'] for item in balance)
        total_saldo_deudor = sum(item['saldo_deudor'] for item in balance)
        total_saldo_acreedor = sum(item['saldo_acreedor'] for item in balance)
        
        return {
            'total_debe': total_debe,
            'total_haber': total_haber,
            'total_saldo_deudor': total_saldo_deudor,
            'total_saldo_acreedor': total_saldo_acreedor,
            'balance_movimientos': abs(total_debe - total_haber),
            'balance_saldos': abs(total_saldo_deudor - total_saldo_acreedor)
        }
