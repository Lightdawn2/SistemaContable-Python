"""
Script para resetear completamente el sistema contable
Elimina todos los datos y deja la base de datos vacía para comenzar de nuevo

USO:
    python reset_system.py
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("\n" + "="*70)
    print("  ⚠️  RESETEAR SISTEMA CONTABLE  ⚠️")
    print("="*70 + "\n")
    
    print("ADVERTENCIA CRÍTICA:")
    print("Esta acción ELIMINARÁ PERMANENTEMENTE:")
    print("  • Todo el Plan de Cuentas")
    print("  • Todos los Comprobantes")
    print("  • Todos los Libros de Compras y Ventas")
    print("  • TODOS los datos del sistema")
    print("\nEl sistema volverá a estar completamente VACÍO.")
    print()
    
    # Confirmación 1
    respuesta1 = input("¿Está SEGURO de que desea continuar? (escriba 'SI' en mayúsculas): ").strip()
    
    if respuesta1 != "SI":
        print("\n✓ Operación cancelada. No se eliminó ningún dato.")
        return 0
    
    # Confirmación 2
    print("\n" + "⚠️ "*20)
    print("ÚLTIMA CONFIRMACIÓN")
    print("Esta acción NO se puede deshacer.")
    respuesta2 = input("Escriba 'ELIMINAR TODO' para confirmar: ").strip()
    
    if respuesta2 != "ELIMINAR TODO":
        print("\n✓ Operación cancelada. No se eliminó ningún dato.")
        return 0
    
    # Proceder con el reseteo
    print("\n Reseteando sistema...")
    
    try:
        from database import reset_database
        
        # Resetear base de datos
        reset_database()
        
        print("\n" + "="*70)
        print("   SISTEMA RESETEADO EXITOSAMENTE")
        print("="*70)
        print("\n El sistema está ahora completamente vacío.")
        print("   Puede comenzar a crear su Plan de Cuentas desde cero.")
        print("\n Sugerencia: Para cargar datos de prueba, ejecute:")
        print("   python test_data_generator.py")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n ERROR al resetear el sistema:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
