"""
Módulo de Contabilidad Profesional - NIIF/IFRS CMFChile
"""

from database.queries import fetch_all, fetch_one
import re


# ═══════════════════════════════════════════════════════════════════════════
# PARTE 1: CLASIFICACIÓN CONTABLE PROFESIONAL
# ═══════════════════════════════════════════════════════════════════════════

CLASIFICACION_CONTABLE = {
    "Activos": {
        "Activos Corrientes": [
            "Efectivo y equivalentes al efectivo",
            "Otros activos financieros, corrientes",
            "Deudores comerciales y otras cuentas por cobrar, corrientes",
            "Cuentas por Cobrar a Entidades Relacionadas, corrientes",
            "Inventarios",
            "Activos biológicos, corrientes",
            "Activos por impuestos, corrientes",
            "Otros activos, corrientes",
        ],
        "Activos No Corrientes": [
            "Otros activos financieros, no corrientes",
            "Deudores comerciales y otras cuentas por cobrar, no corrientes",
            "Cuentas por Cobrar a Entidades Relacionadas, no corrientes",
            "Inversiones contabilizadas utilizando el método de la participación",
            "Activos intangibles distintos de la plusvalía",
            "Plusvalía",
            "Propiedades, Planta y Equipo",
            "Propiedades de inversión, no corrientes",
            "Propiedad de inversión",
            "Activos por impuestos diferidos",
            "Otros activos no financieros, no corrientes",
        ],
    },
    "Pasivos": {
        "Pasivos Corrientes": [
            "Otros pasivos financieros, corrientes",
            "Cuentas comerciales y otras cuentas por pagar, corrientes",
            "Cuentas por Pagar a Entidades Relacionadas, corrientes",
            "Otras provisiones, corrientes",
            "Pasivos por impuestos, corrientes",
            "Provisiones por beneficios a los empleados, corrientes",
            "Otros pasivos no financieros, corrientes",
        ],
        "Pasivos No Corrientes": [
            "Otros pasivos financieros, no corrientes",
            "Otras cuentas por pagar, no corrientes",
            "Otras cuentas por pagar a Entidades Relacionadas, no corrientes",
            "Otras provisiones, no corrientes",
            "Pasivos por impuestos diferidos",
            "Provisiones por beneficios a los empleados, no corrientes",
            "Otros pasivos no financieros, no corrientes",
        ],
    },
    "Patrimonio": {
        "Patrimonio": [
            "Capital emitido",
            "Ganancias o Pérdidas acumuladas",
            "Primas de emisión",
            "Acciones propias en cartera",
            "Otras participaciones en el patrimonio",
            "Otras reservas",
            "Patrimonio atribuible a los propietarios de la controladora",
            "Participaciones no controladoras",
            "Patrimonio total",
        ],
    },
    "Ingresos": {
        "Ingresos de Actividades Ordinarias": [
            "Venta de bienes",
            "Prestación de servicios",
            "Ingresos por regalías, honorarios, comisiones y otros",
            "Ingresos por construcción de activos",
            "Otros ingresos de actividades ordinarias",
        ],
        "Otros Ingresos": [
            "Ganancias por cambio en moneda extranjera",
            "Ingresos financieros",
            "Ganancias en la disposición de activos",
            "Otros ingresos no operacionales",
        ],
    },
    "Gastos": {
        "Costo de Ventas": [
            "Costo de bienes vendidos",
            "Costo de servicios prestados",
        ],
        "Gastos de Administración": [
            "Sueldos y salarios",
            "Beneficios a empleados",
            "Gastos de depreciación y amortización",
            "Gastos de arrendamiento",
            "Gastos de servicios básicos",
            "Gastos de mantenimiento",
            "Gastos de viaje",
            "Gastos de comunicación",
            "Otros gastos administrativos",
        ],
        "Gastos de Ventas": [
            "Gastos de publicidad y marketing",
            "Comisiones a vendedores",
            "Transporte y distribución",
            "Gastos de empaques",
            "Otros gastos de ventas",
        ],
        "Gastos Financieros": [
            "Gastos por intereses",
            "Gastos por comisiones",
            "Pérdidas por cambio en moneda extranjera",
            "Otros gastos financieros",
        ],
        "Otros Gastos": [
            "Pérdidas en disposición de activos",
            "Otros gastos no operacionales",
        ],
    },
}


def obtener_elementos() -> list:
    """Retorna la lista de elementos (Activos, Pasivos, etc.)"""
    return list(CLASIFICACION_CONTABLE.keys())


def obtener_categorias(elemento: str) -> list:
    """Retorna las categorías disponibles para un elemento específico"""
    if elemento not in CLASIFICACION_CONTABLE:
        return []
    return list(CLASIFICACION_CONTABLE[elemento].keys())


def obtener_subcuentas(elemento: str, categoria: str) -> list:
    """Retorna las subcuentas disponibles para un elemento y categoría específicos"""
    if elemento not in CLASIFICACION_CONTABLE:
        return []
    if categoria not in CLASIFICACION_CONTABLE[elemento]:
        return []
    return CLASIFICACION_CONTABLE[elemento][categoria]


def validar_estructura(elemento: str, categoria: str, subcuenta: str) -> bool:
    """Valida que la combinación elemento-categoría-subcuenta sea válida"""
    subcuentas_validas = obtener_subcuentas(elemento, categoria)
    return subcuenta in subcuentas_validas


