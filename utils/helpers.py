"""
Utilidades y funciones auxiliares
"""
from datetime import datetime
from config import DATE_FORMAT, IVA_RATE


def format_currency(amount):
    """Formatea un monto como moneda"""
    return f"${amount:,.0f}"


def parse_currency(text):
    """Convierte texto de moneda a float"""
    return float(text.replace("$", "").replace(",", ""))


def validate_date(date_str):
    """Valida formato de fecha"""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def calculate_iva(neto):
    """Calcula el IVA sobre un monto neto"""
    return neto * IVA_RATE


def calculate_total(neto, iva):
    """Calcula el total sumando neto + IVA"""
    return neto + iva


def validate_rut(rut):
    """Validación básica de RUT (formato chileno)"""
    # Aquí puedes agregar validación más compleja si lo deseas
    return len(rut) > 0
