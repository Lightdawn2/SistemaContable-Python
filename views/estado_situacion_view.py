"""  
Vista del Estado de Situación Financiera
"""
import tkinter as tk
from tkinter import ttk
from models.reportes import ReportesModel


class EstadoSituacionView(ttk.Frame):
    """Vista del Estado de Situación Financiera (Balance)"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = ReportesModel()
        self.create_widgets()
        self.generar_reporte()

    def create_widgets(self):
        frm_header = ttk.Frame(self)
        frm_header.pack(fill="x", padx=10, pady=10)
        ttk.Label(frm_header, text="ESTADO DE SITUACIÓN FINANCIERA", 
                 font=("Arial", 14, "bold")).pack()
        
        frm_buttons = ttk.Frame(frm_header)
        frm_buttons.pack(pady=5)
        ttk.Button(frm_buttons, text="Actualizar", command=self.generar_reporte).pack(side="left", padx=4)

        frm_main = ttk.Frame(self)
        frm_main.pack(fill="both", expand=True, padx=10, pady=10)

        # Activos
        frm_activos = ttk.LabelFrame(frm_main, text="ACTIVOS", padding=10)
        frm_activos.pack(side="left", fill="both", expand=True, padx=5)
        self.tree_activos = ttk.Treeview(frm_activos, columns=("cuenta", "saldo"), 
                                         show="tree headings", height=20)
        self.tree_activos.heading("cuenta", text="Cuenta")
        self.tree_activos.heading("saldo", text="Saldo")
        self.tree_activos.column("#0", width=30)
        self.tree_activos.column("cuenta", width=250)
        self.tree_activos.column("saldo", width=120, anchor="e")
        self.tree_activos.pack(fill="both", expand=True)

        # Pasivos y Patrimonio
        frm_pasivos = ttk.LabelFrame(frm_main, text="PASIVOS Y PATRIMONIO", padding=10)
        frm_pasivos.pack(side="left", fill="both", expand=True, padx=5)
        self.tree_pasivos = ttk.Treeview(frm_pasivos, columns=("cuenta", "saldo"), 
                                         show="tree headings", height=20)
        self.tree_pasivos.heading("cuenta", text="Cuenta")
        self.tree_pasivos.heading("saldo", text="Saldo")
        self.tree_pasivos.column("#0", width=30)
        self.tree_pasivos.column("cuenta", width=250)
        self.tree_pasivos.column("saldo", width=120, anchor="e")
        self.tree_pasivos.pack(fill="both", expand=True)

    def generar_reporte(self):
        for item in self.tree_activos.get_children():
            self.tree_activos.delete(item)
        for item in self.tree_pasivos.get_children():
            self.tree_pasivos.delete(item)

        cuentas = self.model.get_estado_situacion_financiera()

        activos_corrientes = []
        activos_no_corrientes = []
        pasivos_corrientes = []
        pasivos_no_corrientes = []
        patrimonio = []

        for codigo, nombre, elemento, categoria, debe, haber in cuentas:
            if elemento == 'Activo':
                saldo = debe - haber
                if saldo != 0:
                    if 'Corriente' in categoria:
                        activos_corrientes.append((codigo, nombre, saldo))
                    else:
                        activos_no_corrientes.append((codigo, nombre, saldo))
            elif elemento == 'Pasivo':
                saldo = haber - debe
                if saldo != 0:
                    if 'Corriente' in categoria:
                        pasivos_corrientes.append((codigo, nombre, saldo))
                    else:
                        pasivos_no_corrientes.append((codigo, nombre, saldo))
            elif elemento == 'Patrimonio':
                saldo = haber - debe
                if saldo != 0:
                    patrimonio.append((codigo, nombre, saldo))

        # Insertar activos
        if activos_corrientes:
            parent_ac = self.tree_activos.insert("", "end", text="", 
                                                 values=("ACTIVOS CORRIENTES", ""), tags=("bold",))
            total_ac = sum(s for _, _, s in activos_corrientes)
            for codigo, nombre, saldo in activos_corrientes:
                self.tree_activos.insert(parent_ac, "end", text="", 
                                        values=(f"{codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree_activos.insert(parent_ac, "end", text="", 
                                    values=("Total Activos Corrientes", f"${total_ac:,.0f}"), 
                                    tags=("total",))

        if activos_no_corrientes:
            parent_anc = self.tree_activos.insert("", "end", text="", 
                                                  values=("ACTIVOS NO CORRIENTES", ""), tags=("bold",))
            total_anc = sum(s for _, _, s in activos_no_corrientes)
            for codigo, nombre, saldo in activos_no_corrientes:
                self.tree_activos.insert(parent_anc, "end", text="", 
                                        values=(f"{codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree_activos.insert(parent_anc, "end", text="", 
                                    values=("Total Activos No Corrientes", f"${total_anc:,.0f}"), 
                                    tags=("total",))

        total_activos = sum(s for _, _, s in activos_corrientes) + sum(s for _, _, s in activos_no_corrientes)
        self.tree_activos.insert("", "end", text="", 
                                values=("TOTAL ACTIVOS", f"${total_activos:,.0f}"), 
                                tags=("grand_total",))

        # Insertar pasivos y patrimonio
        if pasivos_corrientes:
            parent_pc = self.tree_pasivos.insert("", "end", text="", 
                                                 values=("PASIVOS CORRIENTES", ""), tags=("bold",))
            total_pc = sum(s for _, _, s in pasivos_corrientes)
            for codigo, nombre, saldo in pasivos_corrientes:
                self.tree_pasivos.insert(parent_pc, "end", text="", 
                                        values=(f"{codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree_pasivos.insert(parent_pc, "end", text="", 
                                    values=("Total Pasivos Corrientes", f"${total_pc:,.0f}"), 
                                    tags=("total",))

        if pasivos_no_corrientes:
            parent_pnc = self.tree_pasivos.insert("", "end", text="", 
                                                  values=("PASIVOS NO CORRIENTES", ""), tags=("bold",))
            total_pnc = sum(s for _, _, s in pasivos_no_corrientes)
            for codigo, nombre, saldo in pasivos_no_corrientes:
                self.tree_pasivos.insert(parent_pnc, "end", text="", 
                                        values=(f"{codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree_pasivos.insert(parent_pnc, "end", text="", 
                                    values=("Total Pasivos No Corrientes", f"${total_pnc:,.0f}"), 
                                    tags=("total",))

        if patrimonio:
            parent_pat = self.tree_pasivos.insert("", "end", text="", 
                                                  values=("PATRIMONIO", ""), tags=("bold",))
            total_pat = sum(s for _, _, s in patrimonio)
            for codigo, nombre, saldo in patrimonio:
                self.tree_pasivos.insert(parent_pat, "end", text="", 
                                        values=(f"{codigo} - {nombre}", f"${saldo:,.0f}"))
            self.tree_pasivos.insert(parent_pat, "end", text="", 
                                    values=("Total Patrimonio", f"${total_pat:,.0f}"), 
                                    tags=("total",))

        total_pasivos_patrimonio = (sum(s for _, _, s in pasivos_corrientes) + 
                                    sum(s for _, _, s in pasivos_no_corrientes) + 
                                    sum(s for _, _, s in patrimonio))
        self.tree_pasivos.insert("", "end", text="", 
                                values=("TOTAL PASIVOS + PATRIMONIO", f"${total_pasivos_patrimonio:,.0f}"), 
                                tags=("grand_total",))

        # Estilos
        for tree in [self.tree_activos, self.tree_pasivos]:
            tree.tag_configure("bold", font=("Arial", 10, "bold"))
            tree.tag_configure("total", font=("Arial", 9, "bold"), background="#e0e0e0")
            tree.tag_configure("grand_total", font=("Arial", 11, "bold"), background="#c0c0c0")
