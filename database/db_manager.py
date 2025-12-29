"""
Gestor de base de datos y conexiones
"""
import sqlite3
from config import DB_FILE


def get_connection():
    """Obtiene una conexión a la base de datos"""
    return sqlite3.connect(DB_FILE)


def init_db():
    """Inicializa la base de datos con todas las tablas necesarias"""
    conn = get_connection()
    c = conn.cursor()
    
    # Tabla: Plan de Cuentas
    c.execute("""
        CREATE TABLE IF NOT EXISTS plan_cuentas (
            codigo INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            elemento TEXT NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT,
            grupo TEXT
        )
    """)
    
    # Tabla: Comprobantes
    c.execute("""
        CREATE TABLE IF NOT EXISTS comprobantes (
            numero INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            glosa TEXT NOT NULL
        )
    """)
    
    # Tabla: Detalle de Comprobantes (Asientos contables)
    c.execute("""
        CREATE TABLE IF NOT EXISTS detalle_comprobantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_comprobante INTEGER NOT NULL,
            linea INTEGER NOT NULL,
            codigo_cuenta INTEGER NOT NULL,
            debe REAL DEFAULT 0,
            haber REAL DEFAULT 0,
            FOREIGN KEY (numero_comprobante) REFERENCES comprobantes(numero),
            FOREIGN KEY (codigo_cuenta) REFERENCES plan_cuentas(codigo)
        )
    """)
    
    # Tabla: Libro de Compras
    c.execute("""
        CREATE TABLE IF NOT EXISTS libro_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            tipo_documento TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            rut_proveedor TEXT NOT NULL,
            razon_social TEXT NOT NULL,
            neto REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            exenta INTEGER NOT NULL DEFAULT 0,
            numero_comprobante INTEGER,
            FOREIGN KEY (numero_comprobante) REFERENCES comprobantes(numero)
        )
    """)

    # Migración simple: asegurar columna 'exenta' en libro_compras
    c.execute("PRAGMA table_info(libro_compras)")
    columnas = [row[1] for row in c.fetchall()]
    if 'exenta' not in columnas:
        c.execute("ALTER TABLE libro_compras ADD COLUMN exenta INTEGER NOT NULL DEFAULT 0")
    
    # Tabla: Libro de Ventas
    c.execute("""
        CREATE TABLE IF NOT EXISTS libro_ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            tipo_documento TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            rut_cliente TEXT NOT NULL,
            razon_social TEXT NOT NULL,
            neto REAL NOT NULL,
            iva REAL NOT NULL,
            total REAL NOT NULL,
            numero_comprobante INTEGER,
            FOREIGN KEY (numero_comprobante) REFERENCES comprobantes(numero)
        )
    """)
    
    conn.commit()
    
    # NO insertar plan de cuentas inicial - Los alumnos lo crearán desde cero
    # El sistema comienza completamente vacío para fines educativos
    
    conn.close()


def _insertar_cuentas_iniciales(cursor):
    """
    Inserta el plan de cuentas inicial
    NOTA: Esta función ya NO se ejecuta automáticamente.
    Se mantiene aquí como referencia para los profesores/alumnos.
    Los alumnos deben crear su propio plan de cuentas desde la interfaz.
    """
    cuentas_iniciales = [
        # Activos Corrientes
        (11001, 'Caja', 'Activo', 'Activo Corriente', 'Disponible', 'Efectivo'),
        (11002, 'Banco', 'Activo', 'Activo Corriente', 'Disponible', 'Bancos'),
        (11003, 'Depósitos a Plazo', 'Activo', 'Activo Corriente', 'Disponible', 'Inversiones'),
        (11004, 'Clientes', 'Activo', 'Activo Corriente', 'Exigible', 'Deudores'),
        (11005, 'Deudores Comerciales', 'Activo', 'Activo Corriente', 'Exigible', 'Deudores'),
        (11006, 'Inventarios', 'Activo', 'Activo Corriente', 'Realizable', 'Existencias'),
        (11007, 'Productos en Proceso', 'Activo', 'Activo Corriente', 'Realizable', 'Existencias'),
        (11008, 'IVA Crédito Fiscal', 'Activo', 'Activo Corriente', 'Exigible', 'Impuestos'),
        # Activos No Corrientes
        (12001, 'Vehículos', 'Activo', 'Activo No Corriente', 'Fijo', 'PPE'),
        (12002, 'Terrenos', 'Activo', 'Activo No Corriente', 'Fijo', 'PPE'),
        (12003, 'Maquinarias', 'Activo', 'Activo No Corriente', 'Fijo', 'PPE'),
        (12004, 'Equipos', 'Activo', 'Activo No Corriente', 'Fijo', 'PPE'),
        # Pasivos Corrientes
        (20001, 'Proveedores', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Deudas'),
        (20002, 'Acreedores', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Deudas'),
        (20003, 'Préstamos Bancarios', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Deudas'),
        (20004, 'IVA Débito Fiscal', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Impuestos'),
        (20005, 'Obligaciones con el Público', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Deudas'),
        (20006, 'Impuestos a la Renta por Pagar', 'Pasivo', 'Pasivo Corriente', 'Exigible', 'Impuestos'),
        # Pasivos No Corrientes
        (22001, 'Préstamos Bancarios Largo Plazo', 'Pasivo', 'Pasivo No Corriente', 'Exigible', 'Deudas'),
        (22002, 'Provisiones', 'Pasivo', 'Pasivo No Corriente', 'Exigible', 'Provisiones'),
        # Patrimonio
        (30001, 'Capital Aportado', 'Patrimonio', 'Capital', 'Capital', 'Capital'),
        (30002, 'Resultado Acumulado', 'Patrimonio', 'Resultados', 'Resultados', 'Resultados'),
        (30003, 'Resultado del Ejercicio', 'Patrimonio', 'Resultados', 'Resultados', 'Resultados'),
        # Ingresos
        (40001, 'Ingresos por Ventas', 'Ingreso', 'Ingresos Operacionales', 'Ventas', 'Ventas'),
        (40002, 'Otros Ingresos', 'Ingreso', 'Ingresos No Operacionales', 'Otros', 'Otros'),
        (40003, 'Ingresos Financieros', 'Ingreso', 'Ingresos No Operacionales', 'Financieros', 'Financieros'),
        # Costos
        (50001, 'Costo de Ventas', 'Costo', 'Costos Operacionales', 'Costos', 'Costos'),
        # Gastos
        (60001, 'Gastos de Administración', 'Gasto', 'Gastos Operacionales', 'Administración', 'Gastos'),
        (60002, 'Gastos Comerciales', 'Gasto', 'Gastos Operacionales', 'Comercial', 'Gastos'),
        (60003, 'Otros Gastos', 'Gasto', 'Gastos No Operacionales', 'Otros', 'Gastos'),
        (60004, 'Costos Financieros', 'Gasto', 'Gastos No Operacionales', 'Financieros', 'Gastos'),
    ]
    cursor.executemany(
        "INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) VALUES (?, ?, ?, ?, ?, ?)",
        cuentas_iniciales
    )


def reset_database():
    """
    Resetea completamente la base de datos.
    ELIMINA todos los datos y crea las tablas vacías de nuevo.
    Útil para que los alumnos puedan empezar desde cero si cometen errores.
    """
    import os
    from config import DB_FILE
    
    # Eliminar el archivo de base de datos si existe
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    
    # Crear nuevamente las tablas vacías
    init_db()
