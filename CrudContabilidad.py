import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "comprobantes.db")
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS comprobantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            tipo TEXT NOT NULL,
            numero TEXT NOT NULL,
            descripcion TEXT,
            monto REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


class ComprobantesCRUD(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Comprobantes")
        self.geometry("800x500")
        self.resizable(True, True)
        self.create_widgets()
        self.load_comprobantes()

    def create_widgets(self):
        frm_form = ttk.Frame(self)
        frm_form.pack(fill="x", padx=10, pady=6)

        ttk.Label(frm_form, text="Fecha (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
        self.ent_fecha = ttk.Entry(frm_form)
        self.ent_fecha.grid(row=0, column=1, padx=4, pady=2, sticky="we")
        self.ent_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))

        ttk.Label(frm_form, text="Tipo:").grid(row=0, column=2, sticky="w")
        self.ent_tipo = ttk.Entry(frm_form)
        self.ent_tipo.grid(row=0, column=3, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Número:").grid(row=1, column=0, sticky="w")
        self.ent_numero = ttk.Entry(frm_form)
        self.ent_numero.grid(row=1, column=1, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Descripción:").grid(row=1, column=2, sticky="w")
        self.ent_descripcion = ttk.Entry(frm_form)
        self.ent_descripcion.grid(row=1, column=3, padx=4, pady=2, sticky="we")

        ttk.Label(frm_form, text="Monto:").grid(row=2, column=0, sticky="w")
        self.ent_monto = ttk.Entry(frm_form)
        self.ent_monto.grid(row=2, column=1, padx=4, pady=2, sticky="we")

        for i in range(4):
            frm_form.grid_columnconfigure(i, weight=1)

        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=6)

        self.btn_agregar = ttk.Button(frm_buttons, text="Agregar", command=self.agregar)
        self.btn_agregar.pack(side="left", padx=4)

        self.btn_actualizar = ttk.Button(frm_buttons, text="Actualizar", command=self.actualizar)
        self.btn_actualizar.pack(side="left", padx=4)

        self.btn_eliminar = ttk.Button(frm_buttons, text="Eliminar", command=self.eliminar)
        self.btn_eliminar.pack(side="left", padx=4)

        self.btn_limpiar = ttk.Button(frm_buttons, text="Limpiar campos", command=self.limpiar_campos)
        self.btn_limpiar.pack(side="left", padx=4)

        # Treeview
        columns = ("id", "fecha", "tipo", "numero", "descripcion", "monto")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("numero", text="Número")
        self.tree.heading("descripcion", text="Descripción")
        self.tree.heading("monto", text="Monto")
        self.tree.pack(fill="both", expand=True, padx=10, pady=6)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def run_query(self, query, params=()):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        rows = c.fetchall()
        conn.close()
        return rows

    def load_comprobantes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        rows = self.run_query("SELECT id, fecha, tipo, numero, descripcion, monto FROM comprobantes ORDER BY id DESC")
        for r in rows:
            self.tree.insert("", "end", values=r)

    def validar_campos(self):
        fecha = self.ent_fecha.get().strip()
        tipo = self.ent_tipo.get().strip()
        numero = self.ent_numero.get().strip()
        monto = self.ent_monto.get().strip()
        if not fecha or not tipo or not numero or not monto:
            messagebox.showwarning("Validación", "Fecha, Tipo, Número y Monto son obligatorios.")
            return False
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Validación", "Fecha debe tener formato YYYY-MM-DD.")
            return False
        try:
            float(monto)
        except ValueError:
            messagebox.showwarning("Validación", "Monto debe ser numérico.")
            return False
        return True

    def agregar(self):
        if not self.validar_campos():
            return
        fecha = self.ent_fecha.get().strip()
        tipo = self.ent_tipo.get().strip()
        numero = self.ent_numero.get().strip()
        descripcion = self.ent_descripcion.get().strip()
        monto = float(self.ent_monto.get().strip())
        self.run_query(
            "INSERT INTO comprobantes (fecha, tipo, numero, descripcion, monto) VALUES (?, ?, ?, ?, ?)",
            (fecha, tipo, numero, descripcion, monto),
        )
        self.load_comprobantes()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Comprobante agregado.")

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        # id, fecha, tipo, numero, descripcion, monto
        self.ent_fecha.delete(0, tk.END)
        self.ent_fecha.insert(0, vals[1])
        self.ent_tipo.delete(0, tk.END)
        self.ent_tipo.insert(0, vals[2])
        self.ent_numero.delete(0, tk.END)
        self.ent_numero.insert(0, vals[3])
        self.ent_descripcion.delete(0, tk.END)
        self.ent_descripcion.insert(0, vals[4])
        self.ent_monto.delete(0, tk.END)
        self.ent_monto.insert(0, vals[5])

    def actualizar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un comprobante para actualizar.")
            return
        if not self.validar_campos():
            return
        item = self.tree.item(sel[0], "values")
        id_ = item[0]
        fecha = self.ent_fecha.get().strip()
        tipo = self.ent_tipo.get().strip()
        numero = self.ent_numero.get().strip()
        descripcion = self.ent_descripcion.get().strip()
        monto = float(self.ent_monto.get().strip())
        self.run_query(
            "UPDATE comprobantes SET fecha = ?, tipo = ?, numero = ?, descripcion = ?, monto = ? WHERE id = ?",
            (fecha, tipo, numero, descripcion, monto, id_),
        )
        self.load_comprobantes()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Comprobante actualizado.")

    def eliminar(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un comprobante para eliminar.")
            return
        item = self.tree.item(sel[0], "values")
        id_ = item[0]
        if messagebox.askyesno("Confirmar", f"¿Eliminar comprobante ID {id_}?"):
            self.run_query("DELETE FROM comprobantes WHERE id = ?", (id_,))
            self.load_comprobantes()
            self.limpiar_campos()
            messagebox.showinfo("Eliminado", "Comprobante eliminado.")

    def limpiar_campos(self):
        self.ent_fecha.delete(0, tk.END)
        self.ent_fecha.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.ent_tipo.delete(0, tk.END)
        self.ent_numero.delete(0, tk.END)
        self.ent_descripcion.delete(0, tk.END)
        self.ent_monto.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Menú Principal")
        self.geometry("350x260")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self, padding=20)
        frm.pack(expand=True, fill="both")

        btn_comprobantes = ttk.Button(frm, text="Comprobantes", command=self.open_comprobantes, width=30)
        btn_comprobantes.pack(pady=6)

        btn_plan = ttk.Button(frm, text="Plan de cuentas (deshabilitado)", state="disabled", width=30)
        btn_plan.pack(pady=6)

        btn_esf = ttk.Button(frm, text="Estado de Situación Financiera (deshabilitado)", state="disabled", width=30)
        btn_esf.pack(pady=6)

        btn_er = ttk.Button(frm, text="Estado de Resultados (deshabilitado)", state="disabled", width=30)
        btn_er.pack(pady=6)

        btn_lc = ttk.Button(frm, text="Libro de Compras (deshabilitado)", state="disabled", width=30)
        btn_lc.pack(pady=6)

        btn_lv = ttk.Button(frm, text="Libro de Ventas (deshabilitado)", state="disabled", width=30)
        btn_lv.pack(pady=6)

    def open_comprobantes(self):
        # Evita abrir múltiples instancias
        for w in self.winfo_children():
            if isinstance(w, ComprobantesCRUD):
                w.lift()
                return
        ComprobantesCRUD(self)


if __name__ == "__main__":
    init_db()
    app = MainApp()
    app.mainloop()