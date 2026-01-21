"""
Configuración de Cuentas para Operaciones Automáticas

Este módulo gestiona el mapeo entre operaciones automáticas (Libro de Compras/Ventas)
y las cuentas del plan de cuentas del usuario (formato D.CC.SS.NNNN).

El usuario debe configurar qué cuentas usar para cada tipo de operación.
"""
import json
import os
from config import DB_FILE

CONFIG_FILE = os.path.join(os.path.dirname(DB_FILE), 'cuentas_config.json')


class ConfiguracionCuentas:
    """Gestiona la configuración de cuentas para operaciones automáticas"""
    
    # Estructura por defecto (vacía - debe ser configurada por el usuario)
    DEFAULT_CONFIG = {
        "libro_compras": {
            "cuenta_gasto": None,  # Código cuenta de gasto (ej: "5.01.01.0001")
            "cuenta_iva_credito": None,  # IVA Crédito Fiscal (ej: "1.01.03.0001")
            "cuenta_proveedores": None  # Proveedores (ej: "2.01.01.0001")
        },
        "libro_ventas": {
            "cuenta_ingreso": None,  # Cuenta de ingresos (ej: "4.01.01.0001")
            "cuenta_iva_debito": None,  # IVA Débito Fiscal (ej: "2.01.03.0001")
            "cuenta_clientes": None  # Clientes (ej: "1.01.02.0001")
        }
    }
    
    @staticmethod
    def cargar_configuracion():
        """Carga la configuración desde el archivo JSON"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
                return ConfiguracionCuentas.DEFAULT_CONFIG.copy()
        return ConfiguracionCuentas.DEFAULT_CONFIG.copy()
    
    @staticmethod
    def guardar_configuracion(config):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar configuración: {e}")
            return False
    
    @staticmethod
    def validar_cuenta(codigo_cuenta):
        """
        Valida que una cuenta existe en plan_cuentas
        Retorna: (existe: bool, info: dict)
        """
        from database.db_manager import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT codigo, nombre, elemento FROM plan_cuentas WHERE codigo = ?",
                (codigo_cuenta,)
            )
            result = cursor.fetchone()
            
            if result:
                return True, {
                    'codigo': result[0],
                    'nombre': result[1],
                    'elemento': result[2]
                }
            return False, None
        finally:
            conn.close()
    
    @staticmethod
    def obtener_cuenta_compras(tipo):
        """
        Obtiene el código de cuenta configurado para Libro de Compras
        tipo: 'gasto', 'iva_credito', 'proveedores'
        """
        config = ConfiguracionCuentas.cargar_configuracion()
        tipo_map = {
            'gasto': 'cuenta_gasto',
            'iva_credito': 'cuenta_iva_credito',
            'proveedores': 'cuenta_proveedores'
        }
        
        if tipo in tipo_map:
            return config['libro_compras'].get(tipo_map[tipo])
        return None
    
    @staticmethod
    def obtener_cuenta_ventas(tipo):
        """
        Obtiene el código de cuenta configurado para Libro de Ventas
        tipo: 'ingreso', 'iva_debito', 'clientes'
        """
        config = ConfiguracionCuentas.cargar_configuracion()
        tipo_map = {
            'ingreso': 'cuenta_ingreso',
            'iva_debito': 'cuenta_iva_debito',
            'clientes': 'cuenta_clientes'
        }
        
        if tipo in tipo_map:
            return config['libro_ventas'].get(tipo_map[tipo])
        return None
    
    @staticmethod
    def esta_configurado():
        """
        Verifica si todas las cuentas necesarias están configuradas
        Retorna: (completo: bool, faltantes: list)
        """
        config = ConfiguracionCuentas.cargar_configuracion()
        faltantes = []
        
        for libro, cuentas in config.items():
            for tipo_cuenta, codigo in cuentas.items():
                if not codigo:
                    faltantes.append(f"{libro}.{tipo_cuenta}")
        
        return len(faltantes) == 0, faltantes
    
    @staticmethod
    def buscar_cuentas_sugeridas():
        """
        Busca cuentas en el plan que podrían servir para cada operación
        basándose en elemento y subcategoría
        """
        from database.db_manager import get_connection
        
        conn = get_connection()
        cursor = conn.cursor()
        
        sugerencias = {
            'gasto': [],
            'iva_credito': [],
            'proveedores': [],
            'ingreso': [],
            'iva_debito': [],
            'clientes': []
        }
        
        try:
            # Buscar cuentas de Gastos
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Gastos'
                ORDER BY codigo
            """)
            sugerencias['gasto'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
            # Buscar IVA Crédito (Activos + "IVA" o "Impuesto")
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Activos' 
                AND (LOWER(nombre) LIKE '%iva%' OR LOWER(subcategoria) LIKE '%impuesto%')
                ORDER BY codigo
            """)
            sugerencias['iva_credito'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
            # Buscar Proveedores (Pasivos + "Proveedor" o "Pagar")
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Pasivos' 
                AND (LOWER(nombre) LIKE '%proveedor%' OR LOWER(subcategoria) LIKE '%pagar%')
                ORDER BY codigo
            """)
            sugerencias['proveedores'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
            # Buscar cuentas de Ingresos
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Ingresos'
                ORDER BY codigo
            """)
            sugerencias['ingreso'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
            # Buscar IVA Débito (Pasivos + "IVA" o "Impuesto")
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Pasivos' 
                AND (LOWER(nombre) LIKE '%iva%' OR LOWER(subcategoria) LIKE '%impuesto%')
                ORDER BY codigo
            """)
            sugerencias['iva_debito'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
            # Buscar Clientes (Activos + "Cliente" o "Cobrar")
            cursor.execute("""
                SELECT codigo, nombre, subcategoria 
                FROM plan_cuentas 
                WHERE elemento = 'Activos' 
                AND (LOWER(nombre) LIKE '%cliente%' OR LOWER(subcategoria) LIKE '%cobrar%')
                ORDER BY codigo
            """)
            sugerencias['clientes'] = [
                {'codigo': r[0], 'nombre': r[1], 'subcategoria': r[2]} 
                for r in cursor.fetchall()
            ]
            
        finally:
            conn.close()
        
        return sugerencias
