#!/usr/bin/env python3
"""
Script de prueba para verificar que la BD funciona correctamente
Ejecutar desde cmd: python test_db_fix.py
"""
import os
import sys
import time
import sqlite3

# Eliminar BD existentes (sin estar en el mismo proceso)
db_file = "contabilidad.db"
print("=" * 60)
print("LIMPIANDO BASE DE DATOS ANTERIOR")
print("=" * 60)

for ext in ["", "-shm", "-wal"]:
    path = db_file + ext
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"✓ Eliminado: {path}")
        except Exception as e:
            print(f"✗ No se pudo eliminar {path}: {e}")

time.sleep(1)

# Ahora importar y probar
print("\n" + "=" * 60)
print("INICIALIZANDO BASE DE DATOS")
print("=" * 60)

try:
    from database.db_manager import init_db
    from database.queries import execute_query, fetch_all
    
    init_db()
    print("✓ BD inicializada correctamente\n")
    
except Exception as e:
    print(f"✗ Error al inicializar BD: {e}")
    sys.exit(1)

# Test 1: Insertar primer código
print("=" * 60)
print("TEST 1: INSERTAR PRIMER CÓDIGO")
print("=" * 60)
try:
    query = "INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) VALUES (?, ?, ?, ?, ?, ?)"
    execute_query(query, ("1.01.01.0001", "Efectivo", "Activos", "", "Activos Corrientes", "Efectivo y equivalentes"))
    print("✓ Inserción 1 exitosa\n")
except Exception as e:
    print(f"✗ Error en inserción 1: {e}\n")
    sys.exit(1)

# Test 2: Insertar segundo código
print("=" * 60)
print("TEST 2: INSERTAR SEGUNDO CÓDIGO")
print("=" * 60)
try:
    query = "INSERT INTO plan_cuentas (codigo, nombre, elemento, categoria, subcategoria, grupo) VALUES (?, ?, ?, ?, ?, ?)"
    execute_query(query, ("1.01.02.0001", "Bancos", "Activos", "", "Activos Corrientes", "Otros activos financieros"))
    print("✓ Inserción 2 exitosa\n")
except Exception as e:
    print(f"✗ Error en inserción 2: {e}\n")
    sys.exit(1)

# Test 3: Verificar datos
print("=" * 60)
print("TEST 3: VERIFICAR DATOS")
print("=" * 60)
try:
    resultados = fetch_all("SELECT codigo, nombre FROM plan_cuentas ORDER BY codigo")
    print(f"Total registros: {len(resultados)}")
    for row in resultados:
        print(f"  {row[0]}: {row[1]}")
    
    if len(resultados) == 2:
        print("\n✓✓✓ TODAS LAS PRUEBAS PASARON ✓✓✓\n")
        sys.exit(0)
    else:
        print(f"\n✗ Se esperaban 2 registros, se encontraron {len(resultados)}\n")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error en lectura: {e}\n")
    sys.exit(1)
