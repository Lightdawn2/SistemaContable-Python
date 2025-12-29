# 📚 ÍNDICE DE DOCUMENTACIÓN - SISTEMA CONTABLE EDUCATIVO

## Sistema Validado según Normativa Chilena y NIIF

---

## 📖 DOCUMENTACIÓN PRINCIPAL

### 1. [README.md](README.md) - **EMPEZAR AQUÍ**
**Descripción:** Guía principal del sistema  
**Para quién:** Todos los usuarios  
**Contenido:**
- Descripción general del sistema
- Características principales
- Instalación paso a paso
- Uso básico de la interfaz
- Estructura del proyecto
- Requisitos técnicos

**⏱️ Tiempo lectura:** 5-10 minutos

---

### 2. [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - **PARA DOCENTES** 🎓
**Descripción:** Guía completa para uso educativo  
**Para quién:** Profesores y facilitadores  
**Contenido:**
- Inicio rápido (3 pasos)
- Caso de estudio incluido
- Criterios de evaluación sugeridos
- Ejercicios por nivel de dificultad
- Modificación de escenarios
- Solución de problemas comunes
- Material complementario

**⏱️ Tiempo lectura:** 15-20 minutos

---

### 3. [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md) - **RESUMEN TÉCNICO**
**Descripción:** Resumen de cambios y validación  
**Para quién:** Gerentes, directores académicos, contadores  
**Contenido:**
- Resultado de validación contable
- Cambios implementados
- Mejoras en Estado de Resultados (NIIF)
- Mejoras en Estado de Situación
- Plan de cuentas según estructura chilena
- Casos de prueba
- Archivos modificados y nuevos
- Checklist de funcionalidades

**⏱️ Tiempo lectura:** 10-15 minutos

---

### 4. [VALIDACION_CONTABLE.md](VALIDACION_CONTABLE.md) - **ANÁLISIS TÉCNICO PROFUNDO**
**Descripción:** Validación contable exhaustiva  
**Para quién:** Contadores, auditores, analistas  
**Contenido:**
- Análisis según normativa chilena y NIIF
- Verificación de principios contables
- Validación ecuación contable
- Tratamiento de IVA (19%)
- Impuesto a la Renta (25%)
- Casos de prueba con resultados
- Cumplimiento normativo
- Referencias a NIC/NIIF
- Documentación de validaciones en Excel

**⏱️ Tiempo lectura:** 20-30 minutos

---

## 🔧 SCRIPTS Y HERRAMIENTAS

### 5. [test_data_generator.py](test_data_generator.py) - **GENERADOR DE DATOS**
**Descripción:** Script para crear datos de prueba  
**Para quién:** Profesores, desarrolladores, testers  
**Funcionalidad:**
- Limpia base de datos
- Inserta 40 cuentas del plan
- Crea 12 transacciones comerciales realistas
- Verifica Debe = Haber
- Verifica Activo = Pasivo + Patrimonio
- Muestra resultados de validación

**Uso:**
```bash
python test_data_generator.py
```

**⏱️ Tiempo ejecución:** 2-3 segundos

---

### 6. [test_excel_export.py](test_excel_export.py) - **EXPORTACIÓN AUTOMÁTICA**
**Descripción:** Script para generar Excel automáticamente  
**Para quién:** Profesores, evaluadores  
**Funcionalidad:**
- Ejecuta generador de datos
- Exporta todas las hojas a Excel
- Verifica creación del archivo
- Opción de abrir automáticamente

**Uso:**
```bash
python test_excel_export.py
```

**⏱️ Tiempo ejecución:** 5-10 segundos

---

### 7. [Main.py](Main.py) - **APLICACIÓN PRINCIPAL**
**Descripción:** Sistema contable interactivo  
**Para quién:** Todos los usuarios  
**Funcionalidad:**
- Interfaz gráfica completa
- Gestión de Plan de Cuentas
- Registro de Comprobantes
- Libros de Compra y Venta
- Visualización de reportes
- Exportación a Excel
- Reseteo del sistema

**Uso:**
```bash
python Main.py
```

---

## 📋 DOCUMENTACIÓN TÉCNICA

### 8. [requirements.txt](requirements.txt) - **DEPENDENCIAS**
**Contenido:**
```
tkcalendar>=1.6.1
openpyxl>=3.0.0
Pillow>=10.0.0
```

**Instalación:**
```bash
pip install -r requirements.txt
```

---

### 9. [config.py](config.py) - **CONFIGURACIÓN**
**Parámetros principales:**
- `IVA_RATE = 0.19` (19%)
- `IMPUESTO_RENTA_RATE = 0.25` (25%)
- `DB_FILE` - Ubicación base de datos
- Tipos de documentos permitidos
- Elementos contables

