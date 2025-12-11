"""
Modelo para Comprobantes Contables
"""
import sqlite3
from database.db_manager import get_connection
from database.queries import fetch_all, fetch_one


class ComprobantesModel:
    """Maneja las operaciones de comprobantes contables"""
    
    @staticmethod
    def get_all():
        """Obtiene todos los comprobantes"""
        query = "SELECT numero, fecha, glosa FROM comprobantes ORDER BY numero DESC"
        return fetch_all(query)
    
    @staticmethod
    def get_by_numero(numero):
        """Obtiene un comprobante por su número"""
        query = "SELECT numero, fecha, glosa FROM comprobantes WHERE numero = ?"
        return fetch_one(query, (numero,))
    
    @staticmethod
    def get_detalle(numero_comprobante):
        """Obtiene el detalle de un comprobante"""
        query = """
            SELECT d.linea, d.codigo_cuenta, p.nombre, d.debe, d.haber
            FROM detalle_comprobantes d
            JOIN plan_cuentas p ON d.codigo_cuenta = p.codigo
            WHERE d.numero_comprobante = ?
            ORDER BY d.linea
        """
        return fetch_all(query, (numero_comprobante,))
    
    @staticmethod
    def create(fecha, glosa, detalles):
        """
        Crea un nuevo comprobante con su detalle
        detalles: lista de diccionarios con 'linea', 'codigo', 'debe', 'haber'
        """
        conn = get_connection()
        c = conn.cursor()
        
        try:
            # Insertar comprobante
            c.execute("INSERT INTO comprobantes (fecha, glosa) VALUES (?, ?)", (fecha, glosa))
            numero_comprobante = c.lastrowid
            
            # Insertar detalle
            for det in detalles:
                c.execute(
                    """INSERT INTO detalle_comprobantes 
                       (numero_comprobante, linea, codigo_cuenta, debe, haber) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (numero_comprobante, det['linea'], det['codigo'], det['debe'], det['haber'])
                )
            
            conn.commit()
            return numero_comprobante
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def delete(numero):
        """Elimina un comprobante y su detalle"""
        conn = get_connection()
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM detalle_comprobantes WHERE numero_comprobante = ?", (numero,))
            c.execute("DELETE FROM comprobantes WHERE numero = ?", (numero,))
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
