"""
Punto de entrada principal de la aplicación TPV.

Este script inicializa todos los componentes y lanza la aplicación.
"""

import sys
import locale
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from config.settings import validate_config
from core.image_manager import get_image_manager
from data.data_manager_sqlite import get_data_manager_sqlite as get_data_manager
from models.receipt import ReceiptManager
from controllers.receipt_controller import ReceiptController
from controllers.printer_controller import get_printer_controller
from controllers.calendar_controller import CalendarController
from views.main_view import MainWindow


def inicializar_locale() -> None:
    """Inicializa la configuración regional."""
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain')
        except:
            print("Advertencia: No se pudo establecer el locale español")


def cargar_imagenes() -> bool:
    """
    Carga las imágenes de la aplicación.
    
    Returns:
        bool: True si se cargaron correctamente, False en caso contrario
    """
    try:
        image_manager = get_image_manager()
        image_manager.cargar_imagenes_desde_archivo()
        print(f"✓ Imágenes cargadas: {image_manager.obtener_numero_imagenes()}")
        return True
    except Exception as e:
        print(f"✗ Error al cargar imágenes: {e}")
        print("  Por favor, ejecute 'python create_images.py' primero")
        return False


def inicializar_datos() -> bool:
    """
    Inicializa y carga los datos de la aplicación.
    
    Returns:
        bool: True si se inicializaron correctamente
    """
    try:
        data_manager = get_data_manager()
        
        # Cargar datos generales
        if data_manager.cargar_datos_generales():
            print("✓ Datos cargados correctamente")
        else:
            print("⚠ Creando base de datos nueva...")
            # Crear datos de ejemplo si no existen
            data_manager.crear_datos_ejemplo()
            data_manager.guardar_datos_generales()
            print("✓ Base de datos creada con productos de ejemplo")
        
        print(f"  - Productos: {data_manager.products.obtener_numero_productos()}")
        print(f"  - Clientes: {data_manager.customers.obtener_numero_clientes()}")
        print(f"  - Camareros: {data_manager.waiters.obtener_numero_camareros()}")
        print(f"  - Tickets pendientes: {len(data_manager.receipts_pending)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error al inicializar datos: {e}")
        import traceback
        traceback.print_exc()
        return False


def crear_controladores(data_manager) -> tuple:
    """
    Crea los controladores de la aplicación.
    
    Args:
        data_manager: Gestor de datos
        
    Returns:
        tuple: (receipt_controller, printer_controller, calendar_controller)
    """
    # Cargar recibos anuales
    receipt_manager = data_manager.cargar_recibos_anuales()
    
    # Crear controladores
    receipt_controller = ReceiptController(data_manager, receipt_manager)
    printer_controller = get_printer_controller()
    calendar_controller = CalendarController(receipt_manager)
    
    # Establecer data_manager en calendar_controller para acceso a recibos
    calendar_controller.data_manager = data_manager
    
    print("✓ Controladores creados")
    print(f"  - Impresoras disponibles: {len(printer_controller.obtener_impresoras_disponibles())}")
    
    return receipt_controller, printer_controller, calendar_controller


def main():
    """Función principal de la aplicación."""
    
    print()
    print("=" * 60)
    print("  INICIANDO TPV - BAR ROBLEDO")
    print("=" * 60)
    print()
    
    # Validar configuración
    print("Validando configuración...")
    if not validate_config():
        print("✗ ERROR: Configuración inválida")
        return 1
    print("✓ Configuración válida")
    print()
    
    # Inicializar locale
    print("Configurando idioma...")
    inicializar_locale()
    print("✓ Configuración regional establecida")
    print()
    
    # Cargar imágenes
    print("Cargando imágenes...")
    if not cargar_imagenes():
        print()
        print("=" * 60)
        print("  SOLUCIÓN: Ejecute 'python create_images.py'")
        print("=" * 60)
        return 1
    print()
    
    # Inicializar datos
    print("Inicializando datos...")
    if not inicializar_datos():
        return 1
    print()
    
    # Obtener gestor de datos
    data_manager = get_data_manager()
    
    # Crear controladores
    print("Creando controladores...")
    receipt_controller, printer_controller, calendar_controller = crear_controladores(data_manager)
    print()
    
    print("Creando interfaz gráfica...")
    
    try:
        # Crear ventana principal
        ventana = MainWindow()
        
        # Establecer controladores
        ventana.establecer_controladores(
            receipt_controller,
            printer_controller,
            calendar_controller,
            data_manager
        )
        
        # Crear interfaz
        ventana.crear_interfaz()
        
        # Inicializar datos en la interfaz
        ventana.inicializar_datos()
        
        print("✓ Interfaz creada correctamente")
        print()
        print("=" * 60)
        print("  APLICACIÓN INICIADA - ¡BIENVENIDO!")
        print("=" * 60)
        print()
        print("  Presione ESC para salir")
        print()
        
        # Iniciar aplicación
        ventana.mainloop()
        
        # Al cerrar, guardar datos (ya se hace en el método _salir de MainWindow)
        print()
        print("=" * 60)
        print("  CERRANDO APLICACIÓN")
        print("=" * 60)
        print()
        print("¡Hasta pronto!")
        print()
        return 0
        
    except Exception as e:
        print(f"✗ Error al crear la interfaz: {e}")
        print()
        import traceback
        traceback.print_exc()
        print()
        print("=" * 60)
        print("  ERROR CRÍTICO - La aplicación no puede continuar")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())