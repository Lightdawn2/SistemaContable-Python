# Actualizaciones del Sistema Contable

**Fecha:** 20 de Enero, 2026  
**Versión:** 2.0 - Sistema Educativo con Protección y Exportación Mejorada

---

## 🔐 Sistema de Protección con Contraseña

### Funcionalidad Implementada
Se ha implementado un sistema de protección para los **Libros de Compras** y **Libros de Ventas** con las siguientes características:

#### Contraseña de Acceso
- **Contraseña:** `Contabilidad2026$`
- **Ubicación:** Hardcoded en `views/main_window.py` (línea 20)

#### Comportamiento
1. **Primera Vez:** Al hacer clic en "Libro de Compras" o "Libro de Ventas", aparece un diálogo solicitando contraseña
2. **Desbloqueo Persistente:** Una vez ingresada la contraseña correcta, ambos libros quedan desbloqueados durante toda la sesión
3. **Validación:** Si la contraseña es incorrecta, se muestra un mensaje de error y permite reintentar
4. **Nueva Sesión:** Al cerrar y volver a abrir la aplicación, los libros vuelven a bloquearse

#### Características del Diálogo
- ✅ Ventana modal centrada en pantalla
- ✅ Campo de contraseña con caracteres ocultos (●●●●●)
- ✅ Mensaje informativo sobre el desbloqueo persistente
- ✅ Feedback visual si la contraseña es incorrecta (❌)
- ✅ Tecla Enter para aceptar, Escape para cancelar
- ✅ Mensaje de confirmación cuando se desbloquea exitosamente

#### Beneficios Pedagógicos
- Los estudiantes pueden practicar con **comprobantes manuales** libremente
- El instructor controla **cuándo** dar acceso a los libros automáticos
- No interrumpe el flujo de trabajo (solo pide contraseña una vez por sesión)
- Claro mensaje educativo sobre la restricción de funciones avanzadas

### Archivos Modificados
- `views/main_window.py`:
  - Agregada variable `self.libros_desbloqueados` (línea 18)
  - Agregada constante `self.PASSWORD_LIBROS` (línea 20)
  - Método `solicitar_password()` (líneas 165-255)
  - Modificado `show_libro_compras()` con verificación (líneas 153-163)
  - Modificado `show_libro_ventas()` con verificación (líneas 165-175)

---

## 📊 Exportador de Excel Mejorado

### Actualización a Nuevo Sistema de Códigos

El exportador ahora está completamente actualizado para el sistema de codificación **NIIF/IFRS Chile** con formato `D.CC.SS.NNNN`:

#### Formato de Códigos
- **D:** Elemento (1=Activos, 2=Pasivos, 3=Patrimonio, 4=Ingresos, 5=Gastos)
- **CC:** Categoría (01-99)
- **SS:** Subcuenta (01-99)
- **NNNN:** Secuencial (0001-9999)

#### Nombres de Elementos Actualizados
Todos los nombres de elementos ahora usan **forma plural**:
- ✅ `Activos` (antes: Activo)
- ✅ `Pasivos` (antes: Pasivo)
- ✅ `Patrimonio` (sin cambio)
- ✅ `Ingresos` (antes: Ingreso)
- ✅ `Gastos` (antes: Gasto)
- ✅ `Costos` (antes: Costo)

### Nuevas Funcionalidades del Excel

#### 1. Hoja de Resumen de Evaluación (Primera Hoja)
**Propósito:** Visión rápida del trabajo del alumno para el profesor

**Contenido:**
- ✅ Fecha de generación del reporte
- ✅ Identificación del sistema (NIIF/IFRS Chile)
- ✅ Explicación del formato de códigos

**Estadísticas Generales:**
- Total de cuentas en Plan de Cuentas
- Comprobantes registrados
- Asientos contables totales
- Registros en Libro de Compras
- Registros en Libro de Ventas

**Distribución por Elementos:**
- Desglose de cuentas por cada elemento (Activos, Pasivos, etc.)

**Validación de Integridad Contable:**
- Total Débitos vs Total Créditos
- Diferencia (debe ser 0 o cercano)
- Estado de Cuadre (✓ CUADRADO / ✗ NO CUADRA)

**Validación de Ecuación Contable:**
- Total Activos
- Total Pasivos
- Total Patrimonio (incluye utilidad del ejercicio)
- Validación: Activos = Pasivos + Patrimonio (✓ VÁLIDA / ✗ NO VÁLIDA)

**Instrucciones para el Profesor:**
- Checklist de validaciones a realizar
- Explicación del sistema de códigos
- Criterios de evaluación sugeridos

#### 2. Hoja de Libro de Compras
**Columnas:**
- Fecha, Proveedor, RUT, N° Factura
- Monto Neto, IVA, Total
- N° Comprobante asociado
- Totales calculados automáticamente

#### 3. Hoja de Libro de Ventas
**Columnas:**
- Fecha, Cliente, RUT, N° Factura
- Monto Neto, IVA, Total
- N° Comprobante asociado
- Totales calculados automáticamente

#### 4. Hojas Actualizadas

**Plan de Cuentas:**
- Códigos mostrados como texto (no números)
- Formato D.CC.SS.NNNN preservado

**Comprobantes:**
- Códigos de cuentas como texto
- Validación automática de Debe = Haber

