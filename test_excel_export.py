"""
Script de prueba rápida para validar exportación a Excel
Ejecuta el sistema con datos de prueba y exporta automáticamente
"""
import os
import sys
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*70)
    print("  PRUEBA RÁPIDA - EXPORTACIÓN EXCEL")
    print("="*70 + "\n")
    
    # 1. Generar datos de prueba
    print("📊 Paso 1: Generando datos de prueba...")
    os.system(f'"{sys.executable}" test_data_generator.py')
    
    # 2. Exportar a Excel
    print("\n📝 Paso 2: Exportando a Excel...")
    from utils.excel_exporter import ExcelExporter
    
    filename = f"Prueba_Contable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    exporter = ExcelExporter()
    
    try:
        # Exportar todas las hojas
        exporter.export_resumen_evaluacion()
        exporter.export_plan_cuentas()
        exporter.export_comprobantes()
        exporter.export_libro_diario()
        exporter.export_balance_comprobacion()
        exporter.export_estado_financiero()
        exporter.export_estado_resultados()
        
        # Guardar archivo
        exporter.save(filename)
        
        print(f"\n✅ Archivo Excel creado exitosamente:")
        print(f"   📄 {os.path.abspath(filename)}")
        print(f"   📦 Tamaño: {os.path.getsize(filename) / 1024:.1f} KB")
        
        # 3. Abrir archivo (opcional)
        print("\n🔍 ¿Deseas abrir el archivo ahora? (s/n): ", end="")
        respuesta = input().strip().lower()
        
        if respuesta == 's':
            if os.name == 'nt':  # Windows
                os.startfile(filename)
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'open "{filename}"' if sys.platform == 'darwin' else f'xdg-open "{filename}"')
            print("✓ Archivo abierto")
        
        # 4. Verificación final
        print("\n" + "="*70)
        print("  ✅ PRUEBA COMPLETADA CON ÉXITO")
        print("="*70)
        print("\n📋 Verifica en el Excel:")
        print("   1. Hoja 'Resumen Evaluación' - Estado general")
        print("   2. Hoja 'Balance de Comprobación' - Debe = Haber")
        print("   3. Hoja 'Estado de Situación' - Activo = Pasivo + Patrimonio")
        print("   4. Hoja 'Estado de Resultados' - Estructura NIIF")
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR al exportar: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
