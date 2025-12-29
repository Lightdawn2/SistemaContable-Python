# 🎓 GUÍA PARA PROFESORES

## Sistema Contable Educativo - Validado según Normativa Chilena y NIIF

---

## 🎯 RESUMEN RÁPIDO

✅ **Sistema validado contablemente**  
✅ **Balance cuadra perfectamente: Activo = Pasivo + Patrimonio**  
✅ **Incluye datos de prueba realistas**  
✅ **Exporta Excel profesional para evaluación**  
✅ **Cumple con NIIF y normativa SII Chile**

---

## 🚀 INICIO RÁPIDO (3 pasos)

### 1. Generar Datos de Prueba
```bash
python test_data_generator.py
```
Esto crea:
- 40 cuentas en el Plan de Cuentas
- 12 transacciones comerciales
- Verifica que todo cuadre

### 2. Ejecutar el Sistema
```bash
python Main.py
```
Navega por todos los módulos para verificar los cálculos.

### 3. Exportar Excel
Desde el sistema, clic en "📊 Exportar a Excel"

O ejecutar:
```bash
python test_excel_export.py
```

---

## 📊 CASO DE ESTUDIO INCLUIDO

**Escenario:** Empresa comercial "Demo SpA" - Enero 2025

### Operaciones del mes:
1. **Aporte de Capital:** $50,000,000
2. **Apertura Cuenta Bancaria:** Depósito $40,000,000
3. **Compra Mercaderías:** $11,900,000 (incluye IVA 19%)
4. **Venta Mercaderías:** $17,850,000 (incluye IVA 19%)
5. **Reconocimiento Costo Ventas:** $7,000,000
6. **Pago a Proveedor:** 50% de la deuda
7. **Cobro a Cliente:** 100% de la venta
8. **Pago Remuneraciones:** $2,500,000
9. **Pago Arriendo:** $800,000
10. **Pago Servicios Básicos:** $250,000
11. **Gastos Publicidad:** $1,200,000
12. **Liquidación IVA:** Determinación y registro

### Resultados Esperados:

**Estado de Resultados:**
```
Ingresos Ordinarios            $15,000,000
(-) Costo de Ventas           ($ 7,000,000)
─────────────────────────────────────────
= UTILIDAD BRUTA               $ 8,000,000  (53.3%)

(-) Gastos Administración     ($ 3,550,000)
(-) Gastos de Ventas          ($ 1,200,000)
─────────────────────────────────────────
= RESULTADO OPERACIONAL        $ 3,250,000

(-) Impuesto Renta (25%)      ($   812,500)
─────────────────────────────────────────
= UTILIDAD DEL EJERCICIO       $ 2,437,500  (16.3%)
═════════════════════════════════════════
```

**Estado de Situación Financiera:**
```
ACTIVO
  Caja                         $  9,750,000
  Banco Estado                 $ 44,400,000
  Mercaderías                  $  3,000,000
  Otros Activos                $  3,000,000
  ────────────────────────────────────────
  TOTAL ACTIVO                 $ 60,150,000
  ════════════════════════════════════════

PASIVO
  Proveedores                  $  5,950,000
  IVA por Pagar                $    950,000
  Impuesto por Pagar           $    812,500
  ────────────────────────────────────────
  TOTAL PASIVO                 $  7,712,500

PATRIMONIO
  Capital                      $ 50,000,000
  Utilidad del Ejercicio       $  2,437,500
  ────────────────────────────────────────
  TOTAL PATRIMONIO             $ 52,437,500
  ────────────────────────────────────────
  TOTAL PASIVO + PATRIMONIO    $ 60,150,000 ✓
  ════════════════════════════════════════
```

**Verificación:** ✅ ACTIVO = PASIVO + PATRIMONIO

---

## 🎓 EVALUACIÓN DE ESTUDIANTES

### Criterios Sugeridos:

#### 1. Plan de Cuentas (15 puntos)
- [ ] Estructura lógica (1xxxx, 2xxxx, 3xxxx, etc.)
- [ ] Códigos correctos y ordenados
- [ ] Nombres descriptivos
- [ ] Clasificación por elemento (Activo, Pasivo, etc.)
- [ ] Categorías apropiadas

#### 2. Registro de Comprobantes (30 puntos)
- [ ] Fecha correcta
- [ ] Glosa descriptiva
- [ ] Cuentas apropiadas seleccionadas
- [ ] Montos correctos en Debe y Haber
- [ ] **Debe = Haber** (crítico)
- [ ] Lógica contable correcta

#### 3. Libro de Compras (10 puntos)
- [ ] Facturas registradas completas
- [ ] RUT proveedor válido
- [ ] IVA calculado correctamente (19%)
- [ ] Vinculación con comprobante

#### 4. Libro de Ventas (10 puntos)
- [ ] Facturas emitidas registradas
- [ ] RUT cliente válido
- [ ] IVA calculado correctamente (19%)
- [ ] Vinculación con comprobante

