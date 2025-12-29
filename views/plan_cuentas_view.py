"""
Vista del Plan de Cuentas
"""
import tkinter as tk
from tkinter import ttk, messagebox
from models.plan_cuentas import PlanCuentasModel
from config import ELEMENTOS


class PlanCuentasView(ttk.Frame):
    """Vista de gestión del Plan de Cuentas"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = PlanCuentasModel()
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
        self.ent_codigo = ttk.Entry(frm_form)
        self.ent_codigo.grid(row=0, column=1, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Nombre:").grid(row=0, column=2, sticky="w")
        self.ent_nombre = ttk.Entry(frm_form)
        self.ent_nombre.grid(row=0, column=3, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Elemento:").grid(row=1, column=0, sticky="w")
        self.combo_elemento = ttk.Combobox(frm_form, values=ELEMENTOS)
        self.combo_elemento.grid(row=1, column=1, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Categoría:").grid(row=1, column=2, sticky="w")
        self.ent_categoria = ttk.Entry(frm_form)
        self.ent_categoria.grid(row=1, column=3, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Subcategoría:").grid(row=2, column=0, sticky="w")
        self.ent_subcategoria = ttk.Entry(frm_form)
        self.ent_subcategoria.grid(row=2, column=1, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Grupo:").grid(row=2, column=2, sticky="w")
        self.ent_grupo = ttk.Entry(frm_form)
        self.ent_grupo.grid(row=2, column=3, padx=4, pady=2, sticky="we")

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
        columns = ("codigo", "nombre", "elemento", "categoria", "subcategoria", "grupo")
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
        categoria = self.ent_categoria.get().strip()
        subcategoria = self.ent_subcategoria.get().strip()
        grupo = self.ent_grupo.get().strip()

        if not codigo or not nombre or not elemento or not categoria:
            messagebox.showwarning("Validación", "Código, Nombre, Elemento y Categoría son obligatorios.")
            return

        try:
            self.model.create(int(codigo), nombre, elemento, categoria, subcategoria, grupo)
            self.load_cuentas()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Cuenta agregada correctamente.")
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
        categoria = self.ent_categoria.get().strip()
        subcategoria = self.ent_subcategoria.get().strip()
        grupo = self.ent_grupo.get().strip()

        if not codigo or not nombre or not elemento or not categoria:
            messagebox.showwarning("Validación", "Código, Nombre, Elemento y Categoría son obligatorios.")
            return

        try:
            self.model.update(int(codigo), nombre, elemento, categoria, subcategoria, grupo)
            self.load_cuentas()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Cuenta actualizada correctamente.")
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
        self.ent_categoria.delete(0, tk.END)
        self.ent_categoria.insert(0, vals[3])
        self.ent_subcategoria.delete(0, tk.END)
        self.ent_subcategoria.insert(0, vals[4] if vals[4] else "")
        self.ent_grupo.delete(0, tk.END)
        self.ent_grupo.insert(0, vals[5] if vals[5] else "")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.ent_codigo.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.combo_elemento.set("")
        self.ent_categoria.delete(0, tk.END)
        self.ent_subcategoria.delete(0, tk.END)
        self.ent_grupo.delete(0, tk.END)
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
