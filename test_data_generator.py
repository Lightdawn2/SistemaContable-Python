"""
Script para generar datos de prueba realistas según normativa chilena y NIIF
Este script crea un caso de estudio completo con transacciones que permiten
verificar que el balance cuadre correctamente.
"""
import sqlite3
from datetime import datetime
from config import DB_FILE, IVA_RATE

def limpiar_datos():
    """Limpia todas las tablas para empezar de cero"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("DELETE FROM detalle_comprobantes")
    c.execute("DELETE FROM comprobantes")
    c.execute("DELETE FROM libro_compras")
    c.execute("DELETE FROM libro_ventas")
    c.execute("DELETE FROM plan_cuentas")
    
    conn.commit()
    conn.close()
    print("✓ Datos anteriores eliminados")

def insertar_plan_cuentas():
    """
    Inserta un plan de cuentas básico según estructura chilena
    Códigos según práctica contable chilena:
    - 1xxxx: Activos
    - 2xxxx: Pasivos
    - 3xxxx: Patrimonio
    - 4xxxx: Ingresos
    - 5xxxx: Costos
    - 6xxxx: Gastos
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    cuentas = [
        # ACTIVOS CORRIENTES (11xxx)
        (11001, 'Caja', 'Activo', 'Activo Corriente', 'Disponible', 'Efectivo y Equivalentes'),
        (11002, 'Banco Estado Cta Cte', 'Activo', 'Activo Corriente', 'Disponible', 'Efectivo y Equivalentes'),
        (11003, 'Banco Chile Cta Cte', 'Activo', 'Activo Corriente', 'Disponible', 'Efectivo y Equivalentes'),
        (11101, 'Clientes', 'Activo', 'Activo Corriente', 'Deudores Comerciales', 'Cuentas por Cobrar'),
        (11102, 'Documentos por Cobrar', 'Activo', 'Activo Corriente', 'Deudores Comerciales', 'Cuentas por Cobrar'),
        (11201, 'IVA Crédito Fiscal', 'Activo', 'Activo Corriente', 'Impuestos', 'Activos por Impuestos'),
        (11301, 'Mercaderías', 'Activo', 'Activo Corriente', 'Inventarios', 'Existencias'),
        
        # ACTIVOS NO CORRIENTES (12xxx)
        (12001, 'Terrenos', 'Activo', 'Activo No Corriente', 'Propiedades Planta y Equipo', 'PPE'),
        (12002, 'Edificios', 'Activo', 'Activo No Corriente', 'Propiedades Planta y Equipo', 'PPE'),
        (12003, 'Vehículos', 'Activo', 'Activo No Corriente', 'Propiedades Planta y Equipo', 'PPE'),
        (12004, 'Muebles y Útiles', 'Activo', 'Activo No Corriente', 'Propiedades Planta y Equipo', 'PPE'),
        (12005, 'Equipos Computacionales', 'Activo', 'Activo No Corriente', 'Propiedades Planta y Equipo', 'PPE'),
        (12101, 'Depreciación Acumulada Edificios', 'Activo', 'Activo No Corriente', 'Depreciación Acumulada', 'PPE'),
        (12102, 'Depreciación Acumulada Vehículos', 'Activo', 'Activo No Corriente', 'Depreciación Acumulada', 'PPE'),
        
        # PASIVOS CORRIENTES (21xxx)
        (21001, 'Proveedores', 'Pasivo', 'Pasivo Corriente', 'Cuentas por Pagar Comerciales', 'Acreedores'),
        (21002, 'Documentos por Pagar', 'Pasivo', 'Pasivo Corriente', 'Cuentas por Pagar Comerciales', 'Acreedores'),
        (21101, 'IVA Débito Fiscal', 'Pasivo', 'Pasivo Corriente', 'Impuestos', 'Pasivos por Impuestos'),
        (21102, 'IVA por Pagar', 'Pasivo', 'Pasivo Corriente', 'Impuestos', 'Pasivos por Impuestos'),
        (21201, 'Préstamos Bancarios Corto Plazo', 'Pasivo', 'Pasivo Corriente', 'Préstamos', 'Obligaciones Financieras'),
        (21301, 'Remuneraciones por Pagar', 'Pasivo', 'Pasivo Corriente', 'Provisiones', 'Obligaciones Laborales'),
        
        # PASIVOS NO CORRIENTES (22xxx)
        (22001, 'Préstamos Bancarios Largo Plazo', 'Pasivo', 'Pasivo No Corriente', 'Préstamos', 'Obligaciones Financieras'),
        (22002, 'Provisiones Largo Plazo', 'Pasivo', 'Pasivo No Corriente', 'Provisiones', 'Otras Provisiones'),
        
        # PATRIMONIO (31xxx)
        (31001, 'Capital', 'Patrimonio', 'Capital', 'Capital Emitido', 'Capital Social'),
        (31002, 'Reservas', 'Patrimonio', 'Otras Reservas', 'Reservas', 'Reservas'),
        (31003, 'Resultados Acumulados', 'Patrimonio', 'Resultados Retenidos', 'Utilidades', 'Resultados'),
        
        # INGRESOS (41xxx)
        (41001, 'Ventas de Mercaderías', 'Ingreso', 'Ingresos Ordinarios', 'Ventas', 'Ingresos de Actividades Ordinarias'),
        (41002, 'Prestación de Servicios', 'Ingreso', 'Ingresos Ordinarios', 'Servicios', 'Ingresos de Actividades Ordinarias'),
        (41101, 'Descuentos Otorgados', 'Ingreso', 'Ingresos Ordinarios', 'Descuentos', 'Descuentos y Rebajas'),
        (41201, 'Intereses Ganados', 'Ingreso', 'Otros Ingresos', 'Financieros', 'Ingresos Financieros'),
        
        # COSTOS (51xxx)
        (51001, 'Costo de Ventas', 'Costo', 'Costo de Ventas', 'Costo Mercaderías', 'Costo de Ventas'),
        
        # GASTOS (61xxx)
        (61001, 'Remuneraciones', 'Gasto', 'Gastos de Administración', 'Personal', 'Gastos de Personal'),
        (61002, 'Honorarios', 'Gasto', 'Gastos de Administración', 'Personal', 'Gastos de Personal'),
        (61003, 'Arriendos', 'Gasto', 'Gastos de Administración', 'Operacionales', 'Gastos Operacionales'),
        (61004, 'Luz, Agua y Gas', 'Gasto', 'Gastos de Administración', 'Operacionales', 'Gastos Operacionales'),
        (61005, 'Útiles de Oficina', 'Gasto', 'Gastos de Administración', 'Operacionales', 'Gastos Operacionales'),
        (61101, 'Publicidad y Propaganda', 'Gasto', 'Gastos de Ventas', 'Marketing', 'Gastos de Comercialización'),
        (61102, 'Comisiones de Ventas', 'Gasto', 'Gastos de Ventas', 'Comisiones', 'Gastos de Comercialización'),
        (61201, 'Intereses Bancarios', 'Gasto', 'Gastos Financieros', 'Financieros', 'Costos Financieros'),
        (61202, 'Comisiones Bancarias', 'Gasto', 'Gastos Financieros', 'Financieros', 'Costos Financieros'),
        (61301, 'Depreciación del Ejercicio', 'Gasto', 'Gastos de Administración', 'Depreciación', 'Depreciaciones'),
    ]
    
    c.executemany(
        "INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) VALUES (?, ?, ?, ?, ?, ?)",
        cuentas
    )
    
    conn.commit()
    conn.close()
    print(f"✓ {len(cuentas)} cuentas insertadas en el Plan de Cuentas")

