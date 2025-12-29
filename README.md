# Sistema de Contabilidad

Sistema de contabilidad completo desarrollado en Python con interfaz gráfica Tkinter y navegación lateral.

## 🎨 Interfaz

- **Panel lateral permanente** para navegación rápida entre secciones
- **Área de contenido** que cambia dinámicamente sin abrir ventanas adicionales
- **Vista inicial**: Plan de Cuentas (ideal para comenzar a configurar el sistema)
- Ventana única y moderna (1400x700px)

## Estructura del Proyecto

```
CrudPython/
├── main.py                 # Punto de entrada de la aplicación
├── config.py              # Configuración global
├── database/              # Capa de datos
│   ├── __init__.py
│   ├── db_manager.py      # Gestor de base de datos
│   └── queries.py         # Funciones de consultas
├── models/                # Modelos de negocio
│   ├── __init__.py
│   ├── plan_cuentas.py
│   ├── comprobantes.py
│   ├── libro_compras.py
│   ├── libro_ventas.py
│   └── reportes.py
├── views/                 # Interfaces gráficas
│   ├── __init__.py
│   ├── main_window.py
│   ├── plan_cuentas_view.py
│   ├── comprobantes_view.py
│   ├── estado_situacion_view.py
│   ├── estado_resultados_view.py
│   ├── libro_compras_view.py
│   └── libro_ventas_view.py
├── utils/                 # Utilidades
│   └── helpers.py
└── contabilidad.db        # Base de datos SQLite (se crea automáticamente)
```

## Características

### 1. Plan de Cuentas
- CRUD completo de cuentas contables
- Clasificación por elemento, categoría, subcategoría y grupo
- 31 cuentas predefinidas

### 2. Comprobantes Contables
- Sistema de partida doble (Debe = Haber)
- Numeración automática
- Múltiples líneas por comprobante
- Validación de balance

### 3. Estados Financieros
- Estado de Situación Financiera (Balance)
- Estado de Resultados
- Cálculo automático de saldos

### 4. Libros Auxiliares
- Libro de Compras
- Libro de Ventas
- Cálculo automático de IVA (19%)

## Requisitos

- Python 3.7 o superior
- tkinter (incluido en Python)
- sqlite3 (incluido en Python)
- openpyxl (requerido para exportación a Excel)

## Instalación y Uso

1. Clonar o descargar el proyecto
2. Ejecutar la aplicación:

```bash
python main.py
```

3. La base de datos se creará automáticamente en el primer uso

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

- Botón en la ventana principal: "📊 Exportar a Excel".
- Genera un archivo con hojas: Resumen Evaluación, PlanCuentas, Comprobantes, LibroDiario, Balance de Comprobación, Estado de Situación, Estado de Resultados.
- Incluye fórmulas y validaciones para verificar el cuadre Debe/Haber y totales.
- La exportación se ejecuta en segundo plano (no bloquea la interfaz) y muestra mensajes de éxito o error.

### Cómo usar
- Abrir la aplicación y cargar comprobantes normalmente.
- En el menú principal, elegir "📊 Exportar a Excel" y seleccionar la ubicación.
- Revisar la hoja "Resumen Evaluación" para validar el estado general.

## Autor
Franco Cortés - Lightdawn2 
Sistema Contable basado en "Sistema contable1v0310.xlsm" -> Hugo Moraga
