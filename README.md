# Sistema de Contabilidad

Sistema de contabilidad completo desarrollado en Python con interfaz gráfica Tkinter y navegación lateral. **Diseñado específicamente para uso educativo** donde los estudiantes crean su propio plan de cuentas desde cero.

## 🎨 Interfaz

- **Panel lateral permanente** para navegación rápida entre secciones
- **Logo personalizable** en la parte inferior del sidebar (coloca tu logo en `assets/logo.png`)
- **Área de contenido** que cambia dinámicamente sin abrir ventanas adicionales
- **Vista inicial**: Plan de Cuentas (ideal para comenzar a crear cuentas)
- Ventana única y moderna (1400x700px)

## 🎓 Enfoque Educativo

Este sistema está diseñado para fines pedagógicos:

- ✅ **Inicia completamente VACÍO**: Los estudiantes deben crear su propio plan de cuentas
- ✅ **Aprendizaje práctico**: Construyen el sistema contable desde cero
- ✅ **Función de reseteo**: Pueden empezar de nuevo si cometen errores
- ✅ **Base de datos local**: Cada estudiante tiene su propia base de datos independiente

## Estructura del Proyecto

```
CrudPython/
├── Main.py                # Punto de entrada de la aplicación
├── config.py              # Configuración global
├── requirements.txt       # Dependencias del proyecto
├── assets/                # Recursos visuales
│   ├── logo.png          # Logo personalizable (200x180px recomendado)
│   └── README.md         # Instrucciones para el logo
├── database/              # Capa de datos
│   ├── __init__.py
│   ├── db_manager.py      # Gestor de base de datos
│   └── queries.py         # Funciones de consultas
├── models/                # Modelos de negocio
│   ├── __init__.py
│   ├── plan_cuentas.py
│   ├── comprobantes.py
│   ├── libro_diario.py
│   ├── balance_comprobacion.py
│   ├── libro_compras.py
│   ├── libro_ventas.py
│   └── reportes.py
├── views/                 # Interfaces gráficas
│   ├── __init__.py
│   ├── main_window.py
│   ├── plan_cuentas_view.py
│   ├── comprobantes_view.py
│   ├── libro_diario_view.py
│   ├── balance_comprobacion_view.py
│   ├── estado_situacion_view.py
│   ├── estado_resultados_view.py
│   ├── libro_compras_view.py
│   └── libro_ventas_view.py
├── utils/                 # Utilidades
│   ├── excel_exporter.py  # Exportación a Excel
│   └── helpers.py
└── contabilidad.db        # Base de datos SQLite (se crea automáticamente)
```

## Características

### 1. Plan de Cuentas
- CRUD completo de cuentas contables
- Clasificación por elemento, categoría, subcategoría y grupo
- **Sistema vacío inicial**: Los estudiantes crean todas las cuentas desde cero
- Búsqueda y filtrado de cuentas

### 2. Comprobantes Contables
- Sistema de partida doble (Debe = Haber)
- Numeración automática
- Múltiples líneas por comprobante
- Validación de balance automática
- Selector de fechas integrado

### 3. Libro Diario
- Visualización cronológica de todos los movimientos
- Filtrado por rango de fechas
- Muestra glosa, cuentas, débitos y créditos
- Verificación de balance en tiempo real

### 4. Balance de Comprobación
- Cálculo automático de saldos según naturaleza de cuenta
- Saldos deudores y acreedores
- Filtrado por período
- Verificación de cuadre

### 5. Estados Financieros
- **Estado de Situación Financiera** (Balance General)
  - Activos (Corrientes y No Corrientes)
  - Pasivos (Corrientes y No Corrientes)
  - Patrimonio
- **Estado de Resultados**
  - Ingresos
  - Costos de Ventas
  - Gastos Operacionales
  - Cálculo de utilidad/pérdida
  - Impuesto a la renta (25%)

### 6. Libros Auxiliares
- **Libro de Compras**
  - Registro de compras y servicios
  - Cálculo automático de IVA (19%)
  - Vinculación con comprobantes contables
- **Libro de Ventas**
  - Registro de ventas y servicios
  - Cálculo automático de IVA
  - Integración con contabilidad

### 7. Resetear Sistema 🔄
- **Nueva funcionalidad educativa**
- Permite eliminar todos los datos y empezar desde cero
- Requiere doble confirmación para evitar pérdidas accidentales
- Ideal cuando los estudiantes quieren rehacer su trabajo
- Ubicación: Menú lateral → "Resetear Sistema"

### 8. Personalización
- **Logo empresarial**: Coloca tu logo en `assets/logo.png` (200x180px recomendado)
- Se muestra automáticamente en el panel lateral
- Formato PNG con fondo transparente recomendado

