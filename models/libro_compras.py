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
        - Debe: Gasto/Costo (60001 - Gastos de Administración)
        - Debe: IVA Crédito Fiscal (11008) (solo si NO es exenta)
        - Haber: Proveedores (20001)
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
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
                (numero_comprobante, 1, 60001, neto, 0)  # 60001 = Gastos de Administración
            )
            
            linea = 2
            if not exenta:
                # Línea 2: IVA Crédito Fiscal (DEBE)
                cursor.execute(
                    """INSERT INTO detalle_comprobantes 
                       (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (numero_comprobante, linea, 11008, iva, 0)  # 11008 = IVA Crédito Fiscal
                )
                linea += 1
            
            # Última línea: Proveedores (HABER)
            cursor.execute(
                """INSERT INTO detalle_comprobantes 
                   (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                   VALUES (?, ?, ?, ?, ?)""",
                (numero_comprobante, linea, 20001, 0, total)  # 20001 = Proveedores
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
