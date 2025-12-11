"""
Vista de Comprobantes Contables
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.comprobantes import ComprobantesModel
from models.plan_cuentas import PlanCuentasModel
from config import DATE_FORMAT


class ComprobantesView(tk.Toplevel):
    """Ventana de gestión de Comprobantes Contables"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master_window = master
        self.title("Comprobantes Contables")
        self.geometry("1100x700")
        self.resizable(True, True)
        self.model = ComprobantesModel()
        self.plan_model = PlanCuentasModel()
        self.detalle_lineas = []
        self.create_widgets()
        self.load_comprobantes()
        self.load_cuentas()
        
        # Ocultar ventana principal
        if self.master_window:
            self.master_window.withdraw()
        
        # Manejar el cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame superior: Datos del comprobante
        frm_header = ttk.LabelFrame(self, text="Datos del Comprobante", padding=10)
        frm_header.pack(fill="x", padx=10, pady=6)

        ttk.Label(frm_header, text="Número:").grid(row=0, column=0, sticky="w")
        self.lbl_numero = ttk.Label(frm_header, text="(automático)", foreground="gray")
        self.lbl_numero.grid(row=0, column=1, sticky="w", padx=4)

        ttk.Label(frm_header, text="Fecha:").grid(row=0, column=2, sticky="w", padx=(20, 0))
        self.ent_fecha = ttk.Entry(frm_header, width=15)
        self.ent_fecha.grid(row=0, column=3, sticky="w", padx=4)
        self.ent_fecha.insert(0, datetime.today().strftime(DATE_FORMAT))

        ttk.Label(frm_header, text="Glosa:").grid(row=1, column=0, sticky="w")
        self.ent_glosa = ttk.Entry(frm_header, width=60)
        self.ent_glosa.grid(row=1, column=1, columnspan=3, sticky="we", padx=4, pady=4)

        # Frame detalle
        frm_detalle = ttk.LabelFrame(self, text="Detalle del Comprobante", padding=10)
        frm_detalle.pack(fill="both", expand=True, padx=10, pady=6)

        frm_add_line = ttk.Frame(frm_detalle)
        frm_add_line.pack(fill="x", pady=4)

        ttk.Label(frm_add_line, text="Cuenta:").pack(side="left", padx=2)
        self.combo_cuenta = ttk.Combobox(frm_add_line, width=40, state="readonly")
        self.combo_cuenta.pack(side="left", padx=2)

        ttk.Label(frm_add_line, text="Debe:").pack(side="left", padx=2)
        self.ent_debe = ttk.Entry(frm_add_line, width=12)
        self.ent_debe.pack(side="left", padx=2)
        self.ent_debe.insert(0, "0")

        ttk.Label(frm_add_line, text="Haber:").pack(side="left", padx=2)
        self.ent_haber = ttk.Entry(frm_add_line, width=12)
        self.ent_haber.pack(side="left", padx=2)
        self.ent_haber.insert(0, "0")

        ttk.Button(frm_add_line, text="Agregar Línea", command=self.agregar_linea).pack(side="left", padx=4)

        # Treeview de detalle
        columns_det = ("linea", "codigo", "cuenta", "debe", "haber")
        self.tree_detalle = ttk.Treeview(frm_detalle, columns=columns_det, show="headings", height=8)
        for col, text, width in [("linea", "Línea", 50), ("codigo", "Código", 80), 
                                  ("cuenta", "Cuenta", 300), ("debe", "Debe", 100), 
                                  ("haber", "Haber", 100)]:
            self.tree_detalle.heading(col, text=text)
            self.tree_detalle.column(col, width=width)
        self.tree_detalle.pack(fill="both", expand=True, pady=4)

        frm_total = ttk.Frame(frm_detalle)
        frm_total.pack(fill="x", pady=4)

        self.lbl_total = ttk.Label(frm_total, text="Total Debe: $0  |  Total Haber: $0  |  Diferencia: $0", 
                                   font=("Arial", 10, "bold"))
        self.lbl_total.pack(side="left")

        ttk.Button(frm_total, text="Quitar Línea", command=self.quitar_linea).pack(side="right", padx=4)

        # Botones principales
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=6)

        ttk.Button(frm_buttons, text="Guardar Comprobante", command=self.guardar_comprobante).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="← Volver al Menú", command=self.on_closing).pack(side="right", padx=4)

        # Lista de comprobantes
        frm_list = ttk.LabelFrame(self, text="Comprobantes Guardados", padding=10)
        frm_list.pack(fill="both", expand=True, padx=10, pady=6)

        columns_comp = ("numero", "fecha", "glosa")
        self.tree_comprobantes = ttk.Treeview(frm_list, columns=columns_comp, show="headings", height=6)
        for col, text, width in [("numero", "Número", 80), ("fecha", "Fecha", 100), 
                                 ("glosa", "Glosa", 400)]:
            self.tree_comprobantes.heading(col, text=text)
            self.tree_comprobantes.column(col, width=width)
        self.tree_comprobantes.pack(fill="both", expand=True)
        self.tree_comprobantes.bind("<<TreeviewSelect>>", self.on_comprobante_select)

    def load_cuentas(self):
        """Carga las cuentas para el combobox"""
        self.cuentas_dict = self.plan_model.get_for_combo()
        self.combo_cuenta['values'] = list(self.cuentas_dict.keys())

    def load_comprobantes(self):
        """Carga los comprobantes en el treeview"""
        for row in self.tree_comprobantes.get_children():
            self.tree_comprobantes.delete(row)
        
        comprobantes = self.model.get_all()
        for comp in comprobantes:
            self.tree_comprobantes.insert("", "end", values=comp)

    def agregar_linea(self):
        """Agrega una línea al detalle del comprobante"""
        cuenta_sel = self.combo_cuenta.get()
        if not cuenta_sel:
            messagebox.showwarning("Validación", "Seleccione una cuenta.")
            return

        try:
            debe = float(self.ent_debe.get())
            haber = float(self.ent_haber.get())
        except ValueError:
            messagebox.showwarning("Validación", "Debe y Haber deben ser numéricos.")
            return

        if debe == 0 and haber == 0:
            messagebox.showwarning("Validación", "Debe o Haber debe ser mayor a 0.")
            return

        codigo = self.cuentas_dict[cuenta_sel]
        nombre = cuenta_sel.split(" - ")[1]
        linea = len(self.detalle_lineas) + 1

        self.detalle_lineas.append({
            'linea': linea, 'codigo': codigo, 'nombre': nombre,
            'debe': debe, 'haber': haber
        })

        self.tree_detalle.insert("", "end", values=(linea, codigo, nombre, f"{debe:,.0f}", f"{haber:,.0f}"))
        self.actualizar_totales()

        self.ent_debe.delete(0, tk.END)
        self.ent_debe.insert(0, "0")
        self.ent_haber.delete(0, tk.END)
        self.ent_haber.insert(0, "0")

    def quitar_linea(self):
        """Quita una línea del detalle"""
        sel = self.tree_detalle.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una línea para quitar.")
            return

        item = self.tree_detalle.item(sel[0], "values")
        linea = int(item[0])

        self.detalle_lineas = [l for l in self.detalle_lineas if l['linea'] != linea]
        for i, l in enumerate(self.detalle_lineas):
            l['linea'] = i + 1

        self.tree_detalle.delete(sel[0])
        self.actualizar_totales()

    def actualizar_totales(self):
        """Actualiza los totales del comprobante"""
        total_debe = sum(l['debe'] for l in self.detalle_lineas)
        total_haber = sum(l['haber'] for l in self.detalle_lineas)
        diferencia = total_debe - total_haber

        self.lbl_total.config(
            text=f"Total Debe: ${total_debe:,.0f}  |  Total Haber: ${total_haber:,.0f}  |  Diferencia: ${diferencia:,.0f}",
            foreground="green" if diferencia == 0 else "red"
        )

    def guardar_comprobante(self):
        """Guarda el comprobante en la base de datos"""
        fecha = self.ent_fecha.get().strip()
        glosa = self.ent_glosa.get().strip()

        if not fecha or not glosa:
            messagebox.showwarning("Validación", "Fecha y Glosa son obligatorios.")
            return

        if not self.detalle_lineas:
            messagebox.showwarning("Validación", "Debe agregar al menos una línea.")
            return

        total_debe = sum(l['debe'] for l in self.detalle_lineas)
        total_haber = sum(l['haber'] for l in self.detalle_lineas)

        if total_debe != total_haber:
            messagebox.showerror("Error", "El comprobante no está balanceado. Debe = Haber")
            return

        try:
            numero = self.model.create(fecha, glosa, self.detalle_lineas)
            messagebox.showinfo("Éxito", f"Comprobante #{numero} guardado correctamente.")
            self.load_comprobantes()
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el comprobante: {str(e)}")

    def on_comprobante_select(self, event):
        """Maneja la selección de un comprobante"""
        sel = self.tree_comprobantes.selection()
        if not sel:
            return

        vals = self.tree_comprobantes.item(sel[0], "values")
        numero = vals[0]

        comp = self.model.get_by_numero(numero)
        detalles = self.model.get_detalle(numero)

        self.limpiar_campos()
        self.lbl_numero.config(text=str(numero))
        self.ent_fecha.insert(0, comp[1])
        self.ent_glosa.insert(0, comp[2])

        for det in detalles:
            self.detalle_lineas.append({
                'linea': det[0], 'codigo': det[1], 'nombre': det[2],
                'debe': det[3], 'haber': det[4]
            })
            self.tree_detalle.insert("", "end", values=(det[0], det[1], det[2], 
                                                        f"{det[3]:,.0f}", f"{det[4]:,.0f}"))

        self.actualizar_totales()

    def limpiar_campos(self):
        """Limpia todos los campos"""
        self.lbl_numero.config(text="(automático)")
        self.ent_fecha.delete(0, tk.END)
        self.ent_fecha.insert(0, datetime.today().strftime(DATE_FORMAT))
        self.ent_glosa.delete(0, tk.END)
        self.detalle_lineas = []
        for row in self.tree_detalle.get_children():
            self.tree_detalle.delete(row)
        self.actualizar_totales()
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.master_window:
            self.master_window.deiconify()
        self.destroy()
