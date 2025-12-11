"""
Configuración general del sistema contable
"""
import os

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "contabilidad.db")

# Constantes
IVA_RATE = 0.19  # 19%
IMPUESTO_RENTA_RATE = 0.25  # 25%

# Tipos de documentos
TIPOS_DOCUMENTO = ["Factura", "Boleta", "Nota de Crédito", "Nota de Débito"]

# Elementos contables
ELEMENTOS = ["Activo", "Pasivo", "Patrimonio", "Ingreso", "Costo", "Gasto"]

# Formato de fecha
DATE_FORMAT = "%Y-%m-%d"