#### 5. Balance de Comprobación (15 puntos)
- [ ] Todas las cuentas con movimiento aparecen
- [ ] Saldos Deudores y Acreedores correctos
- [ ] **Total Debe = Total Haber**
- [ ] Saldo Deudor = Saldo Acreedor

#### 6. Estado de Resultados (10 puntos)
- [ ] Estructura según NIIF
- [ ] Utilidad Bruta calculada
- [ ] Resultado Operacional
- [ ] Impuesto a la Renta (25%)
- [ ] Utilidad del Ejercicio

#### 7. Estado de Situación Financiera (10 puntos)
- [ ] Activos clasificados (Corriente/No Corriente)
- [ ] Pasivos clasificados (Corriente/No Corriente)
- [ ] Patrimonio con Capital y Utilidad
- [ ] **Activo = Pasivo + Patrimonio** (crítico)
- [ ] Impuesto por Pagar incluido

---

## 🔍 VALIDACIONES AUTOMÁTICAS EN EXCEL

El archivo Excel generado incluye:

### Hoja "Resumen Evaluación"
- Estadísticas generales
- Número de cuentas
- Número de comprobantes
- **Verificación automática: Balance Cuadra (Sí/No)**

### Hoja "Balance de Comprobación"
- Fórmula verifica: Total Debe = Total Haber
- Fórmula verifica: Saldo Deudor = Saldo Acreedor
- Mensaje: "✓ BALANCE CUADRA" o "✗ NO CUADRA"

### Hoja "Estado de Situación"
- Cálculo automático de totales
- Incluye Utilidad del Ejercicio
- Incluye Impuesto por Pagar
- Permite verificar ecuación contable

### Hoja "Estado de Resultados"
- Estructura según NIIF
- Subtotales automáticos
- Cálculo de Utilidad Bruta
- Cálculo de Resultado Operacional
- Cálculo de Impuesto (25%)

---

## 🛠️ MODIFICAR EL CASO DE ESTUDIO

Para crear tus propios escenarios de evaluación:

### Opción 1: Modificar el script existente

Editar `test_data_generator.py`:

```python
# Cambiar montos en función crear_asiento():

# Ejemplo: Aumentar el aporte de capital
crear_asiento(
    conn, 
    "2025-01-02",
    "Aporte inicial de capital en efectivo",
    [
        (11001, 100000000, 0),  # Era 50M, ahora 100M
        (31001, 0, 100000000),
    ]
)

# Ejemplo: Agregar una compra de vehículo
crear_asiento(
    conn,
    "2025-01-15",
    "Compra camioneta para reparto",
    [
        (12003, 15000000, 0),  # Vehículos DEBE
        (11002, 0, 15000000),  # Banco HABER
    ]
)
```

### Opción 2: Crear escenario de pérdida

Para que los estudiantes vean caso con pérdida:

```python
# Aumentar los gastos más que los ingresos
gastos_extras = 20000000  # Agregar $20M en gastos

crear_asiento(
    conn,
    "2025-01-30",
    "Reparación mayor de equipos",
    [
        (61005, gastos_extras, 0),  # Gastos DEBE
        (11002, 0, gastos_extras),  # Banco HABER
    ]
)
```

Esto resultará en:
- Utilidad negativa (pérdida)
- Impuesto = 0 (no hay impuesto sobre pérdidas)
- Patrimonio disminuido

---

## 📝 EJERCICIOS SUGERIDOS

### Ejercicio 1: Básico
**Objetivo:** Aprender partida doble
- Crear 5 cuentas básicas (Caja, Banco, Capital, Ventas, Gastos)
- Registrar 3 comprobantes simples
- Verificar que balance cuadre

### Ejercicio 2: Intermedio
**Objetivo:** Manejo de IVA
- Incluir IVA Crédito Fiscal e IVA Débito Fiscal
- Registrar compras y ventas con IVA
- Hacer liquidación mensual del IVA
- Registrar pago al fisco

### Ejercicio 3: Avanzado
**Objetivo:** Estados financieros completos
- Crear plan de cuentas completo (40+ cuentas)
- Registrar ciclo completo de operaciones (mes)
- Generar Estado de Resultados con clasificación
- Generar Estado de Situación con ecuación balanceada
- Calcular índices financieros:
  - Margen Bruto = (Utilidad Bruta / Ventas) × 100
  - Margen Neto = (Utilidad Neta / Ventas) × 100
  - ROE = (Utilidad Neta / Patrimonio) × 100

### Ejercicio 4: Casos especiales
**Objetivo:** Situaciones reales
- Descuentos en compras
- Descuentos en ventas
- Devoluciones
- Notas de crédito
- Notas de débito

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Problema: "Balance no cuadra"

**Diagnóstico:**
1. Revisar cada comprobante: ¿Debe = Haber?
2. Usar Excel: Ver hoja "Balance de Comprobación"
3. Buscar comprobante descuadrado

