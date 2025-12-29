"""
Vista del Balance de Comprobación
"""
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from models.balance_comprobacion import BalanceComprobacionModel


class BalanceComprobacionView(ttk.Frame):
    """Vista del Balance de Comprobación"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = BalanceComprobacionModel()
        self.create_widgets()
        self.cargar_balance()

    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame del encabezado
        frm_header = ttk.Frame(self)
        frm_header.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(frm_header, text="BALANCE DE COMPROBACIÓN", 
                 font=("Arial", 14, "bold")).pack()
        
        # Frame de filtros
        frm_filtros = ttk.LabelFrame(self, text="Filtros de Fecha")
        frm_filtros.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frm_filtros, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_desde = DateEntry(frm_filtros, width=12, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='yyyy-mm-dd')
        self.fecha_desde.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frm_filtros, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_hasta = DateEntry(frm_filtros, width=12, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='yyyy-mm-dd')
        self.fecha_hasta.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frm_filtros, text="Filtrar",
                  command=self.aplicar_filtro).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frm_filtros, text="Todo el Período",
                  command=self.cargar_balance).grid(row=0, column=5, padx=5, pady=5)
        
        # Frame para la tabla con scrollbars
        frm_tabla = ttk.Frame(self)
        frm_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(frm_tabla, orient="vertical")
        hsb = ttk.Scrollbar(frm_tabla, orient="horizontal")
        
        # Treeview con columnas del balance
        columns = ("codigo", "cuenta", "debe", "haber", "saldo_deudor", "saldo_acreedor")
        self.tree = ttk.Treeview(frm_tabla, columns=columns, show="headings",
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", width=80, anchor="center")
        
        self.tree.heading("cuenta", text="Cuenta")
        self.tree.column("cuenta", width=350, anchor="w")
        
        self.tree.heading("debe", text="Movimientos Debe")
        self.tree.column("debe", width=150, anchor="e")
        
        self.tree.heading("haber", text="Movimientos Haber")
        self.tree.column("haber", width="150", anchor="e")
        
        self.tree.heading("saldo_deudor", text="Saldo Deudor")
        self.tree.column("saldo_deudor", width=150, anchor="e")
        
        self.tree.heading("saldo_acreedor", text="Saldo Acreedor")
        self.tree.column("saldo_acreedor", width=150, anchor="e")
        
        # Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        frm_tabla.grid_rowconfigure(0, weight=1)
        frm_tabla.grid_columnconfigure(0, weight=1)

        # Frame de totales
        frm_totales = ttk.LabelFrame(self, text="Totales", padding=10)
        frm_totales.pack(fill="x", padx=10, pady=5)
        
        # Labels para totales
        self.lbl_totales_movimientos = ttk.Label(
            frm_totales, 
            text="",
            font=("Arial", 10, "bold")
        )
        self.lbl_totales_movimientos.pack()
        
        self.lbl_totales_saldos = ttk.Label(
            frm_totales,
            text="",
            font=("Arial", 10, "bold")
        )
        self.lbl_totales_saldos.pack()
        
        self.lbl_estado = ttk.Label(
            frm_totales,
            text="",
            font=("Arial", 11, "bold")
        )
        self.lbl_estado.pack(pady=5)
        
        # Frame de botones
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(frm_buttons, text="Actualizar", 
                  command=self.cargar_balance).pack(side="left", padx=4)
    
    def aplicar_filtro(self):
        """Aplica el filtro de fechas"""
        fecha_desde = self.fecha_desde.get_date().strftime('%Y-%m-%d')
        fecha_hasta = self.fecha_hasta.get_date().strftime('%Y-%m-%d')
        self.cargar_balance(fecha_desde, fecha_hasta)
    
    def cargar_balance(self, fecha_desde=None, fecha_hasta=None):
        """Carga el balance de comprobación"""
        # Limpiar el árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener balance
        balance = self.model.get_balance(fecha_desde, fecha_hasta)
        
        # Insertar filas
        for item in balance:
            self.tree.insert("", "end", values=(
                item['codigo'],
                item['nombre'],
                f"${item['debe']:,.0f}" if item['debe'] > 0 else "-",
                f"${item['haber']:,.0f}" if item['haber'] > 0 else "-",
                f"${item['saldo_deudor']:,.0f}" if item['saldo_deudor'] > 0 else "-",
                f"${item['saldo_acreedor']:,.0f}" if item['saldo_acreedor'] > 0 else "-"
            ))
        
        # Calcular y mostrar totales
        totales = self.model.get_totales(balance)
        
        # Totales de movimientos
        self.lbl_totales_movimientos.config(
            text=f"MOVIMIENTOS: Debe: ${totales['total_debe']:,.0f}  |  Haber: ${totales['total_haber']:,.0f}"
        )
        
        # Totales de saldos
        self.lbl_totales_saldos.config(
            text=f"SALDOS: Deudor: ${totales['total_saldo_deudor']:,.0f}  |  Acreedor: ${totales['total_saldo_acreedor']:,.0f}"
        )
        
        # Verificar balance
        balance_ok = (
            abs(totales['balance_movimientos']) < 0.01 and 
            abs(totales['balance_saldos']) < 0.01
        )
        
        if balance_ok:
            self.lbl_estado.config(
                text="✓ BALANCE CUADRADO",
                foreground="green"
            )
        else:
            diferencias = f"Dif. Movimientos: ${totales['balance_movimientos']:,.0f} | Dif. Saldos: ${totales['balance_saldos']:,.0f}"
            self.lbl_estado.config(
                text=f"✗ BALANCE DESCUADRADO - {diferencias}",
                foreground="red"
            )