def crear_asiento(conn, fecha, glosa, movimientos):
    """
    Crea un comprobante contable con sus asientos
    movimientos: lista de tuplas (codigo_cuenta, debe, haber)
    """
    c = conn.cursor()
    
    # Insertar comprobante
    c.execute("INSERT INTO comprobantes (fecha, glosa) VALUES (?, ?)", (fecha, glosa))
    numero_comp = c.lastrowid
    
    # Insertar detalles
    for linea, (codigo_cuenta, debe, haber) in enumerate(movimientos, 1):
        c.execute(
            "INSERT INTO detalle_comprobantes (numero_comprobante, linea, codigo_cuenta, debe, haber) VALUES (?, ?, ?, ?, ?)",
            (numero_comp, linea, codigo_cuenta, debe, haber)
        )
    
    # Verificar cuadre
    total_debe = sum(m[1] for m in movimientos)
    total_haber = sum(m[2] for m in movimientos)
    
    if abs(total_debe - total_haber) > 0.01:
        raise ValueError(f"Asiento descuadrado: Debe={total_debe:,.0f} | Haber={total_haber:,.0f}")
    
    conn.commit()
    return numero_comp

def insertar_transacciones_ejemplo():
    """
    Inserta un conjunto de transacciones realistas para un caso de estudio
    Escenario: Empresa comercial "Demo SpA" - Enero 2025
    """
    conn = sqlite3.connect(DB_FILE)
    
    print("\n=== CREANDO TRANSACCIONES DE PRUEBA ===\n")
    
    # 1. Aporte de capital inicial
    print("1. Aporte de capital...")
    crear_asiento(
        conn, 
        "2025-01-02",
        "Aporte inicial de capital en efectivo",
        [
            (11001, 50000000, 0),  # Caja DEBE
            (31001, 0, 50000000),  # Capital HABER
        ]
    )
    
    # 2. Apertura cuenta corriente bancaria
    print("2. Apertura cuenta bancaria...")
    crear_asiento(
        conn,
        "2025-01-02",
        "Depósito en Banco Estado desde caja",
        [
            (11002, 40000000, 0),  # Banco Estado DEBE
            (11001, 0, 40000000),  # Caja HABER
        ]
    )
    
    # 3. Compra de mercaderías (con IVA)
    neto_compra = 10000000
    iva_compra = neto_compra * IVA_RATE
    total_compra = neto_compra + iva_compra
    
    print("3. Compra de mercaderías...")
    numero_comp_compra = crear_asiento(
        conn,
        "2025-01-05",
        "Compra mercaderías según Factura N°1234 - Proveedor XYZ Ltda",
        [
            (11301, neto_compra, 0),      # Mercaderías DEBE
            (11201, iva_compra, 0),       # IVA CF DEBE
            (21001, 0, total_compra),     # Proveedores HABER
        ]
    )
    
    # Registrar en libro de compras
    c = conn.cursor()
    c.execute("""
        INSERT INTO libro_compras 
        (fecha, tipo_documento, numero_documento, rut_proveedor, razon_social, neto, iva, total, exenta, numero_comprobante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("2025-01-05", "Factura", "1234", "76.123.456-7", "Comercial XYZ Ltda", neto_compra, iva_compra, total_compra, 0, numero_comp_compra))
    conn.commit()
    
    # 4. Venta de mercaderías (con IVA)
    neto_venta = 15000000
    iva_venta = neto_venta * IVA_RATE
    total_venta = neto_venta + iva_venta
    
    print("4. Venta de mercaderías...")
    numero_comp_venta = crear_asiento(
        conn,
        "2025-01-10",
        "Venta mercaderías según Factura N°0001 - Cliente ABC S.A.",
        [
            (11101, total_venta, 0),      # Clientes DEBE
            (41001, 0, neto_venta),       # Ventas HABER
            (21101, 0, iva_venta),        # IVA DF HABER
        ]
    )
    
    # Registrar en libro de ventas
    c.execute("""
        INSERT INTO libro_ventas 
        (fecha, tipo_documento, numero_documento, rut_cliente, razon_social, neto, iva, total, numero_comprobante)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("2025-01-10", "Factura", "0001", "77.234.567-8", "Empresa ABC S.A.", neto_venta, iva_venta, total_venta, numero_comp_venta))
    conn.commit()
    
    # 5. Costo de la venta
    costo_ventas = 7000000
    print("5. Reconocimiento costo de ventas...")
    crear_asiento(
        conn,
        "2025-01-10",
        "Costo de mercaderías vendidas",
        [
            (51001, costo_ventas, 0),     # Costo de Ventas DEBE
            (11301, 0, costo_ventas),     # Mercaderías HABER
        ]
    )
    
    # 6. Pago a proveedor (50% de la deuda)
    pago_proveedor = total_compra * 0.5
    print("6. Pago a proveedor...")
    crear_asiento(
        conn,
        "2025-01-15",
        "Pago 50% Factura N°1234 con transferencia bancaria",
        [
            (21001, pago_proveedor, 0),   # Proveedores DEBE
            (11002, 0, pago_proveedor),   # Banco HABER
        ]
    )
    
    # 7. Cobro a cliente (100%)
    print("7. Cobro a cliente...")
    crear_asiento(
        conn,
        "2025-01-18",
        "Cobro total Factura N°0001 depósito en banco",
        [
            (11002, total_venta, 0),      # Banco DEBE
            (11101, 0, total_venta),      # Clientes HABER
        ]
    )
    
    # 8. Pago de remuneraciones
    remuneraciones = 2500000
    print("8. Pago de remuneraciones...")
    crear_asiento(
        conn,
        "2025-01-25",
        "Pago remuneraciones mes de enero",
        [
            (61001, remuneraciones, 0),   # Remuneraciones DEBE
            (11002, 0, remuneraciones),   # Banco HABER
        ]
    )
    
    # 9. Pago arriendo
    arriendo = 800000
    print("9. Pago arriendo oficina...")
    crear_asiento(
        conn,
        "2025-01-26",
        "Pago arriendo mes enero",
        [
            (61003, arriendo, 0),         # Arriendos DEBE
            (11002, 0, arriendo),         # Banco HABER
        ]
    )
    
    # 10. Gastos servicios básicos
    servicios = 250000
    print("10. Pago servicios básicos...")
    crear_asiento(
        conn,
        "2025-01-27",
        "Pago luz, agua y gas",
        [
            (61004, servicios, 0),        # Servicios DEBE
            (11001, 0, servicios),        # Caja HABER
        ]
    )
    
    # 11. Gastos de publicidad
    publicidad = 1200000
    print("11. Pago publicidad...")
    crear_asiento(
        conn,
        "2025-01-28",
        "Pago campaña publicitaria enero",
        [
            (61101, publicidad, 0),       # Publicidad DEBE
            (11002, 0, publicidad),       # Banco HABER
        ]
    )
    
    # 12. Liquidación IVA (pago al fisco)
    # IVA por pagar = IVA Débito - IVA Crédito
    iva_a_pagar = iva_venta - iva_compra
    if iva_a_pagar > 0:
        print("12. Liquidación IVA...")
        crear_asiento(
            conn,
            "2025-01-31",
            "Determinación IVA a pagar período enero",
            [
                (21101, iva_venta, 0),        # IVA DF DEBE (cierre)
                (11201, 0, iva_compra),       # IVA CF HABER (cierre)
                (21102, 0, iva_a_pagar),      # IVA por Pagar HABER (resultado)
            ]
        )
    
    conn.close()
    print("\n✓ Todas las transacciones creadas exitosamente\n")