---

## 🗂️ ESTRUCTURA DEL PROYECTO

```
CRUD-PYTHON -BackUP/
│
├── 📄 README.md                    # Guía principal
├── 📄 GUIA_PROFESORES.md           # Para docentes
├── 📄 RESUMEN_EJECUTIVO.md         # Resumen técnico
├── 📄 VALIDACION_CONTABLE.md       # Análisis detallado
├── 📄 INDICE_DOCUMENTACION.md      # Este archivo
│
├── 🐍 Main.py                      # Aplicación principal
├── 🐍 config.py                    # Configuración
├── 🐍 test_data_generator.py      # Generador de pruebas
├── 🐍 test_excel_export.py        # Exportación automática
├── 📋 requirements.txt             # Dependencias
│
├── 📁 database/                    # Módulo de base de datos
│   ├── __init__.py
│   ├── db_manager.py              # Gestión de BD
│   └── queries.py                 # Consultas SQL
│
├── 📁 models/                      # Modelos de datos
│   ├── __init__.py
│   ├── plan_cuentas.py            # CRUD Plan de Cuentas
│   ├── comprobantes.py            # CRUD Comprobantes
│   ├── libro_compras.py           # CRUD Libro Compras
│   ├── libro_ventas.py            # CRUD Libro Ventas
│   ├── libro_diario.py            # Libro Diario
│   ├── balance_comprobacion.py    # Balance
│   └── reportes.py                # Estados Financieros
│
├── 📁 views/                       # Vistas/Interfaces
│   ├── __init__.py
│   ├── main_window.py             # Ventana principal
│   ├── plan_cuentas_view.py       # UI Plan Cuentas
│   ├── comprobantes_view.py       # UI Comprobantes
│   ├── libro_compras_view.py      # UI Libro Compras
│   ├── libro_ventas_view.py       # UI Libro Ventas
│   ├── libro_diario_view.py       # UI Libro Diario
│   ├── balance_comprobacion_view.py  # UI Balance
│   ├── estado_situacion_view.py   # UI Estado Situación
│   └── estado_resultados_view.py  # UI Estado Resultados
│
├── 📁 utils/                       # Utilidades
│   ├── excel_exporter.py          # Exportación Excel
│   └── helpers.py                 # Funciones auxiliares
│
├── 📁 assets/                      # Recursos
│   ├── logo.png                   # Logo del sistema
│   └── README.md                  # Instrucciones logo
│
└── 📁 docs/                        # Documentación legacy
    └── (archivos antiguos)
```

---

## 🎯 GUÍAS DE LECTURA SEGÚN ROL

### 👨‍🎓 Para Estudiantes:
1. **Empezar:** [README.md](README.md) - Sección "Instalación"
2. **Aprender:** [README.md](README.md) - Sección "Uso"
3. **Practicar:** Ejecutar `Main.py`
4. **Dudas:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - Sección "Ejercicios"

### 👨‍🏫 Para Profesores:
1. **Empezar:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - "Inicio Rápido"
2. **Preparar clase:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - "Caso de Estudio"
3. **Evaluar:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - "Criterios de Evaluación"
4. **Problemas:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - "Solución de Problemas"

### 💼 Para Contadores/Auditores:
1. **Validar:** [VALIDACION_CONTABLE.md](VALIDACION_CONTABLE.md)
2. **Resumen:** [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)
3. **Probar:** Ejecutar `python test_data_generator.py`
4. **Verificar Excel:** Ejecutar `python test_excel_export.py`

### 👨‍💻 Para Desarrolladores:
1. **Arquitectura:** [README.md](README.md) - Sección "Estructura"
2. **Código:** Revisar archivos en `models/`, `views/`, `utils/`
3. **Base de datos:** `database/db_manager.py`
4. **Tests:** `test_data_generator.py` y `test_excel_export.py`

