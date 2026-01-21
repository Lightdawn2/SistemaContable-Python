"""
Vista del Estado de Resultados
"""
import tkinter as tk
from tkinter import ttk
from models.reportes import ReportesModel
from config import IMPUESTO_RENTA_RATE


class EstadoResultadosView(ttk.Frame):
    """Vista del Estado de Resultados"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = ReportesModel()
        self.create_widgets()
        self.generar_reporte()

    def create_widgets(self):
        frm_header = ttk.Frame(self)
        frm_header.pack(fill="x", padx=10, pady=10)
        ttk.Label(frm_header, text="ESTADO DE RESULTADOS", 
                 font=("Arial", 14, "bold")).pack()
        
        frm_buttons = ttk.Frame(frm_header)
        frm_buttons.pack(pady=5)
        ttk.Button(frm_buttons, text="Actualizar", command=self.generar_reporte).pack(side="left", padx=4)

        self.tree = ttk.Treeview(self, columns=("concepto", "monto"), show="headings", height=20)
        self.tree.heading("concepto", text="Concepto")
        self.tree.heading("monto", text="Monto")
        self.tree.column("concepto", width=400)
        self.tree.column("monto", width=150, anchor="e")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def generar_reporte(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        cuentas = self.model.get_estado_resultados()

        ingresos = []
        costos = []
        gastos_admin = []
        gastos_ventas = []
        gastos_financieros = []
        otros_gastos = []

        for codigo, nombre, elemento, categoria, debe, haber in cuentas:
            if elemento == 'Ingresos':
                saldo = haber - debe
                if saldo != 0:
                    ingresos.append((codigo, nombre, saldo))
            elif elemento == 'Gastos':
                saldo = debe - haber
                if saldo != 0:
                    # Clasificar entre costos y gastos según la categoría
                    if 'Costo de Ventas' in categoria:
                        costos.append((codigo, nombre, saldo))
                    elif 'Administración' in categoria:
                        gastos_admin.append((codigo, nombre, saldo))
                    elif 'Ventas' in categoria or 'Comercial' in categoria:
                        gastos_ventas.append((codigo, nombre, saldo))
                    elif 'Financier' in categoria:
                        gastos_financieros.append((codigo, nombre, saldo))
                    else:
                        otros_gastos.append((codigo, nombre, saldo))

        # INGRESOS ORDINARIOS
        total_ingresos = sum(s for _, _, s in ingresos)
        self.tree.insert("", "end", values=("INGRESOS DE ACTIVIDADES ORDINARIAS", ""), tags=("header",))
        for codigo, nombre, saldo in ingresos:
            self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
        self.tree.insert("", "end", values=("Total Ingresos Ordinarios", f"${total_ingresos:,.0f}"), tags=("subtotal",))

        # COSTO DE VENTAS
        self.tree.insert("", "end", values=("", ""))
        total_costos = sum(s for _, _, s in costos)
        self.tree.insert("", "end", values=("COSTO DE VENTAS", ""), tags=("header",))
        for codigo, nombre, saldo in costos:
            self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
        self.tree.insert("", "end", values=("Total Costo de Ventas", f"${total_costos:,.0f}"), tags=("subtotal",))

        # MARGEN BRUTO / UTILIDAD BRUTA
        margen_bruto = total_ingresos - total_costos
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("UTILIDAD BRUTA", f"${margen_bruto:,.0f}"), tags=("total",))

        # GASTOS DE ADMINISTRACIÓN
        self.tree.insert("", "end", values=("", ""))
        total_gastos_admin = sum(s for _, _, s in gastos_admin)
        if gastos_admin:
            self.tree.insert("", "end", values=("GASTOS DE ADMINISTRACIÓN", ""), tags=("header",))
            for codigo, nombre, saldo in gastos_admin:
                self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree.insert("", "end", values=("Total Gastos Administración", f"${total_gastos_admin:,.0f}"), tags=("subtotal",))

        # GASTOS DE VENTAS
        total_gastos_ventas = sum(s for _, _, s in gastos_ventas)
        if gastos_ventas:
            self.tree.insert("", "end", values=("", ""))
            self.tree.insert("", "end", values=("GASTOS DE VENTAS", ""), tags=("header",))
            for codigo, nombre, saldo in gastos_ventas:
                self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree.insert("", "end", values=("Total Gastos de Ventas", f"${total_gastos_ventas:,.0f}"), tags=("subtotal",))

        # RESULTADO OPERACIONAL
        total_gastos_operacionales = total_gastos_admin + total_gastos_ventas
        resultado_operacional = margen_bruto - total_gastos_operacionales
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("RESULTADO OPERACIONAL", f"${resultado_operacional:,.0f}"), tags=("total",))

        # GASTOS FINANCIEROS
        total_gastos_financieros = sum(s for _, _, s in gastos_financieros)
        if gastos_financieros:
            self.tree.insert("", "end", values=("", ""))
            self.tree.insert("", "end", values=("COSTOS FINANCIEROS", ""), tags=("header",))
            for codigo, nombre, saldo in gastos_financieros:
                self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree.insert("", "end", values=("Total Costos Financieros", f"${total_gastos_financieros:,.0f}"), tags=("subtotal",))

        # OTROS GASTOS
        total_otros_gastos = sum(s for _, _, s in otros_gastos)
        if otros_gastos:
            self.tree.insert("", "end", values=("", ""))
            self.tree.insert("", "end", values=("OTROS GASTOS", ""), tags=("header",))
            for codigo, nombre, saldo in otros_gastos:
                self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree.insert("", "end", values=("Total Otros Gastos", f"${total_otros_gastos:,.0f}"), tags=("subtotal",))

        # RESULTADO ANTES DE IMPUESTO
        resultado_antes_impuesto = resultado_operacional - total_gastos_financieros - total_otros_gastos
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("RESULTADO ANTES DE IMPUESTO A LA RENTA", 
                                           f"${resultado_antes_impuesto:,.0f}"), tags=("total",))

        # IMPUESTO A LA RENTA
        impuesto = resultado_antes_impuesto * IMPUESTO_RENTA_RATE if resultado_antes_impuesto > 0 else 0
        self.tree.insert("", "end", values=(f"Gasto por Impuesto a la Renta ({int(IMPUESTO_RENTA_RATE*100)}%)", 
                                           f"${impuesto:,.0f}"), tags=("subtotal",))

        # RESULTADO DEL EJERCICIO
        resultado_ejercicio = resultado_antes_impuesto - impuesto
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("GANANCIA (PÉRDIDA) DEL EJERCICIO", 
                                           f"${resultado_ejercicio:,.0f}"), tags=("final",))

        # Estilos
        self.tree.tag_configure("header", font=("Arial", 10, "bold"), background="#f0f0f0")
        self.tree.tag_configure("subtotal", font=("Arial", 9, "bold"), background="#e8e8e8")
        self.tree.tag_configure("total", font=("Arial", 10, "bold"), background="#d0d0d0")
        self.tree.tag_configure("final", font=("Arial", 11, "bold"), background="#b0d0ff")