def obtener_informacion_completa(elemento: str, categoria: str = None, subcuenta: str = None) -> dict:
    """Retorna información completa de la estructura seleccionada"""
    return {
        "elemento": elemento,
        "categoria": categoria,
        "subcuenta": subcuenta,
        "es_valida": validar_estructura(elemento, categoria, subcuenta) if all([elemento, categoria, subcuenta]) else None,
    }


# ═══════════════════════════════════════════════════════════════════════════
# PARTE 2: GENERADOR DE CÓDIGOS CONTABLES PROFESIONAL
# ═══════════════════════════════════════════════════════════════════════════

# Mapeo de elementos a dígito inicial
ELEMENTO_DIGITOS = {
    "Activos": "1",
    "Pasivos": "2",
    "Patrimonio": "3",
    "Ingresos": "4",
    "Gastos": "5",
}

# Mapeo inverso
DIGITO_ELEMENTOS = {v: k for k, v in ELEMENTO_DIGITOS.items()}

# Mapeo FIJO de Subcategorías a códigos según NIIF/IFRS Chile
SUBCATEGORIA_CODIGOS = {
    "Activos": {
        "Activos Corrientes": "01",
        "Activos No Corrientes": "02",
    },
    "Pasivos": {
        "Pasivos Corrientes": "01",
        "Pasivos No Corrientes": "02",
    },
    "Patrimonio": {
        "Patrimonio": "01",
    },
    "Ingresos": {
        "Ingresos de Actividades Ordinarias": "01",
        "Otros Ingresos": "02",
    },
    "Gastos": {
        "Costo de Ventas": "01",
        "Gastos de Administración": "02",
        "Gastos de Ventas": "03",
        "Gastos Financieros": "04",
        "Otros Gastos": "05",
    },
}


def obtener_digito_elemento(elemento: str) -> str:
    """Obtiene el dígito inicial según el elemento (1-5)"""
    return ELEMENTO_DIGITOS.get(elemento, "0")


def obtener_digito_subcategoria(elemento: str, subcategoria: str) -> str:
    """
    Obtiene el código de subcategoría FIJO según mapeo NIIF/IFRS Chile.
    """
    if elemento not in SUBCATEGORIA_CODIGOS:
        return "01"
    
    codigo = SUBCATEGORIA_CODIGOS[elemento].get(subcategoria, "01")
    return codigo


def obtener_digito_subcuenta(elemento: str, subcategoria: str, subcuenta: str) -> str:
    """
    Obtiene el código de subcuenta (01-99) usando mapeo FIJO de la clasificación NIIF/IFRS.
    """
    if elemento not in CLASIFICACION_CONTABLE:
        return "01"
    
    if subcategoria not in CLASIFICACION_CONTABLE[elemento]:
        return "01"
    
    subcuentas_fijas = CLASIFICACION_CONTABLE[elemento][subcategoria]
    
    try:
        posicion = subcuentas_fijas.index(subcuenta) + 1
        return f"{posicion:02d}"
    except ValueError:
        return "01"


def obtener_numero_secuencial(elemento: str, subcategoria: str, subcuenta: str) -> str:
    """
    Obtiene el número secuencial (0001-9999) para la próxima cuenta.
    Incrementa por cada cuenta creada con la misma combinación D.CC.SS.
    """
    query = """
        SELECT COUNT(*) + 1 as siguiente
        FROM plan_cuentas
        WHERE elemento = ? AND subcategoria = ? AND grupo = ?
    """
    resultado = fetch_one(query, (elemento, subcategoria, subcuenta))
    siguiente = resultado[0] if resultado else 1
    
    if siguiente > 9999:
        siguiente = 9999
    
    return f"{siguiente:04d}"


def generar_codigo_contable(elemento: str, subcategoria: str, subcuenta: str) -> str:
    """
    Genera automáticamente el código contable completo siguiendo estándar NIIF/IFRS Chile.
    """
    if not all([elemento, subcategoria, subcuenta]):
        return ""
    
    try:
        d = obtener_digito_elemento(elemento)
        cc = obtener_digito_subcategoria(elemento, subcategoria)
        ss = obtener_digito_subcuenta(elemento, subcategoria, subcuenta)
        nnnn = obtener_numero_secuencial(elemento, subcategoria, subcuenta)
        
        codigo = f"{d}.{cc}.{ss}.{nnnn}"
        return codigo
    except Exception as e:
        print(f"Error generando código: {e}")
        return ""


def validar_formato_codigo(codigo: str) -> bool:
    """Valida que el código siga el formato D.CC.SS.NNNN"""
    patron = r"^[1-5]\.\d{2}\.\d{2}\.\d{4}$"
    return bool(re.match(patron, codigo))


def extraer_componentes_codigo(codigo: str) -> dict:
    """Extrae los componentes de un código contable"""
    if not validar_formato_codigo(codigo):
        return {}
    
    partes = codigo.split(".")
    return {
        "elemento_digito": partes[0],
        "elemento": DIGITO_ELEMENTOS.get(partes[0], ""),
        "subcategoria_codigo": partes[1],
        "subcuenta_codigo": partes[2],
        "secuencial": partes[3],
    }


def obtener_proximo_codigo(elemento: str, subcategoria: str, subcuenta: str) -> str:
    """
    Obtiene el próximo código disponible sin crear la cuenta.
    Útil para mostrar sugerencia de código al usuario.
    """
    return generar_codigo_contable(elemento, subcategoria, subcuenta)
