"""
Script de prueba para verificar los cálculos contables
Verifica que los saldos se calculen correctamente según la naturaleza de cada cuenta
"""
from database.queries import fetch_all

def verificar_calculos():
    """Verifica que los cálculos sean correctos"""
    print("=" * 80)
    print("VERIFICACIÓN DE CÁLCULOS CONTABLES")
    print("=" * 80)
    
    # Obtener todas las cuentas con movimientos
    query = """
        SELECT 
            p.codigo,
            p.nombre,
            p.elemento,
            COALESCE(SUM(d.debe), 0) as total_debe,
            COALESCE(SUM(d.haber), 0) as total_haber
        FROM plan_cuentas p
        LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
        GROUP BY p.codigo, p.nombre, p.elemento
        HAVING (total_debe > 0 OR total_haber > 0)
        ORDER BY p.codigo
    """
    
    cuentas = fetch_all(query)
    
    print("\nCUENTAS CON MOVIMIENTOS:")
    print("-" * 80)
    print(f"{'Código':<10} {'Cuenta':<30} {'Elemento':<12} {'Debe':<15} {'Haber':<15} {'Saldo':<15}")
    print("-" * 80)
    
    total_debe_general = 0
    total_haber_general = 0
    
    for codigo, nombre, elemento, debe, haber in cuentas:
        # Calcular saldo según naturaleza
        if elemento in ['Activo', 'Gasto', 'Costo']:
            # Naturaleza DEUDORA
            saldo = debe - haber
            naturaleza = "DEUDORA"
        else:  # Pasivo, Patrimonio, Ingreso
            # Naturaleza ACREEDORA
            saldo = haber - debe
            naturaleza = "ACREEDORA"
        
        total_debe_general += debe
        total_haber_general += haber
        
        # Mostrar solo si tiene saldo significativo
        if abs(saldo) > 0.01:
            print(f"{codigo:<10} {nombre[:28]:<30} {elemento:<12} ${debe:>12,.0f} ${haber:>12,.0f} ${saldo:>12,.0f}")
    
    print("-" * 80)
    print(f"{'TOTALES':<54} ${total_debe_general:>12,.0f} ${total_haber_general:>12,.0f}")
    print("-" * 80)
    
    diferencia = abs(total_debe_general - total_haber_general)
    if diferencia < 0.01:
        print(f"\n✓ BALANCE CUADRA - Los débitos y créditos están balanceados")
    else:
        print(f"\n✗ BALANCE NO CUADRA - Diferencia: ${diferencia:,.2f}")
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN POR TIPO DE CUENTA:")
    print("=" * 80)
    
    # Verificar por elemento
    elementos = ['Activo', 'Pasivo', 'Patrimonio', 'Ingreso', 'Costo', 'Gasto']
    
    for elemento in elementos:
        query_elemento = """
            SELECT 
                p.codigo,
                p.nombre,
                COALESCE(SUM(d.debe), 0) as total_debe,
                COALESCE(SUM(d.haber), 0) as total_haber
            FROM plan_cuentas p
            LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
            WHERE p.elemento = ?
            GROUP BY p.codigo, p.nombre
            HAVING (total_debe > 0 OR total_haber > 0)
            ORDER BY p.codigo
        """
        
        cuentas_elemento = fetch_all(query_elemento, (elemento,))
        
        if cuentas_elemento:
            print(f"\n{elemento.upper()}:")
            print("-" * 80)
            
            total_elemento = 0
            for codigo, nombre, debe, haber in cuentas_elemento:
                if elemento in ['Activo', 'Gasto', 'Costo']:
                    saldo = debe - haber
                else:
                    saldo = haber - debe
                
                if abs(saldo) > 0.01:
                    print(f"  {codigo:<8} {nombre[:40]:<40} ${saldo:>15,.0f}")
                    total_elemento += saldo
            
            print(f"  {'Total ' + elemento:<50} ${total_elemento:>15,.0f}")
    
    print("\n" + "=" * 80)
    print("VERIFICACIÓN ESPECÍFICA DE CAJA:")
    print("=" * 80)
    
    # Verificar específicamente la cuenta Caja
    query_caja = """
        SELECT 
            p.codigo,
            p.nombre,
            p.elemento,
            COALESCE(SUM(d.debe), 0) as total_debe,
            COALESCE(SUM(d.haber), 0) as total_haber
        FROM plan_cuentas p
        LEFT JOIN detalle_comprobantes d ON p.codigo = d.codigo_cuenta
        WHERE p.nombre LIKE '%Caja%' OR p.codigo = '1011'
        GROUP BY p.codigo, p.nombre, p.elemento
    """
    
    caja = fetch_all(query_caja)
    
    if caja:
        for codigo, nombre, elemento, debe, haber in caja:
            saldo = debe - haber  # Activo = Deudora
            print(f"\nCuenta: {nombre}")
            print(f"Código: {codigo}")
            print(f"Elemento: {elemento}")
            print(f"Naturaleza: DEUDORA (Activo)")
            print(f"Total Débitos:  ${debe:>15,.0f}")
            print(f"Total Créditos: ${haber:>15,.0f}")
            print(f"Saldo (Debe - Haber): ${saldo:>15,.0f}")
            
            if saldo < 0:
                print(f"\n⚠️  ADVERTENCIA: Caja con saldo negativo (${saldo:,.0f})")
                print(f"   Esto podría indicar un error en los asientos contables.")
    else:
        print("\nNo se encontró cuenta de Caja en el sistema.")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    from database import init_db
    init_db()
    verificar_calculos()
