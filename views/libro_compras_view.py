"""
Vista del Libro de Compras
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from models.libro_compras import LibroComprasModel
from config import DATE_FORMAT, TIPOS_DOCUMENTO
from utils.helpers import calculate_iva


class LibroComprasView(tk.Toplevel):
    """Vista del Libro de Compras"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.master_window = master
        self.title("Libro de Compras")
        self.geometry("1100x600")
        self.resizable(True, True)
        self.model = LibroComprasModel()
        self.create_widgets()
        self.load_compras()
        
        # Ocultar ventana principal
        if self.master_window:
            self.master_window.withdraw()
        
        # Manejar el cierre de la ventana
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        frm_form = ttk.LabelFrame(self, text="Registrar Compra", padding=10)
        frm_form.pack(fill="x", padx=10, pady=6)

        ttk.Label(frm_form, text="Fecha:").grid(row=0, column=0, sticky="w")
        self.ent_fecha = DateEntry(frm_form, width=12, background='darkblue',
                                   foreground='white', borderwidth=2,
                                   date_pattern='yyyy-mm-dd')
        self.ent_fecha.grid(row=0, column=1, padx=4, pady=2, sticky="w")

        ttk.Label(frm_form, text="Tipo Doc:").grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.combo_tipo = ttk.Combobox(frm_form, values=TIPOS_DOCUMENTO, width=15)
        self.combo_tipo.grid(row=0, column=3, padx=4, pady=2, sticky="w")
        self.combo_tipo.set("Factura")

        ttk.Label(frm_form, text="N° Doc:").grid(row=0, column=4, sticky="w", padx=(10, 0))
        self.ent_numero = ttk.Entry(frm_form, width=12)
        self.ent_numero.grid(row=0, column=5, padx=4, pady=2, sticky="w")

        ttk.Label(frm_form, text="RUT Proveedor:").grid(row=1, column=0, sticky="w")
        self.ent_rut = ttk.Entry(frm_form, width=12)
        self.ent_rut.grid(row=1, column=1, padx=4, pady=2, sticky="w")

        ttk.Label(frm_form, text="Razón Social:").grid(row=1, column=2, sticky="w", padx=(10, 0))
        self.ent_razon = ttk.Entry(frm_form, width=40)
        self.ent_razon.grid(row=1, column=3, columnspan=3, padx=4, pady=2, sticky="we")

        # Exenta de IVA
        self.var_exenta = tk.BooleanVar(value=False)
        self.chk_exenta = ttk.Checkbutton(frm_form, text="Exenta de IVA", variable=self.var_exenta,
                          command=self.toggle_exenta)
        self.chk_exenta.grid(row=1, column=6, padx=8, pady=2, sticky="w")

        ttk.Label(frm_form, text="Neto:").grid(row=2, column=0, sticky="w")
        self.ent_neto = ttk.Entry(frm_form, width=12)
        self.ent_neto.grid(row=2, column=1, padx=4, pady=2, sticky="w")
        self.ent_neto.bind("<KeyRelease>", self.calcular_total)

        ttk.Label(frm_form, text="IVA:").grid(row=2, column=2, sticky="w", padx=(10, 0))
        self.ent_iva = ttk.Entry(frm_form, width=12)
        self.ent_iva.grid(row=2, column=3, padx=4, pady=2, sticky="w")

        ttk.Label(frm_form, text="Total:").grid(row=2, column=4, sticky="w", padx=(10, 0))
        self.ent_total = ttk.Entry(frm_form, width=12)
        self.ent_total.grid(row=2, column=5, padx=4, pady=2, sticky="w")

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=6)
        ttk.Button(frm_buttons, text="Guardar", command=self.guardar).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="← Volver al Menú", command=self.on_closing).pack(side="right", padx=4)

        # Frame de filtros
        frm_filtros = ttk.LabelFrame(self, text="Filtrar por Fecha")
        frm_filtros.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frm_filtros, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.filtro_desde = DateEntry(frm_filtros, width=12, background='darkblue',
                                      foreground='white', borderwidth=2,
                                      date_pattern='yyyy-mm-dd')
        self.filtro_desde.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frm_filtros, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.filtro_hasta = DateEntry(frm_filtros, width=12, background='darkblue',
                                      foreground='white', borderwidth=2,
                                      date_pattern='yyyy-mm-dd')
        self.filtro_hasta.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frm_filtros, text="Filtrar",
                  command=self.aplicar_filtro).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frm_filtros, text="Mostrar Todas",
                  command=self.load_compras).grid(row=0, column=5, padx=5, pady=5)

        columns = ("id", "fecha", "tipo", "numero", "rut", "razon_social", "exenta", "neto", "iva", "total", "comprobante")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        widths = [40, 80, 80, 80, 90, 160, 70, 80, 80, 80, 90]
        headers = ["ID", "Fecha", "Tipo", "N° Doc", "RUT", "Razón Social", "Exenta", "Neto", "IVA", "Total", "N° Comp"]
        for col, width, header in zip(columns, widths, headers):
            self.tree.heading(col, text=header)
            self.tree.column(col, width=width, anchor="center" if width < 100 else "w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def calcular_total(self, event=None):
        try:
            neto = float(self.ent_neto.get())
            if self.var_exenta.get():
                iva = 0.0
                total = neto
            else:
                iva = calculate_iva(neto)
                total = neto + iva
            self.ent_iva.delete(0, tk.END)
            self.ent_iva.insert(0, f"{iva:.0f}")
            self.ent_total.delete(0, tk.END)
            self.ent_total.insert(0, f"{total:.0f}")
        except:
            pass

    def toggle_exenta(self):
        """Activa/desactiva el modo exento y recalcula"""
        if self.var_exenta.get():
            self.ent_iva.config(state="disabled")
        else:
            self.ent_iva.config(state="normal")
        self.calcular_total()

    def load_compras(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        compras = self.model.get_all()
        for c in compras:
            comp_num = f"#{c[10]}" if c[10] else "-"
            exenta_txt = "Sí" if c[9] else "No"
            self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4], c[5], exenta_txt,
                                               f"{c[6]:,.0f}", f"{c[7]:,.0f}", f"{c[8]:,.0f}", comp_num))

    def guardar(self):
        try:
            fecha = self.ent_fecha.get().strip()
            tipo = self.combo_tipo.get().strip()
            numero = self.ent_numero.get().strip()
            rut = self.ent_rut.get().strip()
            razon = self.ent_razon.get().strip()
            neto = float(self.ent_neto.get())
            iva = float(self.ent_iva.get())
            total = float(self.ent_total.get())

            if not all([fecha, tipo, numero, rut, razon]):
                messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
                return

            exenta = 1 if self.var_exenta.get() else 0
            num_comprobante = self.model.create(fecha, tipo, numero, rut, razon, neto, iva, total, exenta)
            self.load_compras()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Compra registrada correctamente.\nComprobante #{num_comprobante} generado automáticamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la compra: {str(e)}")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        # Convertir fecha string a objeto datetime
        fecha_obj = datetime.strptime(vals[1], '%Y-%m-%d')
        self.ent_fecha.set_date(fecha_obj)
        self.combo_tipo.set(vals[2])
        self.ent_numero.delete(0, tk.END)
        self.ent_numero.insert(0, vals[3])
        self.ent_rut.delete(0, tk.END)
        self.ent_rut.insert(0, vals[4])
        self.ent_razon.delete(0, tk.END)
        self.ent_razon.insert(0, vals[5])
        self.ent_neto.delete(0, tk.END)
        self.ent_neto.insert(0, vals[6].replace(",", ""))
        # Exenta
        exenta_val = vals[6]
        self.var_exenta.set(exenta_val == "Sí")
        self.toggle_exenta()
        self.ent_iva.delete(0, tk.END)
        self.ent_iva.insert(0, vals[8].replace(",", ""))
        self.ent_total.delete(0, tk.END)
        self.ent_total.insert(0, vals[9].replace(",", ""))

    def eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una compra para eliminar.")
            return
        item = self.tree.item(sel[0], "values")
        if messagebox.askyesno("Confirmar", f"¿Eliminar compra ID {item[0]}?"):
            try:
                self.model.delete(item[0])
                self.load_compras()
                self.limpiar_campos()
                messagebox.showinfo("Eliminado", "Compra eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

    def aplicar_filtro(self):
        """Filtra las compras por rango de fechas"""
        fecha_desde = self.filtro_desde.get_date().strftime('%Y-%m-%d')
        fecha_hasta = self.filtro_hasta.get_date().strftime('%Y-%m-%d')
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        compras = self.model.get_all()
        for c in compras:
            if fecha_desde <= c[1] <= fecha_hasta:
                comp_num = f"#{c[10]}" if c[10] else "-"
                exenta_txt = "Sí" if c[9] else "No"
                self.tree.insert("", "end", values=(c[0], c[1], c[2], c[3], c[4], c[5], exenta_txt,
                                                   f"{c[6]:,.0f}", f"{c[7]:,.0f}", f"{c[8]:,.0f}", comp_num))
    
    def limpiar_campos(self):
        self.ent_fecha.set_date(datetime.today())
        self.combo_tipo.set("Factura")
        self.var_exenta.set(False)
        self.toggle_exenta()
        for entry in [self.ent_numero, self.ent_rut, self.ent_razon, 
                     self.ent_neto, self.ent_iva, self.ent_total]:
            entry.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if self.master_window:
            self.master_window.deiconify()
        self.destroy()