**Libro Diario:**
- Códigos como texto
- Ordenado por fecha

**Balance de Comprobación:**
- Usa nombres plurales de elementos
- Clasifica correctamente según naturaleza:
  - Deudoras: Activos, Gastos, Costos
  - Acreedoras: Pasivos, Patrimonio, Ingresos

**Estado de Situación Financiera:**
- Elementos: Activos, Pasivos, Patrimonio
- Cálculos según naturaleza correcta
- Incluye Impuesto por Pagar calculado
- Incluye Utilidad del Ejercicio

**Estado de Resultados:**
- Elementos: Ingresos, Costos, Gastos
- Clasificación por categorías:
  - Costo de Ventas
  - Gastos de Administración
  - Gastos de Ventas
  - Gastos Financieros
- Cálculo de impuesto (25%)
- Resultado final: Ganancia/Pérdida del Ejercicio

### Orden de Hojas en el Excel

1. **Resumen Evaluación** ← Inicio aquí para profesores
2. Plan de Cuentas
3. Comprobantes
4. Libro Diario
5. Libro de Compras
6. Libro de Ventas
7. Balance de Comprobación
8. Estado de Situación
9. Estado de Resultados

### Archivos Modificados
- `utils/excel_exporter.py`:
  - Actualizado formato de códigos (líneas 101-108, 151-158, 216-223)
  - Actualizado nombres de elementos de singular a plural (líneas 288-296, 454-461, 571-583, 632-645, 667-680, 715-728)
  - Mejorada hoja de Resumen de Evaluación (líneas 335-489)
  - Agregado método `export_libro_compras()` (líneas 900-950)
  - Agregado método `export_libro_ventas()` (líneas 952-1002)
  - Actualizado `export_all_data()` para incluir nuevas hojas (líneas 1013-1027)

---

## 🎯 Uso del Sistema para Profesores

### Configuración Inicial

1. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generar Datos de Prueba:**
   ```bash
   python test_data_generator.py
   ```

3. **Ejecutar la Aplicación:**
   ```bash
   python Main.py
   ```

### Workflow Recomendado para Clases

#### Modo 1: Práctica Libre (Sin Protección)
Para que los estudiantes exploren todas las funcionalidades:
- Compartir la contraseña: `Contabilidad2026$`
- Permitir acceso a todos los módulos

#### Modo 2: Práctica Controlada (Con Protección)
Para enseñar paso a paso:
1. **Fase 1:** Estudiantes crean comprobantes manuales
2. **Fase 2:** Profesor desbloquea Libros (comparte contraseña)
3. **Fase 3:** Estudiantes ven Estados Financieros

### Evaluación del Trabajo

1. **Exportar Excel:**
   - Estudiante hace clic en "Exportar a Excel"
   - Guarda el archivo con su nombre: `Apellido_Nombre_Contabilidad.xlsx`
   - Envía archivo al profesor

2. **Revisión del Profesor:**
   - Abrir archivo Excel
   - **Hoja 1 (Resumen Evaluación):** Verificar validaciones
     - ¿Estado de Cuadre = CUADRADO? ✓
     - ¿Ecuación Contable = VÁLIDA? ✓
   - Revisar hojas específicas según objetivos de aprendizaje
   - Calificar comprensión y correcta clasificación

### Criterios de Evaluación Sugeridos

**Básico (40%):**
- ✅ Balance cuadrado (Debe = Haber)
- ✅ Ecuación contable válida (A = P + Pat)

**Intermedio (30%):**
- ✅ Clasificación correcta de cuentas por elemento
- ✅ Uso apropiado de códigos NIIF
- ✅ Comprobantes con glosas descriptivas

**Avanzado (30%):**
- ✅ Uso correcto de Libros de Compras/Ventas
- ✅ Estados financieros coherentes
- ✅ Comprensión de costo vs gasto
- ✅ Aplicación correcta de IVA e impuestos

---

## 🔧 Modificación de la Contraseña

Si desea cambiar la contraseña para un curso específico:

1. Abrir `views/main_window.py`
2. Ir a la línea 20
3. Modificar:
   ```python
   self.PASSWORD_LIBROS = "SuNuevaContraseña2026"
   ```
4. Guardar y reiniciar la aplicación

---

## 📝 Notas Técnicas

### Validaciones Implementadas
- Partida doble: Debe = Haber en cada comprobante
- Ecuación contable: Activos = Pasivos + Patrimonio
- Balance de Comprobación: Sumas Debe = Sumas Haber
- Naturaleza de cuentas respetada en todos los reportes

### Códigos de Ejemplo
```
1.01.01.0001 - Caja (Activos > Activo Corriente > Disponible > Caja)
2.01.02.0001 - Proveedores (Pasivos > Pasivo Corriente > Cuentas por Pagar)
3.01.01.0001 - Capital (Patrimonio > Capital y Reservas)
4.01.01.0001 - Ventas (Ingresos > Ingresos Ordinarios)
5.01.01.0001 - Sueldos (Gastos > Gastos de Administración)
```

### Soporte
Para preguntas o problemas técnicos, revisar:
- `README.md` - Documentación general
- `docs/` - Carpeta de documentación adicional

---

**Desarrollado por:** Franco Cortés, Crexer  
**Versión:** 2.0  
**Última Actualización:** 20 de Enero, 2026
