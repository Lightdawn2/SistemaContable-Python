"""
Script para generar datos de prueba realistas según normativa chilena y NIIF
Este script crea un caso de estudio completo con transacciones que permiten
verificar que el balance cuadre correctamente.

ACTUALIZADO: Usa el nuevo sistema de codificación D.CC.SS.NNNN según accounting.py
- D: Elemento (1=Activos, 2=Pasivos, 3=Patrimonio, 4=Ingresos, 5=Gastos)
- CC: Subcategoría (01-99)
- SS: Subcuenta (01-99)
- NNNN: Secuencial (0001-9999)
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
    Inserta un plan de cuentas según el nuevo sistema de codificación NIIF/IFRS Chile
    Formato de códigos: D.CC.SS.NNNN
    - D: Elemento (1=Activos, 2=Pasivos, 3=Patrimonio, 4=Ingresos, 5=Gastos)
    - CC: Subcategoría (01-99)
    - SS: Subcuenta (01-99)
    - NNNN: Secuencial (0001-9999)
    """
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    cuentas = [
        # ACTIVOS CORRIENTES - 1.01.01.NNNN
        ('1.01.01.0001', 'Caja', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Efectivo y equivalentes al efectivo'),
        ('1.01.01.0002', 'Banco Estado Cta Cte', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Efectivo y equivalentes al efectivo'),
        ('1.01.01.0003', 'Banco Chile Cta Cte', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Efectivo y equivalentes al efectivo'),
        ('1.01.03.0001', 'Clientes', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Deudores comerciales y otras cuentas por cobrar, corrientes'),
        ('1.01.03.0002', 'Documentos por Cobrar', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Deudores comerciales y otras cuentas por cobrar, corrientes'),
        ('1.01.07.0001', 'IVA Crédito Fiscal', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Activos por impuestos, corrientes'),
        ('1.01.05.0001', 'Mercaderías', 'Activos', 'Activos Corrientes', 'Activos Corrientes', 'Inventarios'),
        
        # ACTIVOS NO CORRIENTES - 1.02.07.NNNN (PPE)
        ('1.02.07.0001', 'Terrenos', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0002', 'Edificios', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0003', 'Vehículos', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0004', 'Muebles y Útiles', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0005', 'Equipos Computacionales', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0006', 'Depreciación Acumulada Edificios', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        ('1.02.07.0007', 'Depreciación Acumulada Vehículos', 'Activos', 'Activos No Corrientes', 'Activos No Corrientes', 'Propiedades, Planta y Equipo'),
        
        # PASIVOS CORRIENTES - 2.01.01.NNNN
        ('2.01.02.0001', 'Proveedores', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Cuentas comerciales y otras cuentas por pagar, corrientes'),
        ('2.01.02.0002', 'Documentos por Pagar', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Cuentas comerciales y otras cuentas por pagar, corrientes'),
        ('2.01.04.0001', 'IVA Débito Fiscal', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Pasivos por impuestos, corrientes'),
        ('2.01.04.0002', 'IVA por Pagar', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Pasivos por impuestos, corrientes'),
        ('2.01.01.0001', 'Préstamos Bancarios Corto Plazo', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Otros pasivos financieros, corrientes'),
        ('2.01.05.0001', 'Remuneraciones por Pagar', 'Pasivos', 'Pasivos Corrientes', 'Pasivos Corrientes', 'Provisiones por beneficios a los empleados, corrientes'),
        
        # PASIVOS NO CORRIENTES - 2.02.01.NNNN
        ('2.02.01.0001', 'Préstamos Bancarios Largo Plazo', 'Pasivos', 'Pasivos No Corrientes', 'Pasivos No Corrientes', 'Otros pasivos financieros, no corrientes'),
        ('2.02.03.0001', 'Provisiones Largo Plazo', 'Pasivos', 'Pasivos No Corrientes', 'Pasivos No Corrientes', 'Otras provisiones, no corrientes'),
        
        # PATRIMONIO - 3.01.01.NNNN
        ('3.01.01.0001', 'Capital', 'Patrimonio', 'Patrimonio', 'Patrimonio', 'Capital emitido'),
        ('3.01.06.0001', 'Reservas', 'Patrimonio', 'Patrimonio', 'Patrimonio', 'Otras reservas'),
        ('3.01.02.0001', 'Resultados Acumulados', 'Patrimonio', 'Patrimonio', 'Patrimonio', 'Ganancias o Pérdidas acumuladas'),
        
        # INGRESOS - 4.01.01.NNNN
        ('4.01.01.0001', 'Ventas de Mercaderías', 'Ingresos', 'Ingresos de Actividades Ordinarias', 'Ingresos de Actividades Ordinarias', 'Venta de bienes'),
        ('4.01.02.0001', 'Prestación de Servicios', 'Ingresos', 'Ingresos de Actividades Ordinarias', 'Ingresos de Actividades Ordinarias', 'Prestación de servicios'),
        ('4.01.05.0001', 'Descuentos Otorgados', 'Ingresos', 'Ingresos de Actividades Ordinarias', 'Ingresos de Actividades Ordinarias', 'Otros ingresos de actividades ordinarias'),
        ('4.02.02.0001', 'Intereses Ganados', 'Ingresos', 'Otros Ingresos', 'Otros Ingresos', 'Ingresos financieros'),
        
        # GASTOS - 5.01.01.NNNN (Costo de Ventas)
        ('5.01.01.0001', 'Costo de Ventas', 'Gastos', 'Costo de Ventas', 'Costo de Ventas', 'Costo de bienes vendidos'),
        
        # GASTOS DE ADMINISTRACIÓN - 5.02.01.NNNN
        ('5.02.01.0001', 'Remuneraciones', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Sueldos y salarios'),
        ('5.02.01.0002', 'Honorarios', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Sueldos y salarios'),
        ('5.02.04.0001', 'Arriendos', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Gastos de arrendamiento'),
        ('5.02.05.0001', 'Luz, Agua y Gas', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Gastos de servicios básicos'),
        ('5.02.09.0001', 'Útiles de Oficina', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Otros gastos administrativos'),
        
        # GASTOS DE VENTAS - 5.03.01.NNNN
        ('5.03.01.0001', 'Publicidad y Propaganda', 'Gastos', 'Gastos de Ventas', 'Gastos de Ventas', 'Gastos de publicidad y marketing'),
        ('5.03.02.0001', 'Comisiones de Ventas', 'Gastos', 'Gastos de Ventas', 'Gastos de Ventas', 'Comisiones a vendedores'),
        
        # GASTOS FINANCIEROS - 5.04.01.NNNN
        ('5.04.01.0001', 'Intereses Bancarios', 'Gastos', 'Gastos Financieros', 'Gastos Financieros', 'Gastos por intereses'),
        ('5.04.02.0001', 'Comisiones Bancarias', 'Gastos', 'Gastos Financieros', 'Gastos Financieros', 'Gastos por comisiones'),
        
        # DEPRECIACIÓN
        ('5.02.03.0001', 'Depreciación del Ejercicio', 'Gastos', 'Gastos de Administración', 'Gastos de Administración', 'Gastos de depreciación y amortización'),
    ]
    
    c.executemany(
        "INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) VALUES (?, ?, ?, ?, ?, ?)",
        cuentas
    )
    
    conn.commit()
    conn.close()
    print(f"✓ {len(cuentas)} cuentas insertadas en el Plan de Cuentas (nuevo formato D.CC.SS.NNNN)")

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
    ACTUALIZADO: Usa códigos del nuevo sistema D.CC.SS.NNNN
    """
    conn = sqlite3.connect(DB_FILE)
    
    print("\n=== CREANDO TRANSACCIONES DE PRUEBA (Sistema NIIF/IFRS Chile) ===\n")
    
    # 1. Aporte de capital inicial
    print("1. Aporte de capital...")
    crear_asiento(
        conn, 
        "2025-01-02",
        "Aporte inicial de capital en efectivo",
        [
            ('1.01.01.0001', 50000000, 0),  # Caja DEBE
            ('3.01.01.0001', 0, 50000000),  # Capital HABER
        ]
    )
    
    # 2. Apertura cuenta corriente bancaria
    print("2. Apertura cuenta bancaria...")
    crear_asiento(
        conn,
        "2025-01-02",
        "Depósito en Banco Estado desde caja",
        [
            ('1.01.01.0002', 40000000, 0),  # Banco Estado DEBE
            ('1.01.01.0001', 0, 40000000),  # Caja HABER
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
            ('1.01.05.0001', neto_compra, 0),      # Mercaderías DEBE
            ('1.01.07.0001', iva_compra, 0),       # IVA CF DEBE
            ('2.01.02.0001', 0, total_compra),     # Proveedores HABER
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
            ('1.01.03.0001', total_venta, 0),      # Clientes DEBE
            ('4.01.01.0001', 0, neto_venta),       # Ventas HABER
            ('2.01.04.0001', 0, iva_venta),        # IVA DF HABER
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
            ('5.01.01.0001', costo_ventas, 0),     # Costo de Ventas DEBE
            ('1.01.05.0001', 0, costo_ventas),     # Mercaderías HABER
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
            ('2.01.02.0001', pago_proveedor, 0),   # Proveedores DEBE
            ('1.01.01.0002', 0, pago_proveedor),   # Banco HABER
        ]
    )
    
    # 7. Cobro a cliente (100%)
    print("7. Cobro a cliente...")
    crear_asiento(
        conn,
        "2025-01-18",
        "Cobro total Factura N°0001 depósito en banco",
        [
            ('1.01.01.0002', total_venta, 0),      # Banco DEBE
            ('1.01.03.0001', 0, total_venta),      # Clientes HABER
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
            ('5.02.01.0001', remuneraciones, 0),   # Remuneraciones DEBE
            ('1.01.01.0002', 0, remuneraciones),   # Banco HABER
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
            ('5.02.04.0001', arriendo, 0),         # Arriendos DEBE
            ('1.01.01.0002', 0, arriendo),         # Banco HABER
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
            ('5.02.05.0001', servicios, 0),        # Servicios DEBE
            ('1.01.01.0001', 0, servicios),        # Caja HABER
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
            ('5.03.01.0001', publicidad, 0),       # Publicidad DEBE
            ('1.01.01.0002', 0, publicidad),       # Banco HABER
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
                ('2.01.04.0001', iva_venta, 0),        # IVA DF DEBE (cierre)
                ('1.01.07.0001', 0, iva_compra),       # IVA CF HABER (cierre)
                ('2.01.04.0002', 0, iva_a_pagar),      # IVA por Pagar HABER (resultado)
            ]
        )
    
    conn.close()
    print("\n✓ Todas las transacciones creadas exitosamente con códigos NIIF/IFRS Chile\n")

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
        if elemento == 'Activos':
            saldo = debe - haber
            total_activo += saldo
        elif elemento == 'Pasivos':
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