### 👔 Para Directivos:
1. **Resumen Ejecutivo:** [RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)
2. **Validación:** [VALIDACION_CONTABLE.md](VALIDACION_CONTABLE.md) - Sección "Conclusiones"
3. **Uso Educativo:** [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - Sección "Casos de Éxito"

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

### Primera Vez (Setup):
1. Leer [README.md](README.md) - Sección Instalación
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar: `python test_data_generator.py`
4. Verificar: `python Main.py`
5. Exportar: `python test_excel_export.py`

### Uso Docente (Preparar Clase):
1. Ejecutar: `python test_data_generator.py`
2. Abrir: `python Main.py`
3. Navegar por todos los módulos
4. Exportar Excel para mostrar
5. Modificar `test_data_generator.py` si necesario

### Uso Estudiante (Hacer Ejercicio):
1. Abrir: `python Main.py`
2. Ir a "Plan de Cuentas" → Crear cuentas
3. Ir a "Comprobantes" → Registrar transacciones
4. Verificar: "Estado de Resultados"
5. Verificar: "Estado de Situación"
6. Exportar: Botón "Exportar a Excel"
7. Entregar archivo Excel

### Validación Contable:
1. Leer: [VALIDACION_CONTABLE.md](VALIDACION_CONTABLE.md)
2. Ejecutar: `python test_data_generator.py`
3. Verificar salida: Debe mostrar "BALANCE CUADRADO"
4. Generar Excel: `python test_excel_export.py`
5. Revisar hoja "Balance de Comprobación"
6. Revisar hoja "Estado de Situación"

---

## 📞 AYUDA Y SOPORTE

### Errores Comunes:

**Error: "No module named 'tkcalendar'"**
- Solución: `pip install tkcalendar`

**Error: "No module named 'openpyxl'"**
- Solución: `pip install openpyxl`

**Error: "No module named 'PIL'"**
- Solución: `pip install Pillow`

**Error: "Balance no cuadra"**
- Ver: [GUIA_PROFESORES.md](GUIA_PROFESORES.md) - "Solución de Problemas"

**Error: "Activo ≠ Pasivo + Patrimonio"**
- Ver: [VALIDACION_CONTABLE.md](VALIDACION_CONTABLE.md) - Sección 2.2

### Recursos Adicionales:

**Normativas:**
- NIC 1: Presentación de Estados Financieros
- NIC 2: Inventarios
- NIC 12: Impuesto a las Ganancias
- Código Tributario de Chile
- Normativa SII sobre IVA

**Enlaces Útiles:**
- IFRS Foundation: https://www.ifrs.org/
- Colegio de Contadores de Chile: https://www.contadores.cl/
- SII Chile: https://www.sii.cl/

---

## 🔄 ACTUALIZACIONES

### Versión 2.0 (Actual) - Diciembre 2025
✅ Estado de Resultados según NIIF  
✅ Cálculo automático de Utilidad del Ejercicio  
✅ Inclusión de Impuesto por Pagar  
✅ Validación contable completa  
✅ Generador de datos de prueba  
✅ Exportación Excel mejorada  
✅ Documentación exhaustiva  

### Versión 1.0 - Anterior
- Sistema básico funcional
- Estados financieros simples
- Exportación Excel básica

---

## ✅ CHECKLIST DE VERIFICACIÓN

Antes de usar el sistema, verificar:

- [ ] Python 3.12+ instalado
- [ ] Virtual environment activado (opcional pero recomendado)
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Base de datos creada (se crea automáticamente al ejecutar)
- [ ] Documentación leída ([README.md](README.md))

Para validar funcionamiento:

- [ ] `python test_data_generator.py` ejecuta sin errores
- [ ] Muestra "BALANCE CUADRADO"
- [ ] `python Main.py` abre interfaz
- [ ] "Exportar a Excel" genera archivo
- [ ] Excel tiene 7 hojas completas

---

## 📊 ESTADÍSTICAS DEL SISTEMA

**Líneas de código:** ~5,000+  
**Archivos Python:** 25+  
**Módulos principales:** 8  
**Vistas/Interfaces:** 8  
**Documentación:** 5 archivos principales  
**Tests automatizados:** 2 scripts  
**Funcionalidades core:** 8  

**Normativas cumplidas:**
- ✅ Contabilidad General Chilena
- ✅ NIIF (4 normas principales)
- ✅ Normativa SII Chile
- ✅ Principios Contables Generalmente Aceptados

**Validaciones implementadas:**
- ✅ Partida Doble (Debe = Haber)
- ✅ Ecuación Contable (A = P + P)
- ✅ Naturaleza de Cuentas
- ✅ IVA 19%
- ✅ Impuesto Renta 25%

---

## 🎓 CONCLUSIÓN

Este sistema está **completamente validado** desde la perspectiva contable y cumple con todas las normativas vigentes en Chile y estándares internacionales (NIIF).

Es ideal para:
- ✅ Enseñanza de contabilidad
- ✅ Práctica de estudiantes
- ✅ Casos de estudio
- ✅ Evaluación de conocimientos
- ✅ Comprensión de partida doble
- ✅ Elaboración de estados financieros

---

**Última actualización:** 29 de Diciembre de 2025  
**Versión:** 2.0  
**Estado:** Validado y Aprobado ✅

---

_Este índice fue creado para facilitar la navegación en la documentación del Sistema Contable Educativo. Para soporte o consultas, referirse a la sección correspondiente de cada documento._
