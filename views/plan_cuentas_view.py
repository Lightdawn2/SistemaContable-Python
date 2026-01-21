"""
Vista del Plan de Cuentas con selección jerárquica profesional:
Elemento → Subcategoría → Subcuenta (antes "Grupo").
Las listas dependen del Excel/NIIF y se filtran según la selección del usuario.
Códigos generados automáticamente siguiendo estándar NIIF/IFRS Chile: D.CC.SS.NNNN
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.plan_cuentas import PlanCuentasModel
from utils.accounting import (
    obtener_elementos,
    obtener_categorias,
    obtener_subcuentas,
    validar_estructura,
    generar_codigo_contable,
)



class PlanCuentasView(ttk.Frame):
    """Vista de gestión del Plan de Cuentas"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = PlanCuentasModel()
        # Migrar datos antiguos: mover categoría -> subcategoría y dejar categoría nula
        try:
            self.model.migrate_categoria_to_subcategoria()
        except Exception:
            # Si falla la migración, continuamos para no bloquear la UI
            pass
        self.create_widgets()
        self.load_cuentas()

    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Título
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=10)
        ttk.Label(header, text="Plan de Cuentas", 
                 font=("Arial", 14, "bold")).pack(side="left")
        
        # Frame del formulario
        frm_form = ttk.Frame(self)
        frm_form.pack(fill="x", padx=10, pady=6)

        ttk.Label(frm_form, text="Código:").grid(row=0, column=0, sticky="w")
        self.ent_codigo = ttk.Entry(frm_form, width=15, state="readonly")
        self.ent_codigo.grid(row=0, column=1, padx=4, pady=2, sticky="we")
        
        ttk.Label(frm_form, text="Nombre:").grid(row=0, column=2, sticky="w")
        self.ent_nombre = ttk.Entry(frm_form)
        self.ent_nombre.grid(row=0, column=3, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Elemento:").grid(row=1, column=0, sticky="w")
        self.combo_elemento = ttk.Combobox(frm_form, values=obtener_elementos(), state="readonly")
        self.combo_elemento.grid(row=1, column=1, padx=4, pady=2, sticky="we")
        self.combo_elemento.bind("<<ComboboxSelected>>", self.on_elemento_change)

        ttk.Label(frm_form, text="Subcategoría:").grid(row=1, column=2, sticky="w")
        self.combo_subcategoria = ttk.Combobox(frm_form, values=[], state="readonly")
        self.combo_subcategoria.grid(row=1, column=3, padx=4, pady=2, sticky="we")
        self.combo_subcategoria.bind("<<ComboboxSelected>>", self.on_subcategoria_change)

        ttk.Label(frm_form, text="Sub cuenta:").grid(row=2, column=0, sticky="w")
        self.combo_subcuenta = ttk.Combobox(frm_form, values=[], state="readonly")
        self.combo_subcuenta.grid(row=2, column=1, padx=4, pady=2, sticky="we")
        self.combo_subcuenta.bind("<<ComboboxSelected>>", self.on_subcuenta_change)

        ttk.Label(frm_form, text="").grid(row=2, column=2, sticky="w")  # placeholder para alineación
        ttk.Label(frm_form, text="").grid(row=2, column=3, sticky="w")

        for i in range(4):
            frm_form.grid_columnconfigure(i, weight=1)

        # Frame de botones
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=6)

        ttk.Button(frm_buttons, text="Agregar", command=self.agregar).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)
        ttk.Button(frm_buttons, text="Limpiar", command=self.limpiar_campos).pack(side="left", padx=4)

        # Treeview
        columns = ("codigo", "nombre", "elemento", "subcategoria", "subcuenta")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_cuentas(self):
        """Carga las cuentas en el treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        cuentas = self.model.get_all()
        for cuenta in cuentas:
            self.tree.insert("", "end", values=cuenta)

    def agregar(self):
        """Agrega una nueva cuenta"""
        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()
        elemento = self.combo_elemento.get().strip()
        subcategoria = self.combo_subcategoria.get().strip()
        subcuenta = self.combo_subcuenta.get().strip()

        if not codigo or not nombre or not elemento or not subcategoria:
            messagebox.showwarning("Validación", "Código, Nombre, Elemento y Subcategoría son obligatorios.")
            return

        if subcuenta and not validar_estructura(elemento, subcategoria, subcuenta):
            messagebox.showwarning("Validación", "La subcuenta no corresponde a la subcategoría seleccionada.")
            return

        try:
            self.model.create(codigo, nombre, elemento, subcategoria, subcuenta)
            self.load_cuentas()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Cuenta '{codigo}' agregada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar la cuenta: {str(e)}")

    def actualizar(self):
        """Actualiza la cuenta seleccionada"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una cuenta para actualizar.")
            return

        codigo = self.ent_codigo.get().strip()
        nombre = self.ent_nombre.get().strip()
        elemento = self.combo_elemento.get().strip()
        subcategoria = self.combo_subcategoria.get().strip()
        subcuenta = self.combo_subcuenta.get().strip()

        if not codigo or not nombre or not elemento or not subcategoria:
            messagebox.showwarning("Validación", "Código, Nombre, Elemento y Subcategoría son obligatorios.")
            return

        if subcuenta and not validar_estructura(elemento, subcategoria, subcuenta):
            messagebox.showwarning("Validación", "La subcuenta no corresponde a la subcategoría seleccionada.")
            return

        try:
            self.model.update(codigo, nombre, elemento, subcategoria, subcuenta)
            self.load_cuentas()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", f"Cuenta '{codigo}' actualizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la cuenta: {str(e)}")

    def eliminar(self):
        """Elimina la cuenta seleccionada"""
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una cuenta para eliminar.")
            return
        
        item = self.tree.item(sel[0], "values")
        codigo = item[0]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar cuenta {codigo}?"):
            try:
                self.model.delete(codigo)
                self.load_cuentas()
                self.limpiar_campos()
                messagebox.showinfo("Eliminado", "Cuenta eliminada correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar la cuenta: {str(e)}")

    def on_tree_select(self, event):
        """Maneja la selección en el treeview"""
        sel = self.tree.selection()
        if not sel:
            return
        
        vals = self.tree.item(sel[0], "values")
        self.ent_codigo.delete(0, tk.END)
        self.ent_codigo.insert(0, vals[0])
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, vals[1])
        self.combo_elemento.set(vals[2])
        self.on_elemento_change(None)  # actualizar subcategorías
        self.combo_subcategoria.set(vals[3])
        self.on_subcategoria_change(None)  # actualizar subcuentas
        self.combo_subcuenta.set(vals[4] if vals[4] else "")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.combo_elemento.set("")
        self.combo_subcategoria.set("")
        self.combo_subcuenta.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())

    def on_elemento_change(self, event):
        """Actualiza subcategorías al cambiar elemento"""
        elemento = self.combo_elemento.get()
        subcategorias = obtener_categorias(elemento)
        self.combo_subcategoria["values"] = subcategorias
        self.combo_subcategoria.set("")
        self.combo_subcuenta["values"] = []
        self.combo_subcuenta.set("")

    def on_subcategoria_change(self, event):
        """Actualiza subcuentas al cambiar subcategoría"""
        elemento = self.combo_elemento.get()
        subcategoria = self.combo_subcategoria.get()
        subcuentas = obtener_subcuentas(elemento, subcategoria)
        self.combo_subcuenta["values"] = subcuentas
        if subcuentas:
            self.combo_subcuenta.set(subcuentas[0])
        else:
            self.combo_subcuenta.set("")
        # Sugerir código automático
        self.sugerir_codigo()

    def on_subcuenta_change(self, event):
        """Actualiza sugerencia de código al cambiar subcuenta"""
        self.sugerir_codigo()

    def sugerir_codigo(self):
        """Sugiere el código automático basado en elemento, subcategoría y subcuenta"""
        elemento = self.combo_elemento.get()
        subcategoria = self.combo_subcategoria.get()
        subcuenta = self.combo_subcuenta.get()
        
        if elemento and subcategoria and subcuenta:
            codigo_sugerido = generar_codigo_contable(elemento, subcategoria, subcuenta)
            # Cambiar a estado normal para escribir, luego volver a readonly
            self.ent_codigo.config(state="normal")
            self.ent_codigo.delete(0, tk.END)
            self.ent_codigo.insert(0, codigo_sugerido)
            self.ent_codigo.config(state="readonly")