def verificar_balance():
    """Verifica que la ecuación contable se cumpla"""
    from models.reportes import ReportesModel
    
    print("=== VERIFICACIÓN DEL BALANCE ===\n")
    
    model = ReportesModel()
    
    # Obtener saldos
    cuentas = model.get_estado_situacion_financiera()
    resultados = model.calcular_utilidad_impuesto()
    
    total_activo = 0
    total_pasivo = 0
    total_patrimonio = 0
    
    for codigo, nombre, elemento, categoria, debe, haber in cuentas:
        if elemento == 'Activo':
            saldo = debe - haber
            total_activo += saldo
        elif elemento == 'Pasivo':
            saldo = haber - debe
            total_pasivo += saldo
        elif elemento == 'Patrimonio':
            saldo = haber - debe
            total_patrimonio += saldo
    
    # Agregar utilidad del ejercicio al patrimonio
    utilidad = resultados['utilidad_ejercicio']
    impuesto = resultados['impuesto']
    
    total_patrimonio_final = total_patrimonio + utilidad
    total_pasivo_final = total_pasivo + impuesto
    total_pasivo_patrimonio = total_pasivo_final + total_patrimonio_final
    
    print(f"ACTIVO TOTAL:                     ${total_activo:,.0f}")
    print(f"PASIVO TOTAL (con impuesto):      ${total_pasivo_final:,.0f}")
    print(f"PATRIMONIO TOTAL (con utilidad):  ${total_patrimonio_final:,.0f}")
    print(f"PASIVO + PATRIMONIO:              ${total_pasivo_patrimonio:,.0f}")
    print()
    
    diferencia = abs(total_activo - total_pasivo_patrimonio)
    
    if diferencia < 1:  # Tolerancia de $1 por redondeo
        print("✓✓✓ BALANCE CUADRADO - La ecuación contable se cumple ✓✓✓")
        print("    ACTIVO = PASIVO + PATRIMONIO")
        return True
    else:
        print(f"✗✗✗ BALANCE DESCUADRADO - Diferencia: ${diferencia:,.0f} ✗✗✗")
        return False

