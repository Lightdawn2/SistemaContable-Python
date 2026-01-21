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
        # Estado de desbloqueo de libros (persistente durante la sesión)
        self.libros_desbloqueados = False
        # Contraseña para desbloquear libros
        self.PASSWORD_LIBROS = "Contabilidad2026$"
        self.create_widgets()
        # Mostrar Plan de Cuentas al iniciar
        self.show_esf()

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
        
        self.create_menu_button(menu_frame, "Limpiar Base de Datos", self.clear_database)
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
        """Muestra el Libro de Compras (requiere contraseña la primera vez)"""
        # Verificar si los libros están desbloqueados
        if not self.libros_desbloqueados:
            if not self.solicitar_password():
                return  # Si la contraseña es incorrecta, no abrir la vista
        
        from views.libro_compras_view import LibroComprasView
        self.clear_content_area()
        self.current_view = LibroComprasView(self.content_area)
        self.current_view.pack(fill="both", expand=True)

    def show_libro_ventas(self):
        """Muestra el Libro de Ventas (requiere contraseña la primera vez)"""
        # Verificar si los libros están desbloqueados
        if not self.libros_desbloqueados:
            if not self.solicitar_password():
                return  # Si la contraseña es incorrecta, no abrir la vista
        
        from views.libro_ventas_view import LibroVentasView
        self.clear_content_area()
        self.current_view = LibroVentasView(self.content_area)
        self.current_view.pack(fill="both", expand=True)
    
    def solicitar_password(self):
        """Solicita contraseña para desbloquear los libros. Retorna True si es correcta."""
        # Crear ventana modal
        dialog = tk.Toplevel(self)
        dialog.title("Acceso Restringido")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Variable para almacenar el resultado
        password_correcta = [False]
        
        # Frame principal
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Mensaje informativo
        ttk.Label(
            main_frame,
            text="Acceso a Libros de Compras y Ventas",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 10))
        
        ttk.Label(
            main_frame,
            text="Esta sección requiere contraseña.\nUna vez desbloqueada, permanecerá así durante la sesión.",
            justify="center"
        ).pack(pady=(0, 20))
        
        # Frame para entrada de contraseña
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Contraseña:").pack(side="left", padx=(0, 10))
        password_entry = ttk.Entry(input_frame, show="●", width=25)
        password_entry.pack(side="left")
        password_entry.focus()
        
        # Mensaje de error (inicialmente oculto)
        error_label = ttk.Label(main_frame, text="", foreground="red")
        error_label.pack(pady=(10, 0))
        
        def verificar_password():
            """Verifica si la contraseña ingresada es correcta"""
            password_ingresada = password_entry.get()
            
            if password_ingresada == self.PASSWORD_LIBROS:
                # Contraseña correcta: desbloquear libros y cerrar diálogo
                self.libros_desbloqueados = True
                password_correcta[0] = True
                messagebox.showinfo(
                    "Acceso Concedido",
                    "Los Libros de Compras y Ventas han sido desbloqueados.\n"
                    "Permanecerán accesibles durante esta sesión.",
                    parent=dialog
                )
                dialog.destroy()
            else:
                # Contraseña incorrecta: mostrar error
                error_label.config(text="❌ Contraseña incorrecta")
                password_entry.delete(0, tk.END)
                password_entry.focus()
        
        def cancelar():
            """Cierra el diálogo sin desbloquear"""
            dialog.destroy()
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Aceptar",
            command=verificar_password
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Cancelar",
            command=cancelar
        ).pack(side="left", padx=5)
        
        # Bind Enter key
        password_entry.bind("<Return>", lambda e: verificar_password())
        dialog.bind("<Escape>", lambda e: cancelar())
        
        # Esperar a que se cierre el diálogo
        dialog.wait_window()
        
        return password_correcta[0]
    
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

    def clear_database(self):
        """Limpia la base de datos excepto el Plan de Cuentas"""
        confirm = messagebox.askyesno(
            "Limpiar Base de Datos",
            "Se eliminarán TODOS los datos operativos (comprobantes, detalles, libros)\n"
            "pero se mantendrá el Plan de Cuentas.\n\n"
            "¿Desea continuar?"
        )

        if not confirm:
            return

        def do_clear():
            try:
                from database.queries import clear_all_data_except_plan_cuentas

                counts = clear_all_data_except_plan_cuentas()
                msg = (
                    "Datos operativos eliminados correctamente.\n\n"
                    "Detalle de borrado:\n"
                    f"- Detalle de comprobantes: {counts.get('detalle_comprobantes', 0)} registros\n"
                    f"- Comprobantes: {counts.get('comprobantes', 0)} registros\n"
                    f"- Libro de Compras: {counts.get('libro_compras', 0)} registros\n"
                    f"- Libro de Ventas: {counts.get('libro_ventas', 0)} registros\n"
                )
                messagebox.showinfo("Base de datos limpiada", msg)

                # Volver a mostrar el estado financiero para refrescar vistas
                self.show_esf()
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo limpiar la base de datos:\n{str(e)}"
                )

        threading.Thread(target=do_clear, daemon=True).start()