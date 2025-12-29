"""
DOCUMENTACIÓN: MÓDULO DE EXPORTACIÓN A EXCEL
==============================================

Este módulo permite exportar todos los datos contables del sistema
a un archivo Excel profesional y evaluable por profesores.

CARACTERÍSTICAS:
================

1. RESUMEN DE EVALUACIÓN
   - Fecha de generación
   - Estadísticas generales (cantidad de cuentas, asientos, etc.)
   - Validación de integridad contable (cuadre débito-crédito)
   - Indicador visual de estado

2. PLAN DE CUENTAS
   - Listado completo de cuentas creadas por el alumno
   - Código, nombre, elemento, categoría, subcategoría
   - Útil para evaluar la estructura del plan de cuentas

3. COMPROBANTES
   - Detalle de todos los asientos contables realizados
   - Número de comprobante, fecha, glosa
   - Detalles: Código cuenta, nombre, debe, haber
   - Cálculo automático del cuadre

4. LIBRO DIARIO
   - Ordenado cronológicamente por fecha
   - Formato profesional de contabilidad
   - Totales de débito y crédito
   - Cuadre automático

5. BALANCE DE COMPROBACIÓN
   - Saldos de cada cuenta
   - Separación entre saldos deudores y acreedores
   - Validación automática de cuadre
   - Totales verificados

CÓMO USAR EN LA APLICACIÓN:
===========================

1. Desde el menú principal del Sistema Contable
2. Haz clic en el botón "📊 Exportar a Excel"
3. Selecciona la ubicación donde guardar el archivo
4. El sistema generará un Excel completo con todos los datos
5. El archivo estará listo para evaluación

FORMATO PROFESIONAL:
====================

- Encabezados con fondo azul oscuro y texto blanco
- Números formateados con dos decimales
- Bordes en todas las celdas
- Ancho de columnas ajustado automáticamente
- Fórmulas para cálculos automáticos
- Totales y validaciones integradas

INFORMACIÓN PARA EVALUADORES (PROFESORES):
==========================================

El archivo Excel contiene todo lo necesario para evaluar:

1. Competencia del alumno en clasificación de cuentas
2. Corrección en el registro de asientos
3. Capacidad de mantener la ecuación contable (Debe = Haber)
4. Conocimiento de estructura contable
5. Calidad de los registros realizados

Cada hoja incluye:
- Datos claros y ordenados
- Totales automáticos
- Indicadores visuales de cuadre/validación
- Fácil de revisar sin conocimiento técnico

ARCHIVO DE PRUEBA:
==================

El archivo "PRUEBA_Evaluacion_Contable.xlsx" contiene:
- Plan de Cuentas con datos iniciales del sistema
- Hojas vacías/con datos de ejemplo si se han registrado comprobantes
- Demostración de formato y estructura

NOTAS TÉCNICAS:
================

- Generado con librería openpyxl
- Compatible con Microsoft Excel, LibreOffice, Google Sheets
- Tamaño típico: 10-50 KB (muy ligero)
- Generación rápida (menos de 1 segundo)
- No requiere conexión a internet

PERSONALIZACIÓN FUTURA:
=======================

Es posible agregar:
- Hoja de Estados Financieros (ESF)
- Hoja de Estado de Resultados (ER)
- Gráficos de análisis
- Campos personalizables (alumno, fecha evaluación, etc.)
- Rubros específicos según asignatura
"""
