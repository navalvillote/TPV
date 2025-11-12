"""
Script para crear el archivo de imágenes encriptadas (image.tpv).

Este script debe ejecutarse cuando se añaden o modifican imágenes
en el directorio 'archivos/'.

Uso:
    python create_images.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from core.image_manager import ImageManager
from config.settings import IMAGES_SOURCE_DIR, IMAGES_FILE


def main():
    """Función principal."""
    
    print("=" * 60)
    print("Script de Creación de Archivo de Imágenes")
    print("=" * 60)
    print()
    
    # Verificar directorio de origen
    if not IMAGES_SOURCE_DIR.exists():
        print(f"ERROR: No se encontró el directorio de imágenes")
        print(f"Ruta esperada: {IMAGES_SOURCE_DIR}")
        print()
        print("Por favor, cree el directorio 'archivos/' y coloque")
        print("las imágenes PNG necesarias en él.")
        return 1
    
    print(f"Directorio de origen: {IMAGES_SOURCE_DIR}")
    print(f"Archivo de destino: {IMAGES_FILE}")
    print()
    
    # Contar archivos PNG
    archivos_png = list(IMAGES_SOURCE_DIR.glob("*.png"))
    
    if not archivos_png:
        print("ERROR: No se encontraron archivos PNG en el directorio")
        print(f"Ruta: {IMAGES_SOURCE_DIR}")
        return 1
    
    print(f"Archivos PNG encontrados: {len(archivos_png)}")
    print()
    
    # Listar archivos
    print("Imágenes a procesar:")
    for i, archivo in enumerate(archivos_png, 1):
        print(f"  {i}. {archivo.name}")
    print()
    
    # Confirmar
    respuesta = input("¿Desea continuar? (s/n): ").strip().lower()
    
    if respuesta != 's' and respuesta != 'si' and respuesta != 'sí':
        print("Operación cancelada")
        return 0
    
    print()
    print("Procesando imágenes...")
    print("-" * 60)
    
    try:
        # Crear archivo de imágenes
        ImageManager.crear_archivo_imagenes()
        
        print("-" * 60)
        print()
        print("✓ Archivo de imágenes creado exitosamente")
        print(f"✓ Ubicación: {IMAGES_FILE}")
        print()
        print("Ahora puede ejecutar la aplicación principal con:")
        print("  python main.py")
        
        return 0
        
    except Exception as e:
        print("-" * 60)
        print()
        print(f"✗ ERROR al crear archivo de imágenes:")
        print(f"  {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return 1


def actualizar_imagen(nombre: str, ruta: str):
    """
    Actualiza una imagen específica en el archivo.
    
    Args:
        nombre: Nombre de la imagen (sin extensión)
        ruta: Ruta al nuevo archivo PNG
    """
    print(f"Actualizando imagen '{nombre}'...")
    
    try:
        ImageManager.actualizar_imagen_en_archivo(nombre, ruta)
        print(f"✓ Imagen '{nombre}' actualizada correctamente")
        
    except Exception as e:
        print(f"✗ ERROR al actualizar imagen:")
        print(f"  {str(e)}")


if __name__ == "__main__":
    # Si se pasan argumentos, actualizar imagen específica
    if len(sys.argv) == 3:
        nombre_imagen = sys.argv[1]
        ruta_imagen = sys.argv[2]
        actualizar_imagen(nombre_imagen, ruta_imagen)
    else:
        # Crear archivo completo
        sys.exit(main())