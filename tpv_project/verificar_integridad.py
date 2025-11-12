"""
Script de verificación de integridad del proyecto.

Verifica que todos los archivos necesarios existen y que no hay errores
de sintaxis obvios.
"""

import sys
from pathlib import Path
import os

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_header(msg):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")

def verificar_estructura():
    """Verifica la estructura de directorios."""
    print_header("Verificando estructura de directorios")
    
    directorios_requeridos = [
        'config',
        'core',
        'models',
        'controllers',
        'views',
        'views/components',
        'data',
        'utils'
    ]
    
    errores = []
    
    for directorio in directorios_requeridos:
        if os.path.isdir(directorio):
            print_success(f"Directorio '{directorio}' existe")
        else:
            print_error(f"Directorio '{directorio}' NO EXISTE")
            errores.append(f"Falta directorio: {directorio}")
    
    return errores

def verificar_archivos_python():
    """Verifica que existen los archivos Python necesarios."""
    print_header("Verificando archivos Python")
    
    archivos_requeridos = [
        # Raíz
        'main.py',
        'create_images.py',
        
        # Config
        'config/__init__.py',
        'config/settings.py',
        
        # Core
        'core/__init__.py',
        'core/encryption.py',
        'core/image_manager.py',
        
        # Models
        'models/__init__.py',
        'models/product.py',
        'models/receipt.py',
        'models/customer.py',
        
        # Controllers
        'controllers/__init__.py',
        'controllers/printer_controller.py',
        'controllers/calendar_controller.py',
        'controllers/receipt_controller.py',
        
        # Data
        'data/__init__.py',
        'data/data_manager.py',
        
        # Utils
        'utils/__init__.py',
        'utils/formatters.py',
        'utils/validators.py',
        
        # Views
        'views/__init__.py',
        'views/main_view.py',
        'views/calendar_view.py',
        'views/keyboard_view.py',
        
        # Components
        'views/components/__init__.py',
        'views/components/base_widgets.py',
        'views/components/keyboard.py',
        'views/components/ticket_display.py',
    ]
    
    errores = []
    
    for archivo in archivos_requeridos:
        if os.path.isfile(archivo):
            print_success(f"Archivo '{archivo}' existe")
        else:
            print_error(f"Archivo '{archivo}' NO EXISTE")
            errores.append(f"Falta archivo: {archivo}")
    
    return errores

def verificar_sintaxis():
    """Verifica la sintaxis de los archivos Python principales."""
    print_header("Verificando sintaxis Python")
    
    archivos_criticos = [
        'main.py',
        'views/main_view.py',
        'views/calendar_view.py',
        'views/keyboard_view.py',
        'controllers/receipt_controller.py',
        'data/data_manager.py'
    ]
    
    errores = []
    
    for archivo in archivos_criticos:
        if not os.path.isfile(archivo):
            continue
            
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                compile(f.read(), archivo, 'exec')
            print_success(f"Sintaxis correcta en '{archivo}'")
        except SyntaxError as e:
            print_error(f"Error de sintaxis en '{archivo}': línea {e.lineno}")
            errores.append(f"Error de sintaxis en {archivo}: {e.msg}")
        except Exception as e:
            print_warning(f"Advertencia en '{archivo}': {str(e)}")
    
    return errores

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas."""
    print_header("Verificando dependencias")
    
    dependencias = [
        'PIL',
        'cryptography',
        'win32print',
        'win32ui'
    ]
    
    errores = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            print_success(f"Dependencia '{dep}' instalada")
        except ImportError:
            if dep.startswith('win32'):
                print_warning(f"Dependencia '{dep}' no encontrada (solo Windows)")
            else:
                print_error(f"Dependencia '{dep}' NO INSTALADA")
                errores.append(f"Falta dependencia: {dep}")
    
    return errores

def verificar_archivos_datos():
    """Verifica los archivos de datos."""
    print_header("Verificando archivos de datos")
    
    errores = []
    
    # Verificar icono
    if os.path.isfile('icono.ico'):
        print_success("Archivo 'icono.ico' existe")
    else:
        print_warning("Archivo 'icono.ico' no encontrado (opcional)")
    
    # Verificar image.tpv
    if os.path.isfile('image.tpv'):
        print_success("Archivo 'image.tpv' existe")
    else:
        print_error("Archivo 'image.tpv' NO EXISTE")
        errores.append("Falta image.tpv - ejecute: python create_images.py")
    
    # Verificar directorio archivos
    if os.path.isdir('archivos'):
        archivos_png = [f for f in os.listdir('archivos') if f.endswith('.png')]
        if archivos_png:
            print_success(f"Directorio 'archivos/' contiene {len(archivos_png)} imágenes PNG")
        else:
            print_warning("Directorio 'archivos/' existe pero está vacío")
    else:
        print_warning("Directorio 'archivos/' no existe (necesario para crear image.tpv)")
    
    # Verificar data.tpv (se creará automáticamente)
    if os.path.isfile('data/data.tpv'):
        print_success("Archivo 'data/data.tpv' existe")
    else:
        print_warning("Archivo 'data/data.tpv' no existe (se creará automáticamente)")
    
    return errores

def main():
    """Función principal."""
    print("\n")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}  VERIFICACIÓN DE INTEGRIDAD - TPV BAR ROBLEDO{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    todos_errores = []
    
    # Ejecutar verificaciones
    todos_errores.extend(verificar_estructura())
    todos_errores.extend(verificar_archivos_python())
    todos_errores.extend(verificar_sintaxis())
    todos_errores.extend(verificar_dependencias())
    todos_errores.extend(verificar_archivos_datos())
    
    # Resumen final
    print_header("RESUMEN")
    
    if not todos_errores:
        print_success("¡Todo correcto! La aplicación está lista para ejecutarse.")
        print("\nPara iniciar la aplicación, ejecute:")
        print(f"  {Colors.GREEN}python main.py{Colors.END}\n")
        return 0
    else:
        print_error(f"Se encontraron {len(todos_errores)} error(es):")
        print()
        for i, error in enumerate(todos_errores, 1):
            print(f"  {i}. {error}")
        print()
        print("Por favor, corrija estos errores antes de ejecutar la aplicación.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())