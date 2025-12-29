# EJEMPLO DE SALIDA: ARCHIVO EXCEL GENERADO

## Estructura Visual del Archivo

### HOJA 1: RESUMEN EVALUACIÓN
```
════════════════════════════════════════════════════════════
                REPORTE DE EVALUACIÓN CONTABLE
════════════════════════════════════════════════════════════

Fecha de Generación:              22/12/2025 14:30
Sistema:                          Sistema Contable Educativo

────────────────────────────────────────────────────────────
ESTADÍSTICAS GENERALES
────────────────────────────────────────────────────────────
Cuentas en Plan de Cuentas:       32
Comprobantes Registrados:         0
Asientos Contables:               0

────────────────────────────────────────────────────────────
VALIDACIÓN DE INTEGRIDAD
────────────────────────────────────────────────────────────
Total Débitos:                    0.00
Total Créditos:                   0.00
Estado de Cuadre:                 CUADRADO
════════════════════════════════════════════════════════════
```

**Propósito**: Profesor obtiene visión rápida del trabajo

---

### HOJA 2: PLAN DE CUENTAS

```
┌──────────┬──────────────────────┬─────────────┬────────────┬──────────────┬──────────┐
│ Código   │ Nombre               │ Elemento    │ Categoría  │ Subcategoría │ Grupo    │
├──────────┼──────────────────────┼─────────────┼────────────┼──────────────┼──────────┤
│ 11001    │ Caja                 │ Activo      │ Activo...  │ Disponible   │ Efectivo │
│ 11002    │ Banco                │ Activo      │ Activo...  │ Disponible   │ Bancos   │
│ 11003    │ Depósitos a Plazo    │ Activo      │ Activo...  │ Disponible   │ Inversi..│
│ 11004    │ Clientes             │ Activo      │ Activo...  │ Exigible     │ Deudores │
│ ...      │ ...                  │ ...         │ ...        │ ...          │ ...      │
│ 60004    │ Costos Financieros   │ Gasto       │ Gastos No..│ Financieros  │ Gastos   │
├──────────┼──────────────────────┼─────────────┼────────────┼──────────────┼──────────┤
│ Total de Cuentas: 32                                                              │
└──────────────────────────────────────────────────────────────────────────────────┘
```

**Propósito**: Evaluar estructura y clasificación contable

---

### HOJA 3: COMPROBANTES

```
┌────┬────────────┬──────────────┬───────┬────────────────────┬──────────┬──────────┐
│ Nº │ Fecha      │ Glosa        │ Código│ Nombre Cuenta      │ Debe     │ Haber    │
├────┼────────────┼──────────────┼───────┼────────────────────┼──────────┼──────────┤
│ 1  │ 01/12/2025 │ Dep. Inicial │ 11001│ Caja               │ 50000.00 │          │
│    │            │              │ 30001│ Capital Aportado   │          │ 50000.00 │
│ 2  │ 05/12/2025 │ Compra inv.  │ 11006│ Inventarios        │ 25000.00 │          │
│    │            │              │ 11001│ Caja               │          │ 25000.00 │
│ 3  │ 10/12/2025 │ Venta        │ 11001│ Caja               │ 35000.00 │          │
│    │            │              │ 40001│ Ingresos por Vtas  │          │ 35000.00 │
├────┼────────────┼──────────────┼───────┼────────────────────┼──────────┼──────────┤
│ TOTAL                                                        │110000.00 │110000.00 │
├────┼────────────────────────────────────────────────────────┼──────────┼──────────┤
│ Cuadre (Debe=Haber)        ✓ CUADRA                                               │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Propósito**: Detalle completo de cada asiento

---

### HOJA 4: LIBRO DIARIO

```
┌────────────┬────┬────────┬──────────────────────┬──────────┬──────────┬──────────────┐
│ Fecha      │ Nº │ Código │ Cuenta               │ Debe     │ Haber    │ Glosa        │
├────────────┼────┼────────┼──────────────────────┼──────────┼──────────┼──────────────┤
│ 01/12/2025 │ 1  │ 11001  │ Caja                 │ 50000.00 │          │ Dep. Inicial │
│            │    │ 30001  │ Capital Aportado     │          │ 50000.00 │              │
│ 05/12/2025 │ 2  │ 11006  │ Inventarios          │ 25000.00 │          │ Compra inv.  │
│            │    │ 11001  │ Caja                 │          │ 25000.00 │              │
│ 10/12/2025 │ 3  │ 11001  │ Caja                 │ 35000.00 │          │ Venta        │
│            │    │ 40001  │ Ingresos por Vtas    │          │ 35000.00 │              │
├────────────┼────┼────────┼──────────────────────┼──────────┼──────────┼──────────────┤
│ TOTALES                                         │110000.00 │110000.00 │              │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Propósito**: Visualizar movimientos cronológicamente

---

### HOJA 5: BALANCE DE COMPROBACIÓN

