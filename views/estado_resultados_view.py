"""
Vista del Estado de Resultados
"""
import tkinter as tk
from tkinter import ttk
from models.reportes import ReportesModel
from config import IMPUESTO_RENTA_RATE


class EstadoResultadosView(tk.Toplevel):
    """Vista del Estado de Resultados"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master_window = master
        self.title("Estado de Resultados")
        self.geometry("700x600")
        self.resizable(True, True)
        self.model = ReportesModel()
        self.create_widgets()
        self.generar_reporte()
        
        # Ocultar ventana principal
        if self.master_window:
            self.master_window.withdraw()
        
        # Manejar el cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        frm_header = ttk.Frame(self)
        frm_header.pack(fill="x", padx=10, pady=10)
        ttk.Label(frm_header, text="ESTADO DE RESULTADOS", 
                 font=("Arial", 14, "bold")).pack()
        
        frm_buttons = ttk.Frame(frm_header)
        frm_buttons.pack(pady=5)
        ttk.Button(frm_buttons, text="Actualizar", command=self.generar_reporte).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="← Volver al Menú", command=self.on_closing).pack(side="left", padx=4)

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
        gastos = []

        for codigo, nombre, elemento, categoria, debe, haber in cuentas:
            if elemento == 'Ingreso':
                saldo = haber - debe
                if saldo != 0:
                    ingresos.append((codigo, nombre, saldo))
            elif elemento == 'Costo':
                saldo = debe - haber
                if saldo != 0:
                    costos.append((codigo, nombre, saldo))
            elif elemento == 'Gasto':
                saldo = debe - haber
                if saldo != 0:
                    gastos.append((codigo, nombre, saldo))

        total_ingresos = sum(s for _, _, s in ingresos)
        total_costos = sum(s for _, _, s in costos)
        total_gastos = sum(s for _, _, s in gastos)

        self.tree.insert("", "end", values=("INGRESOS", ""), tags=("header",))
        for codigo, nombre, saldo in ingresos:
            self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${saldo:,.0f}"))
        self.tree.insert("", "end", values=("Total Ingresos", f"${total_ingresos:,.0f}"), tags=("subtotal",))

        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("COSTOS DE VENTAS", ""), tags=("header",))
        for codigo, nombre, saldo in costos:
            self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${-saldo:,.0f}"))
        self.tree.insert("", "end", values=("Total Costos", f"${-total_costos:,.0f}"), tags=("subtotal",))

        margen_bruto = total_ingresos - total_costos
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("MARGEN BRUTO", f"${margen_bruto:,.0f}"), tags=("total",))

        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("GASTOS OPERACIONALES", ""), tags=("header",))
        for codigo, nombre, saldo in gastos:
            self.tree.insert("", "end", values=(f"  {codigo} - {nombre}", f"${-saldo:,.0f}"))
        self.tree.insert("", "end", values=("Total Gastos", f"${-total_gastos:,.0f}"), tags=("subtotal",))

        resultado_antes_impuesto = margen_bruto - total_gastos
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("RESULTADO ANTES DE IMPUESTO", 
                                           f"${resultado_antes_impuesto:,.0f}"), tags=("total",))

        impuesto = resultado_antes_impuesto * IMPUESTO_RENTA_RATE
        self.tree.insert("", "end", values=(f"Impuesto a la Renta ({int(IMPUESTO_RENTA_RATE*100)}%)", 
                                           f"${-impuesto:,.0f}"), tags=("subtotal",))

        resultado_ejercicio = resultado_antes_impuesto - impuesto
        self.tree.insert("", "end", values=("", ""))
        self.tree.insert("", "end", values=("RESULTADO DEL EJERCICIO", 
                                           f"${resultado_ejercicio:,.0f}"), tags=("final",))

        # Estilos
        self.tree.tag_configure("header", font=("Arial", 10, "bold"), background="#f0f0f0")
        self.tree.tag_configure("subtotal", font=("Arial", 9, "bold"), background="#e8e8e8")
        self.tree.tag_configure("total", font=("Arial", 10, "bold"), background="#d0d0d0")
        self.tree.tag_configure("final", font=("Arial", 11, "bold"), background="#b0d0ff")
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.master_window:
            self.master_window.deiconify()
        self.destroy()
