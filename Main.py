"""
Sistema de Contabilidad
Punto de entrada principal de la aplicación

Autor: Sistema Contable v2.0
Fecha: Diciembre 2025
"""
from database import init_db
from views.main_window import MainWindow


def main():
    """Función principal que inicia la aplicación"""
    # Inicializar la base de datos
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos inicializada correctamente.")
    
    # Crear y ejecutar la aplicación
    print("Iniciando aplicación..")
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