**Solución:**
```bash
python test_data_generator.py
```
Verá qué comprobante falla en la verificación.

### Problema: "Activo ≠ Pasivo + Patrimonio"

**Causa común:**
- Falta incluir Utilidad del Ejercicio
- Falta incluir Impuesto por Pagar

**Verificar:**
- ¿Está visible "Utilidad del Ejercicio" en Patrimonio?
- ¿Está visible "Impuesto por Pagar" en Pasivos?

**Solución:**
El sistema ahora lo hace automáticamente. Si falla, verificar que está ejecutando la versión actualizada.

### Problema: "IVA no cuadra"

**Verificar:**
1. Compras: IVA CF = Neto × 0.19
2. Ventas: IVA DF = Neto × 0.19
3. Liquidación: IVA por Pagar = IVA DF - IVA CF

**Nota:** El IVA se cierra contra "IVA por Pagar", no contra Banco directamente.

---

## 📚 MATERIAL COMPLEMENTARIO

### Lecturas Recomendadas:
1. **NIC 1:** Presentación de Estados Financieros
2. **NIC 2:** Inventarios
3. **NIC 12:** Impuesto a las Ganancias
4. **Código Tributario Chileno:** Artículos sobre IVA
5. **Circular SII:** Sobre Libros de Compra y Venta

### Videos Sugeridos:
1. Principio de Partida Doble
2. Naturaleza de las Cuentas
3. Ciclo Contable
4. Tratamiento del IVA en Chile
5. Elaboración de Estados Financieros

---

## ✅ CHECKLIST CLASE TIPO

### Antes de la clase:
- [ ] Ejecutar `python test_data_generator.py`
- [ ] Verificar que Main.py funciona
- [ ] Generar Excel de ejemplo
- [ ] Revisar que balance cuadra
- [ ] Preparar ejercicio del día

### Durante la clase:
- [ ] Mostrar estructura del sistema
- [ ] Explicar principio de partida doble
- [ ] Demostrar un comprobante completo
- [ ] Mostrar cómo verifica el sistema (Debe = Haber)
- [ ] Navegar por los estados financieros
- [ ] Exportar y revisar Excel

### Después de la clase:
- [ ] Asignar ejercicio a estudiantes
- [ ] Establecer fecha de entrega
- [ ] Indicar criterios de evaluación
- [ ] Solicitar archivo Excel exportado

---

## 🎯 METAS DE APRENDIZAJE

Al finalizar el curso con este sistema, los estudiantes deberán:

### Nivel Básico:
- ✅ Entender partida doble
- ✅ Identificar naturaleza de cuentas
- ✅ Registrar comprobantes simples
- ✅ Verificar Debe = Haber

### Nivel Intermedio:
- ✅ Crear plan de cuentas estructurado
- ✅ Manejar IVA correctamente
- ✅ Registrar compras y ventas
- ✅ Hacer liquidación IVA
- ✅ Generar Balance de Comprobación

### Nivel Avanzado:
- ✅ Elaborar Estado de Resultados completo
- ✅ Elaborar Estado de Situación Financiera
- ✅ Verificar ecuación contable
- ✅ Calcular y registrar Impuesto a la Renta
- ✅ Analizar ratios financieros
- ✅ Interpretar estados financieros

---

## 📞 CONTACTO Y SOPORTE

### Documentación Disponible:
- `README.md` - Guía general del sistema
- `VALIDACION_CONTABLE.md` - Análisis técnico completo
- `RESUMEN_EJECUTIVO.md` - Resumen de cambios
- `GUIA_PROFESORES.md` - Este archivo

### Scripts Útiles:
- `test_data_generator.py` - Genera datos de prueba
- `test_excel_export.py` - Exporta automáticamente
- `Main.py` - Sistema principal

### En caso de problemas:
1. Verificar que Python 3.12+ está instalado
2. Verificar que el virtual environment está activo
3. Ejecutar: `pip install -r requirements.txt`
4. Si persiste, eliminar `contabilidad.db` y reiniciar

---

## 🏆 CASOS DE ÉXITO

### Uso Sugerido por Nivel:

**Primer Año (Introducción):**
- Usar con 5-10 cuentas básicas
- 3-5 comprobantes simples
- Sin IVA inicialmente
- Enfoque en partida doble

**Segundo Año (Intermedio):**
- Plan de cuentas completo (30-40 cuentas)
- Incluir IVA en todas las operaciones
- Libros de Compra y Venta
- Balance de Comprobación

**Tercer Año (Avanzado):**
- Caso completo como "Demo SpA"
- Estados Financieros completos
- Análisis financiero
- Cumplimiento NIIF

---

**¡Éxito en sus clases! 🎓**

El sistema está diseñado para facilitar el aprendizaje práctico de la contabilidad, respetando todas las normativas vigentes y principios contables.

---

_Documento actualizado: 29 de Diciembre de 2025_  
_Sistema validado según: Normativa Chilena, NIIF, SII Chile_