```
┌─────────┬───────────────────────────┬──────────┬──────────┬──────────────┬──────────────┐
│ Código  │ Cuenta                    │ Debe     │ Haber    │ Sdo Deudor   │ Sdo Acreedor │
├─────────┼───────────────────────────┼──────────┼──────────┼──────────────┼──────────────┤
│ 11001   │ Caja                      │ 110000.0 │          │ 110000.00    │              │
│ 11006   │ Inventarios               │ 25000.00 │          │ 25000.00     │              │
│ 30001   │ Capital Aportado          │          │ 50000.00 │              │ 50000.00     │
│ 40001   │ Ingresos por Ventas       │          │ 35000.00 │              │ 35000.00     │
├─────────┼───────────────────────────┼──────────┼──────────┼──────────────┼──────────────┤
│ TOTALES                             │110000.00 │110000.00 │ 135000.00    │ 85000.00     │
├─────────┼───────────────────────────┼──────────┼──────────┼──────────────┼──────────────┤
│ Validación                 ✓ BALANCE CUADRA                                           │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

**Propósito**: Validar ecuación fundamental de contabilidad

---

### HOJA 6: ESTADO DE SITUACIÓN FINANCIERA

```
════════════════════════════════════════════════════════════
          ESTADO DE SITUACIÓN FINANCIERA
════════════════════════════════════════════════════════════

ACTIVO
──────────────────────────────────
  Caja                      110000.00
  Inventarios                25000.00
  ───────────────────────────────
  Total Activo               135000.00

PASIVO
──────────────────────────────────
  (Sin pasivos registrados)
  ───────────────────────────────
  Total Pasivo                    0.00

PATRIMONIO
──────────────────────────────────
  Capital Aportado            50000.00
  Resultado Ejercicio         85000.00
  ───────────────────────────────
  Total Patrimonio            85000.00

════════════════════════════════════════════════════════════
VALIDACIÓN: Activo 135000.00 = Pasivo 0.00 + Patrimonio 85000.00
════════════════════════════════════════════════════════════
```

**Propósito**: Resumen de posición financiera

---

### HOJA 7: ESTADO DE RESULTADOS

```
════════════════════════════════════════════════════════════
            ESTADO DE RESULTADOS
════════════════════════════════════════════════════════════

INGRESOS
──────────────────────────────────
  Ingresos por Ventas         35000.00
  ───────────────────────────────
  Total Ingresos              35000.00

COSTOS
──────────────────────────────────
  (Sin costos directos)
  ───────────────────────────────
  Total Costos                    0.00

GASTOS
──────────────────────────────────
  (Sin gastos)
  ───────────────────────────────
  Total Gastos                    0.00

════════════════════════════════════════════════════════════
RESULTADO NETO (Utilidad/Pérdida)         35000.00
════════════════════════════════════════════════════════════
```

**Propósito**: Resultado económico del período

---

## Características de Presentación

### Elementos Visuales
- ✓ **Encabezados azules** → Fácil identificación
- ✓ **Totales sombreados** → Distinción clara
- ✓ **Bordes definidos** → Separación de datos
- ✓ **Números alineados derecha** → Fácil lectura
- ✓ **Formato moneda** → Estándar contable

### Datos Automáticos
- ✓ **Fórmulas de suma** → No requieren recalcular
- ✓ **Validaciones** → Indican si cuadra
- ✓ **Totales dinámicos** → Se actualizan automáticamente

---

## Cómo Interpretar los Datos

### Indicador "CUADRA"
Significa que la ecuación fundamental se cumple:
- En Balance: **Débitos = Créditos**
- En Estado de Situación: **Activo = Pasivo + Patrimonio**

### Indicador "NO CUADRA"
Significa que hay inconsistencias que deben revisarse

### Ceros
- Cuenta sin movimiento
- Sección sin registros
- Completamente normal

### Datos Negativos
Pueden ocurrir si hay errores en el registro. Revisar.

---

## Casos de Uso Reales

### Caso 1: Evaluación Rápida
Profesor abre el archivo y ve inmediatamente:
- Cantidad de trabajos = cantidad de comprobantes
- Si está correcto = estado "CUADRA"
- Calidad de datos = claridad de datos

**Tiempo**: 2-3 minutos por alumno

### Caso 2: Revisión Detallada
Profesor revisa:
1. Plan de Cuentas (¿está bien estructurado?)
2. Comprobantes (¿los asientos tienen sentido?)
3. Balance (¿cuadra perfectamente?)
4. Estados (¿reflejan la realidad?)

**Tiempo**: 10-15 minutos por alumno

### Caso 3: Retroalimentación Documentada
Profesor puede:
- Anotaciones directas en Excel
- Sugerencias de correcciones
- Feedback visual junto a datos

**Tiempo**: 15-20 minutos por alumno

---

## Exportación Exitosa: Checklist

- ✓ Archivo generado sin errores
- ✓ Todas 7 hojas presentes
- ✓ Datos completos y legibles
- ✓ Formato profesional
- ✓ Fórmulas funcionando
- ✓ Tamaño razonable (~15 KB)
- ✓ Compatible con Excel/Sheets
- ✓ Listo para evaluación

---

**Ejemplo generado**: 22/12/2025  
**Versión del Sistema**: 1.0  
**Archivo de prueba**: PRUEBA_Evaluacion_Contable.xlsx
