"""
Modelo para el Libro de Compras
"""
from database.queries import execute_query, fetch_all
from database.db_manager import get_connection


class LibroComprasModel:
    """Maneja las operaciones del Libro de Compras"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las compras"""
        query = """
            SELECT id, fecha, tipo_documento, numero_documento, rut_proveedor, 
                   razon_social, neto, iva, total, exenta, numero_comprobante 
            FROM libro_compras 
            ORDER BY fecha DESC
        """
        return fetch_all(query)
    
    @staticmethod
    def create(fecha, tipo_documento, numero_documento, rut_proveedor, 
               razon_social, neto, iva, total, exenta=0):
        """
        Registra una nueva compra y genera el comprobante contable automáticamente
        Asiento: 
        - Debe: Gasto/Costo (busca cuenta de gastos)
        - Debe: IVA Crédito Fiscal (solo si NO es exenta)
        - Haber: Proveedores
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Buscar códigos de cuentas dinámicamente
            # Buscar cuenta de gastos de administración (cualquier gasto que no sea costo de ventas)
            cursor.execute(
                "SELECT codigo FROM plan_cuentas WHERE elemento = 'Gastos' AND categoria != 'Costo de Ventas' ORDER BY codigo LIMIT 1"
            )
            cuenta_gasto = cursor.fetchone()
            
            # Buscar IVA Crédito Fiscal
            cursor.execute(
                "SELECT codigo FROM plan_cuentas WHERE nombre LIKE '%IVA%' AND (nombre LIKE '%Cr_dito%' OR nombre LIKE '%Credito%') LIMIT 1"
            )
            cuenta_iva_cf = cursor.fetchone()
            
            # Buscar Proveedores
            cursor.execute(
                "SELECT codigo FROM plan_cuentas WHERE nombre LIKE '%Proveedor%' LIMIT 1"
            )
            cuenta_proveedores = cursor.fetchone()
            
            if not cuenta_gasto or not cuenta_proveedores:
                raise Exception("No se encontraron las cuentas contables necesarias en el plan de cuentas. Asegúrese de tener creadas las cuentas: Gastos, Proveedores y opcionalmente IVA Crédito Fiscal.")
            
            if not exenta and not cuenta_iva_cf:
                raise Exception("No se encontró la cuenta de IVA Crédito Fiscal en el plan de cuentas.")
            
            # Generar glosa para el comprobante
            glosa = f"Compra {tipo_documento} N° {numero_documento} - {razon_social}"
            
            # 1. Crear el comprobante
            cursor.execute(
                "INSERT INTO comprobantes (fecha, glosa) VALUES (?, ?)",
                (fecha, glosa)
            )
            numero_comprobante = cursor.lastrowid
            
            # 2. Insertar detalle del comprobante (partida doble)
            # Línea 1: Gasto/Costo por compra (DEBE)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, 1, cuenta_gasto[0], neto, 0)
            )
            
            linea = 2
            if not exenta:
                # Línea 2: IVA Crédito Fiscal (DEBE)
                cursor.execute(
                    """INSERT INTO detalle_comprobantes 
                       (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (numero_comprobante, linea, cuenta_iva_cf[0], iva, 0)
                )
                linea += 1
            
            # Última línea: Proveedores (HABER)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, linea, cuenta_proveedores[0], 0, total)
            )
            
            # 3. Registrar en libro de compras con referencia al comprobante
            cursor.execute(
                """INSERT INTO libro_compras 
                   (fecha, tipo_documento, numero_documento, rut_proveedor, 
                    razon_social, neto, iva, total, exenta, numero_comprobante) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (fecha, tipo_documento, numero_documento, rut_proveedor, 
                 razon_social, neto, iva, total, exenta, numero_comprobante)
            )
            
            conn.commit()
            return numero_comprobante
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def delete(id_compra):
        """Elimina una compra y su comprobante asociado"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener número de comprobante antes de eliminar
            cursor.execute("SELECT numero_comprobante FROM libro_compras WHERE id = ?", (id_compra,))
            result = cursor.fetchone()
            
            if result and result[0]:
                numero_comprobante = result[0]
                # Eliminar detalle del comprobante
                cursor.execute("DELETE FROM detalle_comprobantes WHERE numero_comprobante = ?", (numero_comprobante,))
                # Eliminar comprobante
                cursor.execute("DELETE FROM comprobantes WHERE numero = ?", (numero_comprobante,))
            
            # Eliminar de libro de compras
            cursor.execute("DELETE FROM libro_compras WHERE id = ?", (id_compra,))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
