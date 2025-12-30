"""
Ventana principal de la aplicación con panel lateral
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from PIL import Image, ImageTk


class MainWindow(tk.Tk):
    """Ventana principal del sistema contable con navegación lateral"""
    
    def __init__(self):
        super().__init__()
        self.title("Sistema Contable")
        self.geometry("1400x700")
        self.resizable(True, True)
        self.current_view = None
        self.create_widgets()
        # Mostrar Plan de Cuentas al iniciar
        self.show_plan_cuentas()

    def create_widgets(self):
        """Crea el layout con panel lateral y área de contenido"""
        # Panel lateral izquierdo
        self.sidebar = ttk.Frame(self, width=250, relief="raised", borderwidth=1)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Título del menú
        header = ttk.Frame(self.sidebar)
        header.pack(fill="x", pady=15)
        ttk.Label(header, text="SISTEMA CONTABLE", 
                 font=("Arial", 13, "bold")).pack()
        
        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", pady=5)

        # Botones de navegación
        menu_frame = ttk.Frame(self.sidebar)
        menu_frame.pack(fill="both", expand=True, pady=5)

        self.create_menu_button(menu_frame, "Plan de Cuentas", self.show_plan_cuentas)
        self.create_menu_button(menu_frame, "Comprobantes Contables", self.show_comprobantes)
        self.create_menu_button(menu_frame, "Libro Diario", self.show_libro_diario)
        self.create_menu_button(menu_frame, "Balance de Comprobación", self.show_balance_comprobacion)
        self.create_menu_button(menu_frame, "Estado de Situación", self.show_esf)
        self.create_menu_button(menu_frame, "Estado de Resultados", self.show_er)
        self.create_menu_button(menu_frame, "Libro de Compras", self.show_libro_compras)
        self.create_menu_button(menu_frame, "Libro de Ventas", self.show_libro_ventas)

        ttk.Separator(menu_frame, orient="horizontal").pack(fill="x", pady=10)
        
        self.create_menu_button(menu_frame, "Exportar a Excel", self.export_to_excel)
        self.create_menu_button(menu_frame, "Salir", self.quit_app)

        # Sección del logo en la parte inferior del sidebar
        logo_frame = ttk.Frame(self.sidebar)
        logo_frame.pack(side="bottom", fill="both", padx=10, pady=10)
        
        # Intentar cargar el logo
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "logo.png")
        if os.path.exists(logo_path):
            try:
                # Cargar y redimensionar imagen
                logo_img = Image.open(logo_path)
                # Redimensionar manteniendo aspecto (máximo 180x180 para que quepa en el frame)
                logo_img.thumbnail((180, 180), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                
                # Mostrar logo centrado
                logo_label = ttk.Label(logo_frame, image=self.logo_photo)
                logo_label.pack(anchor="center")
            except Exception as e:
                # Si falla la carga, no mostrar nada
                print(f"Error al cargar logo: {e}")
        else:
            # Si no existe logo, no mostrar nada
            pass
        
        # Firma del desarrollador
        firma_label = ttk.Label(logo_frame, 
                               text="Diseñado y Creado por\nFranco Cortés, Crexer",
                               font=("Arial", 8, "italic"),
                               foreground="#666666",
                               justify="center")
        firma_label.pack(anchor="center", pady=(10, 0))

        # Área de contenido derecha
        self.content_area = ttk.Frame(self, relief="flat")
        self.content_area.pack(side="right", fill="both", expand=True)

    def create_menu_button(self, parent, text, command):
        """Crea un botón de menú con estilo consistente"""
        btn = ttk.Button(parent, text=text, command=command)
        btn.pack(fill="x", padx=8, pady=3)
        return btn

    def clear_content_area(self):
        """Limpia el área de contenido"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None

    def show_plan_cuentas(self):
        """Muestra la vista de Plan de Cuentas"""
        from views.plan_cuentas_view import PlanCuentasView
        self.clear_content_area()
        self.current_view = PlanCuentasView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_comprobantes(self):
        """Muestra la vista de Comprobantes"""
        from views.comprobantes_view import ComprobantesView
        self.clear_content_area()
        self.current_view = ComprobantesView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_libro_diario(self):
        """Muestra la vista del Libro Diario"""
        from views.libro_diario_view import LibroDiarioView
        self.clear_content_area()
        self.current_view = LibroDiarioView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_balance_comprobacion(self):
        """Muestra la vista del Balance de Comprobación"""
        from views.balance_comprobacion_view import BalanceComprobacionView
        self.clear_content_area()
        self.current_view = BalanceComprobacionView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_esf(self):
        """Muestra el Estado de Situación Financiera"""
        from views.estado_situacion_view import EstadoSituacionView
        self.clear_content_area()
        self.current_view = EstadoSituacionView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_er(self):
        """Muestra el Estado de Resultados"""
        from views.estado_resultados_view import EstadoResultadosView
        self.clear_content_area()
        self.current_view = EstadoResultadosView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_libro_compras(self):
        """Muestra el Libro de Compras"""
        from views.libro_compras_view import LibroComprasView
        self.clear_content_area()
        self.current_view = LibroComprasView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_libro_ventas(self):
        """Muestra el Libro de Ventas"""
        from views.libro_ventas_view import LibroVentasView
        self.clear_content_area()
        self.current_view = LibroVentasView(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def quit_app(self):
        """Cierra la aplicación"""
        if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
            self.quit()
    
    def export_to_excel(self):
        """Exporta todos los datos a un archivo Excel"""
        # Crear cuadro de diálogo para guardar archivo
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            initialfile=f"Evaluacion_Contable.xlsx"
        )
        
        if not filename:
            return
        
        # Ejecutar en hilo separado para no bloquear la interfaz
        def do_export():
            try:
                from utils.excel_exporter import export_all_data
                result_file = export_all_data(filename)
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{result_file}")
            except Exception as e:
                messagebox.showerror("Error en Exportación", f"Error al exportar datos:\n{str(e)}")
        
        export_thread = threading.Thread(target=do_export, daemon=True)
        export_thread.start()