"""
Modelo para el Libro de Ventas
"""
from database.queries import execute_query, fetch_all
from database.db_manager import get_connection


class LibroVentasModel:
    """Maneja las operaciones del Libro de Ventas"""
    
    @staticmethod
    def get_all():
        """Obtiene todas las ventas"""
        query = """
            SELECT id, fecha, tipo_documento, numero_documento, rut_cliente, 
                   razon_social, neto, iva, total, numero_comprobante 
            FROM libro_ventas 
            ORDER BY fecha DESC
        """
        return fetch_all(query)
    
    @staticmethod
    def create(fecha, tipo_documento, numero_documento, rut_cliente, 
               razon_social, neto, iva, total):
        """
        Registra una nueva venta y genera el comprobante contable automáticamente
        Asiento:
        - Debe: Clientes (11004)
        - Haber: Ingresos por Ventas (40001)
        - Haber: IVA Débito Fiscal (20004)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Generar glosa para el comprobante
            glosa = f"Venta {tipo_documento} N° {numero_documento} - {razon_social}"
            
            # 1. Crear el comprobante
            cursor.execute(
                "INSERT INTO comprobantes (fecha, glosa) VALUES (?, ?)",
                (fecha, glosa)
            )
            numero_comprobante = cursor.lastrowid
            
            # 2. Insertar detalle del comprobante (partida doble)
            # Línea 1: Clientes (DEBE)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, 1, 11004, total, 0)  # 11004 = Clientes
            )
            
            # Línea 2: Ingresos por Ventas (HABER)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, 2, 40001, 0, neto)  # 40001 = Ingresos por Ventas
            )
            
            # Línea 3: IVA Débito Fiscal (HABER)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, 3, 20004, 0, iva)  # 20004 = IVA Débito Fiscal
            )
            
            # 3. Registrar en libro de ventas con referencia al comprobante
            cursor.execute(
                """INSERT INTO libro_ventas 
                   (fecha, tipo_documento, numero_documento, rut_cliente, 
                    razon_social, neto, iva, total, numero_comprobante) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (fecha, tipo_documento, numero_documento, rut_cliente, 
                 razon_social, neto, iva, total, numero_comprobante)
            )
            
            conn.commit()
            return numero_comprobante
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def delete(id_venta):
        """Elimina una venta y su comprobante asociado"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            # Obtener número de comprobante antes de eliminar
            cursor.execute("SELECT numero_comprobante FROM libro_ventas WHERE id = ?", (id_venta,))
            result = cursor.fetchone()
            
            if result and result[0]:
                numero_comprobante = result[0]
                # Eliminar detalle del comprobante
                cursor.execute("DELETE FROM detalle_comprobantes WHERE numero_comprobante = ?", (numero_comprobante,))
                # Eliminar comprobante
                cursor.execute("DELETE FROM comprobantes WHERE numero = ?", (numero_comprobante,))
            
            # Eliminar de libro de ventas
            cursor.execute("DELETE FROM libro_ventas WHERE id = ?", (id_venta,))
            
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