## Requisitos

### Librerías Externas
- **tkcalendar** >= 1.6.1 - Widget de calendario para filtros de fecha
- **openpyxl** >= 3.0.0 - Para exportar reportes a Excel
- **Pillow** >= 10.0.0 - Para manejo de imágenes (logo)

### Librerías Estándar (incluidas en Python)
- **tkinter** - Interfaz gráfica
- **sqlite3** - Base de datos
- **datetime** - Manejo de fechas
- **os** - Operaciones del sistema

## Instalación y Uso

### Instalación

1. Clonar o descargar el proyecto

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. (Opcional) Agregar logo personalizado:
   - Coloca tu logo en `assets/logo.png`
   - Dimensiones recomendadas: 200x180 píxeles
   - Formato PNG con fondo transparente

### Ejecución

```bash
python Main.py
```

- La base de datos se creará automáticamente en el primer uso
- El sistema iniciará completamente vacío (sin cuentas predefinidas)
- Comenzar creando el Plan de Cuentas

### Primer Uso (Estudiantes)

1. **Crear Plan de Cuentas**
   - Ir a "Plan de Cuentas"
   - Crear las cuentas necesarias (Activos, Pasivos, Patrimonio, Ingresos, Costos, Gastos)
   - Cada cuenta debe tener: código, nombre, elemento, categoría, subcategoría y grupo

2. **Registrar Comprobantes**
   - Ir a "Comprobantes Contables"
   - Crear comprobantes con sus asientos
   - Asegurar que Debe = Haber

3. **Verificar en Libro Diario**
   - Ver todos los movimientos cronológicamente
   - Verificar que todo cuadra

4. **Revisar Balance de Comprobación**
   - Verificar saldos de todas las cuentas
   - Confirmar que Débitos = Créditos

5. **Generar Estados Financieros**
   - Estado de Situación Financiera
   - Estado de Resultados

6. **Exportar a Excel** (cuando esté listo)
   - Genera reporte completo profesional

### Si necesitas empezar de nuevo

- Usar **"Resetear Sistema"** en el menú lateral
- Confirmará dos veces antes de eliminar todos los datos
- El sistema volverá al estado inicial (vacío)

## Arquitectura

El proyecto sigue una arquitectura en capas:

- **config.py**: Configuración centralizada
- **database/**: Capa de acceso a datos
- **models/**: Lógica de negocio
- **views/**: Interfaces gráficas
- **utils/**: Funciones auxiliares

## Ventajas de esta Estructura

1. **Separación de responsabilidades**: Cada módulo tiene una función específica
2. **Fácil mantenimiento**: Los cambios en una capa no afectan a las demás
3. **Reutilización**: Los modelos y utilidades pueden usarse en diferentes vistas
4. **Escalabilidad**: Fácil agregar nuevas funcionalidades
5. **Profesional**: Estructura estándar de proyectos Python

## Exportación a Excel

El sistema genera un archivo Excel profesional con múltiples hojas de cálculo:

### Hojas Incluidas
1. **Resumen Evaluación** - Estadísticas generales y validaciones
2. **Plan de Cuentas** - Listado completo de cuentas
3. **Comprobantes** - Todos los comprobantes con detalles
4. **Libro Diario** - Movimientos cronológicos
5. **Balance de Comprobación** - Saldos con verificación
6. **Estado de Situación** - Balance General estructurado
7. **Estado de Resultados** - Estado de Resultados con cálculos

### Características
- ✅ Formato profesional con estilos y colores
- ✅ Fórmulas automáticas para validación
- ✅ Verificación de cuadre Debe/Haber
- ✅ Cálculos según naturaleza de cada cuenta
- ✅ Exportación en segundo plano (no bloquea la interfaz)

### Cómo usar
1. En el menú principal, elegir **"Exportar a Excel"**
2. Seleccionar ubicación y nombre del archivo
3. Esperar mensaje de confirmación
4. Abrir el archivo generado
5. Revisar la hoja "Resumen Evaluación" para validar el estado general

### Cálculos Correctos
El sistema respeta la naturaleza contable de cada cuenta:
- **Activo, Gasto, Costo** (Deudoras): Saldo = Debe - Haber
- **Pasivo, Patrimonio, Ingreso** (Acreedoras): Saldo = Haber - Debe

Esto asegura que las cuentas como "Caja" nunca muestren valores negativos incorrectos.

## Autor
Franco Cortés - Lightdawn2 
Sistema Contable basado en "Sistema contable1v0310.xlsm" -> Hugo Moraga
