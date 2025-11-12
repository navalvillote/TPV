"""
Gestor de imágenes para la aplicación TPV.

Este módulo maneja la carga, almacenamiento y recuperación de imágenes
encriptadas desde el archivo image.tpv.
"""

import os
import io
from typing import Dict, List, Optional, Tuple
from PIL import Image
from pathlib import Path
from core.encryption import get_encryption_manager
from config.settings import IMAGES_FILE, IMAGES_SOURCE_DIR


class ImageManager:
    """Gestiona las imágenes de la aplicación."""
    
    def __init__(self):
        """Inicializa el gestor de imágenes."""
        self._imagenes: Dict[str, Image.Image] = {}
        self._encryption = get_encryption_manager()
    
    def cargar_imagenes_desde_archivo(self, ruta_archivo: str = None) -> None:
        """
        Carga las imágenes desde el archivo image.tpv.
        
        Args:
            ruta_archivo: Ruta al archivo de imágenes. Si es None, usa
                         la ruta por defecto de configuración.
                         
        Raises:
            FileNotFoundError: Si el archivo no existe
            Exception: Si hay error al cargar las imágenes
        """
        ruta = ruta_archivo or str(IMAGES_FILE)
        
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Archivo de imágenes no encontrado: {ruta}")
        
        try:
            # Cargar y desencriptar el archivo
            datos_lista = self._encryption.cargar_archivo_encriptado(
                ruta, 
                usar_json=False
            )
            
            # Procesar cada imagen
            self._imagenes.clear()
            for nombre, imagen_binaria in datos_lista:
                imagen = Image.open(io.BytesIO(imagen_binaria))
                imagen.filename = nombre
                self._imagenes[nombre] = imagen
                
        except Exception as e:
            raise Exception(f"Error al cargar imágenes: {str(e)}")
    
    def obtener_imagen(self, nombre: str) -> Optional[Image.Image]:
        """
        Obtiene una imagen por su nombre.
        
        Args:
            nombre: Nombre de la imagen (sin extensión)
            
        Returns:
            Optional[Image.Image]: Imagen si existe, None en caso contrario
        """
        return self._imagenes.get(nombre)
    
    def existe_imagen(self, nombre: str) -> bool:
        """
        Verifica si existe una imagen con el nombre dado.
        
        Args:
            nombre: Nombre de la imagen
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return nombre in self._imagenes
    
    def listar_imagenes(self) -> List[str]:
        """
        Lista todos los nombres de imágenes disponibles.
        
        Returns:
            List[str]: Lista de nombres de imágenes
        """
        return list(self._imagenes.keys())
    
    def obtener_numero_imagenes(self) -> int:
        """
        Obtiene el número total de imágenes cargadas.
        
        Returns:
            int: Número de imágenes
        """
        return len(self._imagenes)
    
    @staticmethod
    def crear_archivo_imagenes(directorio_origen: str = None,
                               ruta_destino: str = None) -> None:
        """
        Crea el archivo image.tpv a partir de imágenes PNG.
        
        Lee todas las imágenes PNG del directorio origen, las convierte
        a binario y las guarda encriptadas en image.tpv.
        
        Args:
            directorio_origen: Directorio con las imágenes PNG. Si es None,
                             usa el directorio por defecto.
            ruta_destino: Ruta del archivo destino. Si es None, usa la
                        ruta por defecto.
                        
        Raises:
            FileNotFoundError: Si el directorio origen no existe
            Exception: Si hay error al crear el archivo
        """
        dir_origen = directorio_origen or str(IMAGES_SOURCE_DIR)
        ruta_dest = ruta_destino or str(IMAGES_FILE)
        
        if not os.path.exists(dir_origen):
            raise FileNotFoundError(
                f"Directorio de imágenes no encontrado: {dir_origen}"
            )
        
        try:
            # Obtener lista de archivos PNG
            archivos_png = [
                f for f in os.listdir(dir_origen) 
                if f.lower().endswith('.png')
            ]
            
            if not archivos_png:
                raise Exception(
                    f"No se encontraron archivos PNG en {dir_origen}"
                )
            
            lista_imagenes = []
            
            # Procesar cada imagen
            for archivo in archivos_png:
                nombre = os.path.splitext(archivo)[0]
                ruta_completa = os.path.join(dir_origen, archivo)
                
                # Leer la imagen en binario
                with open(ruta_completa, "rb") as image_file:
                    imagen_binaria = image_file.read()
                
                lista_imagenes.append([nombre, imagen_binaria])
            
            # Guardar encriptado
            encryption = get_encryption_manager()
            encryption.guardar_archivo_encriptado(
                ruta_dest,
                lista_imagenes,
                usar_json=False
            )
            
            print(f"Archivo de imágenes creado exitosamente: {ruta_dest}")
            print(f"Total de imágenes procesadas: {len(lista_imagenes)}")
            
        except Exception as e:
            raise Exception(f"Error al crear archivo de imágenes: {str(e)}")
    
    @staticmethod
    def actualizar_imagen_en_archivo(nombre_imagen: str,
                                     ruta_imagen: str,
                                     ruta_archivo: str = None) -> None:
        """
        Actualiza o añade una imagen específica en el archivo image.tpv.
        
        Args:
            nombre_imagen: Nombre de la imagen (sin extensión)
            ruta_imagen: Ruta a la nueva imagen PNG
            ruta_archivo: Ruta al archivo image.tpv. Si es None, usa la
                        ruta por defecto.
                        
        Raises:
            FileNotFoundError: Si la imagen o el archivo no existen
            Exception: Si hay error al actualizar
        """
        ruta = ruta_archivo or str(IMAGES_FILE)
        
        if not os.path.exists(ruta_imagen):
            raise FileNotFoundError(f"Imagen no encontrada: {ruta_imagen}")
        
        try:
            encryption = get_encryption_manager()
            
            # Cargar archivo existente o crear lista vacía
            if os.path.exists(ruta):
                lista_imagenes = encryption.cargar_archivo_encriptado(
                    ruta,
                    usar_json=False
                )
            else:
                lista_imagenes = []
            
            # Leer nueva imagen
            with open(ruta_imagen, "rb") as image_file:
                imagen_binaria = image_file.read()
            
            # Buscar y actualizar o añadir
            encontrada = False
            for i, (nombre, _) in enumerate(lista_imagenes):
                if nombre == nombre_imagen:
                    lista_imagenes[i] = [nombre_imagen, imagen_binaria]
                    encontrada = True
                    break
            
            if not encontrada:
                lista_imagenes.append([nombre_imagen, imagen_binaria])
            
            # Guardar archivo actualizado
            encryption.guardar_archivo_encriptado(
                ruta,
                lista_imagenes,
                usar_json=False
            )
            
            accion = "actualizada" if encontrada else "añadida"
            print(f"Imagen '{nombre_imagen}' {accion} exitosamente")
            
        except Exception as e:
            raise Exception(f"Error al actualizar imagen: {str(e)}")


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

_image_manager = None


def get_image_manager() -> ImageManager:
    """
    Obtiene la instancia global del gestor de imágenes.
    
    Returns:
        ImageManager: Gestor de imágenes
    """
    global _image_manager
    if _image_manager is None:
        _image_manager = ImageManager()
    return _image_manager


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'ImageManager',
    'get_image_manager'
]