def verificar_debe_haber():
    """Verifica que en todos los comprobantes Debe = Haber"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    print("\n=== VERIFICACIÓN DEBE = HABER ===\n")
    
    c.execute("SELECT DISTINCT numero_comprobante FROM detalle_comprobantes")
    comprobantes = c.fetchall()
    
    descuadres = []
    
    for (num_comp,) in comprobantes:
        c.execute("""
            SELECT SUM(debe), SUM(haber) 
            FROM detalle_comprobantes 
            WHERE numero_comprobante = ?
        """, (num_comp,))
        
        debe, haber = c.fetchone()
        diferencia = abs(debe - haber)
        
        if diferencia > 0.01:
            descuadres.append((num_comp, debe, haber, diferencia))
    
    if not descuadres:
        print(f"✓ Todos los {len(comprobantes)} comprobantes están cuadrados (Debe = Haber)")
    else:
        print(f"✗ Se encontraron {len(descuadres)} comprobantes descuadrados:")
        for num, debe, haber, dif in descuadres:
            print(f"  Comprobante {num}: Debe=${debe:,.0f} | Haber=${haber:,.0f} | Dif=${dif:,.0f}")
    
    conn.close()
    return len(descuadres) == 0

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  GENERADOR DE DATOS DE PRUEBA - SISTEMA CONTABLE")
    print("  Normativa: Contabilidad Chilena + NIIF")
    print("="*60 + "\n")
    
    try:
        # 1. Limpiar datos anteriores
        limpiar_datos()
        
        # 2. Insertar plan de cuentas
        insertar_plan_cuentas()
        
        # 3. Insertar transacciones
        insertar_transacciones_ejemplo()
        
        # 4. Verificar cuadre Debe/Haber
        debe_haber_ok = verificar_debe_haber()
        
        # 5. Verificar balance
        balance_ok = verificar_balance()
        
        print("\n" + "="*60)
        if debe_haber_ok and balance_ok:
            print("  ✓✓✓ SISTEMA VALIDADO CORRECTAMENTE ✓✓✓")
            print("  El sistema cumple con los principios contables")
        else:
            print("  ✗✗✗ SE ENCONTRARON ERRORES ✗✗✗")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
