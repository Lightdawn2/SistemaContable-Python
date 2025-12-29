"""
Vista del Libro Diario
"""
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from models.libro_diario import LibroDiarioModel


class LibroDiarioView(ttk.Frame):
    """Vista del Libro Diario - Detalle cronológico de movimientos"""
    
    def __init__(self, master=None):
        super().__init__(master)
        self.model = LibroDiarioModel()
        self.create_widgets()
        self.cargar_libro_diario()

    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame del encabezado
        frm_header = ttk.Frame(self)
        frm_header.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(frm_header, text="LIBRO DIARIO - Detalle de Movimientos", 
                 font=("Arial", 14, "bold")).pack()
        
        # Frame de filtros
        frm_filtros = ttk.LabelFrame(self, text="Filtros de Fecha")
        frm_filtros.pack(fill="x", padx=10, pady=5)
        
        # Fecha desde
        ttk.Label(frm_filtros, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
        self.fecha_desde = DateEntry(frm_filtros, width=12, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='yyyy-mm-dd')
        self.fecha_desde.grid(row=0, column=1, padx=5, pady=5)
        
        # Fecha hasta
        ttk.Label(frm_filtros, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
        self.fecha_hasta = DateEntry(frm_filtros, width=12, background='darkblue',
                                     foreground='white', borderwidth=2,
                                     date_pattern='yyyy-mm-dd')
        self.fecha_hasta.grid(row=0, column=3, padx=5, pady=5)
        
        # Botones de filtro
        ttk.Button(frm_filtros, text="Filtrar",
                  command=self.aplicar_filtro).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(frm_filtros, text="Limpiar Filtros",
                  command=self.limpiar_filtros).grid(row=0, column=5, padx=5, pady=5)
        
        # Frame para la tabla con scrollbars
        frm_tabla = ttk.Frame(self)
        frm_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Scrollbars
        vsb = ttk.Scrollbar(frm_tabla, orient="vertical")
        hsb = ttk.Scrollbar(frm_tabla, orient="horizontal")
        
        # Treeview con todas las columnas del libro diario
        columns = ("fecha", "numero", "glosa", "codigo", "cuenta", "debe", "haber")
        self.tree = ttk.Treeview(frm_tabla, columns=columns, show="headings",
                                yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading("fecha", text="Fecha")
        self.tree.column("fecha", width=100, anchor="center")
        
        self.tree.heading("numero", text="N° Comp.")
        self.tree.column("numero", width=80, anchor="center")
        
        self.tree.heading("glosa", text="Glosa")
        self.tree.column("glosa", width=300, anchor="w")
        
        self.tree.heading("codigo", text="Código")
        self.tree.column("codigo", width=80, anchor="center")
        
        self.tree.heading("cuenta", text="Cuenta")
        self.tree.column("cuenta", width=250, anchor="w")
        
        self.tree.heading("debe", text="Debe")
        self.tree.column("debe", width=120, anchor="e")
        
        self.tree.heading("haber", text="Haber")
        self.tree.column("haber", width=120, anchor="e")
        
        # Grid
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        frm_tabla.grid_rowconfigure(0, weight=1)
        frm_tabla.grid_columnconfigure(0, weight=1)

        # Frame de totales
        frm_totales = ttk.Frame(self)
        frm_totales.pack(fill="x", padx=10, pady=10)
        
        self.lbl_totales = ttk.Label(frm_totales, 
                                     text="",
                                     font=("Arial", 11, "bold"),
                                     foreground="#000080")
        self.lbl_totales.pack()
        
        # Frame de botones
        frm_buttons = ttk.Frame(self)
        frm_buttons.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(frm_buttons, text="Actualizar", 
                  command=self.cargar_libro_diario).pack(side="left", padx=4)

    
    def aplicar_filtro(self):
        """Aplica el filtro de fechas"""
        fecha_desde = self.fecha_desde.get_date().strftime('%Y-%m-%d')
        fecha_hasta = self.fecha_hasta.get_date().strftime('%Y-%m-%d')
        self.cargar_libro_diario(fecha_desde, fecha_hasta)
    
    def limpiar_filtros(self):
        """Limpia los filtros y muestra todos los movimientos"""
        self.cargar_libro_diario()

    def cargar_libro_diario(self, fecha_desde=None, fecha_hasta=None):
        """Carga los movimientos del libro diario en orden cronológico"""
        # Limpiar el árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener movimientos
        movimientos = self.model.get_movimientos(fecha_desde, fecha_hasta)
        
        # Insertar movimientos con separadores entre comprobantes
        comprobante_anterior = None
        for fecha, numero, glosa, codigo, cuenta, debe, haber in movimientos:
            # Agregar línea separadora visual entre comprobantes diferentes
            if comprobante_anterior and comprobante_anterior != numero:
                self.tree.insert("", "end", values=('', '', '', '', '', '', ''), tags=('separador',))
            
            self.tree.insert("", "end", values=(
                fecha,
                numero,
                glosa,
                codigo,
                cuenta,
                f"${debe:,.0f}" if debe > 0 else "-",
                f"${haber:,.0f}" if haber > 0 else "-"
            ))
            
            comprobante_anterior = numero
        
        # Configurar tag para separadores
        self.tree.tag_configure('separador', background='#f0f0f0')
        
        # Obtener y mostrar totales
        totales = self.model.get_totales_generales(fecha_desde, fecha_hasta)
        total_debe, total_haber = totales
        
        # Contar movimientos
        num_movimientos = len(movimientos)
        
        # Verificar balance
        diferencia = abs(total_debe - total_haber)
        cuadrado = diferencia < 0.01
        
        texto_totales = f"Movimientos: {num_movimientos}  |  TOTALES: Debe: ${total_debe:,.0f}  |  Haber: ${total_haber:,.0f}"
        if cuadrado:
            texto_totales += "  ✓ CUADRADO"
            self.lbl_totales.config(text=texto_totales, foreground="green")
        else:
            texto_totales += f"  ✗ DESCUADRADO (Diferencia: ${diferencia:,.0f})"
            self.lbl_totales.config(text=texto_totales, foreground="red")
