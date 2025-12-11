"""
Ventana principal de la aplicación
"""
import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    """Ventana principal del sistema contable"""
    
    def __init__(self):
        super().__init__()
        self.title("Sistema Contable - Menú Principal")
        self.geometry("400x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        """Crea los widgets del menú principal"""
        frm = ttk.Frame(self, padding=20)
        frm.pack(expand=True, fill="both")

        ttk.Label(frm, text="SISTEMA CONTABLE", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frm, text="Seleccione una opción:", 
                 font=("Arial", 10)).pack(pady=5)

        ttk.Button(frm, text="Plan de Cuentas", 
                  command=self.open_plan_cuentas, width=35).pack(pady=4)
        ttk.Button(frm, text="Comprobantes Contables", 
                  command=self.open_comprobantes, width=35).pack(pady=4)
        ttk.Button(frm, text="Estado de Situación Financiera", 
                  command=self.open_esf, width=35).pack(pady=4)
        ttk.Button(frm, text="Estado de Resultados", 
                  command=self.open_er, width=35).pack(pady=4)
        ttk.Button(frm, text="Libro de Compras", 
                  command=self.open_libro_compras, width=35).pack(pady=4)
        ttk.Button(frm, text="Libro de Ventas", 
                  command=self.open_libro_ventas, width=35).pack(pady=4)

        ttk.Separator(frm, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(frm, text="Salir", command=self.quit, width=35).pack(pady=4)

    def open_plan_cuentas(self):
        """Abre la ventana de Plan de Cuentas"""
        from views.plan_cuentas_view import PlanCuentasView
        if not any(isinstance(w, PlanCuentasView) for w in self.winfo_children()):
            PlanCuentasView(self)

    def open_comprobantes(self):
        """Abre la ventana de Comprobantes"""
        from views.comprobantes_view import ComprobantesView
        if not any(isinstance(w, ComprobantesView) for w in self.winfo_children()):
            ComprobantesView(self)

    def open_esf(self):
        """Abre el Estado de Situación Financiera"""
        from views.estado_situacion_view import EstadoSituacionView
        if not any(isinstance(w, EstadoSituacionView) for w in self.winfo_children()):
            EstadoSituacionView(self)

    def open_er(self):
        """Abre el Estado de Resultados"""
        from views.estado_resultados_view import EstadoResultadosView
        if not any(isinstance(w, EstadoResultadosView) for w in self.winfo_children()):
            EstadoResultadosView(self)

    def open_libro_compras(self):
        """Abre el Libro de Compras"""
        from views.libro_compras_view import LibroComprasView
        if not any(isinstance(w, LibroComprasView) for w in self.winfo_children()):
            LibroComprasView(self)

    def open_libro_ventas(self):
        """Abre el Libro de Ventas"""
        from views.libro_ventas_view import LibroVentasView
        if not any(isinstance(w, LibroVentasView) for w in self.winfo_children()):
            LibroVentasView(self)
