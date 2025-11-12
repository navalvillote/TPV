"""
Configuración global de la aplicación TPV.

Este módulo contiene todas las configuraciones y constantes
utilizadas en la aplicación.
"""

import os
from pathlib import Path
from typing import Tuple

# ============================================================================
# RUTAS Y ARCHIVOS
# ============================================================================

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio de datos
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# Archivos de datos
DATA_FILE = DATA_DIR / 'data.tpv'
IMAGES_FILE = BASE_DIR / 'image.tpv'
ICON_FILE = BASE_DIR / 'icono.ico'

# Directorio de imágenes fuente (para crear image.tpv)
IMAGES_SOURCE_DIR = BASE_DIR / 'archivos'


# ============================================================================
# CONFIGURACIÓN DE LA VENTANA
# ============================================================================

class WindowConfig:
    """Configuración de la ventana principal."""
    
    TITLE = "TPV - Bar Robledo"
    MIN_WIDTH = 1024
    MIN_HEIGHT = 768
    BACKGROUND_COLOR = 'gray34'
    
    @classmethod
    def get_dimensions(cls) -> Tuple[int, int]:
        """Retorna las dimensiones mínimas de la ventana."""
        return cls.MIN_WIDTH, cls.MIN_HEIGHT


# ============================================================================
# CONFIGURACIÓN DE COLORES
# ============================================================================

class ColorScheme:
    """Esquema de colores de la aplicación."""
    
    # Colores principales
    PRIMARY_BG = 'gray82'
    SECONDARY_BG = 'gray94'
    DARK_BG = 'gray22'
    
    # Colores por familia de productos
    BEBIDAS = 'dark slate gray'
    COMIDAS = 'salmon4'
    OTROS = 'DarkOrange4'
    
    # Colores de estado
    PENDIENTE = 'MediumPurple1'
    PENDIENTE_DARK = 'red4'
    REORDER = 'red4'
    
    # Colores de texto
    TEXT_NORMAL = 'SlateGray4'
    TEXT_DARK = 'gray18'
    TEXT_LIGHT = 'gray92'
    TEXT_INFO = 'green2'
    
    # Colores de botones
    BTN_DELETE = 'red3'
    BTN_OK = 'forest green'
    BTN_NORMAL = 'gray18'


# ============================================================================
# CONFIGURACIÓN DE TICKETS
# ============================================================================

class TicketConfig:
    """Configuración de tickets y recibos."""
    
    HEADER = 'Bar Robledo - BR2010'
    DEFAULT_IVA = 21.0
    LINE_WIDTH = 30
    TICKET_SEPARATOR = '-' * LINE_WIDTH
    
    # Formato de fecha y hora
    DATETIME_FORMAT = '%d/%m/%Y - %H:%M:%S'
    DATE_FORMAT = '%d/%m/%Y'
    
    # Estados de pago
    ESTADO_EFECTIVO = 'efectivo'
    ESTADO_TARJETA = 'tarjeta'
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_NUEVO = 'Nuevo'


# ============================================================================
# CONFIGURACIÓN DE IMPRESIÓN
# ============================================================================

class PrinterConfig:
    """Configuración de impresoras."""
    
    # Comando ESC/POS para abrir caja registradora
    OPEN_DRAWER_CMD = b'\x1B\x70\x00\x19\xFA'
    
    # Configuración de fuente
    FONT_NAME = "Consolas"
    FONT_HEIGHT = 37
    LINE_SPACING = 40


# ============================================================================
# CONFIGURACIÓN DE ENCRIPTACIÓN
# ============================================================================

class EncryptionConfig:
    """Configuración de encriptación de datos."""
    
    # IMPORTANTE: En producción, esta clave debería estar en variables de entorno
    ENCRYPTION_KEY = b'5-uvWBhTHRAk7Eq8wlzdnXZlLCZFj8rE44rUN49wztg='


# ============================================================================
# CONFIGURACIÓN DE PRODUCTOS
# ============================================================================

class ProductConfig:
    """Configuración de productos."""
    
    # Familias de productos
    FAMILIA_BEBIDA = 'Bebida'
    FAMILIA_COMIDA = 'Comida'
    FAMILIA_OTROS = 'Otros'
    FAMILIA_VARIOS = 'Varios'
    
    # Lista de familias
    FAMILIAS = [FAMILIA_BEBIDA, FAMILIA_COMIDA, FAMILIA_OTROS]
    
    # Límites
    MAX_PRODUCTOS_POR_FAMILIA = 40


# ============================================================================
# CONFIGURACIÓN DE INTERFAZ
# ============================================================================

class UIConfig:
    """Configuración de elementos de interfaz."""
    
    # Fuentes
    FONT_FAMILY = "Consolas"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_MEDIUM = 14
    FONT_SIZE_LARGE = 20
    FONT_SIZE_XLARGE = 24
    FONT_SIZE_XXLARGE = 26
    
    # Dimensiones de elementos
    TECLA_WIDTH = 70
    TECLA_HEIGHT = 70
    TECLA_DOBLE_WIDTH = 140
    TECLA_TRIPLE_WIDTH = 210
    TECLA_SPACE_WIDTH = 416
    TECLA_MARCO_WIDTH = 152
    TECLA_MARCO_HEIGHT = 70
    
    # Espaciado
    SPACING_SMALL = 5
    SPACING_MEDIUM = 10
    SPACING_LARGE = 20


# ============================================================================
# CONFIGURACIÓN DE TECLADO VIRTUAL
# ============================================================================

class KeyboardConfig:
    """Configuración del teclado virtual."""
    
    # Distribución de teclas
    TECLAS = (
        ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '7', '8', '9'),
        ('A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Ñ', '4', '5', '6'),
        ('-', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Ü', 'Ç', '1', '2', '3'),
        ('Shift', 'Space', 'Delete', '0', '.')
    )
    
    # Límites de escritura
    MAX_LINES = 2
    MAX_CHARS_PER_LINE = 14
    MAX_PASSWORD_LENGTH = 22


# ============================================================================
# CONFIGURACIÓN DE CALENDARIO
# ============================================================================

class CalendarConfig:
    """Configuración del calendario."""
    
    DIAS_SEMANA = ("LUN", "MAR", "MIE", "JUE", "VIE", "SAB", "DOM")
    
    # Tipos de reporte
    TIPO_DIA = 'día'
    TIPO_MES = 'mes'
    TIPO_DIA_A_DIA = 'día a día'
    
    # Totales disponibles
    TOTALES = (
        ('Caja Total Diaria', 'día'),
        ('Caja Total Mensual', 'mes'),
        ('Caja Mensual por Día', 'día a día'),
        ('Caja Mensual en Efectivo', 'efectivo'),
        ('Caja Mensual con Tarjeta', 'tarjeta')
    )


# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

class SecurityConfig:
    """Configuración de seguridad."""
    
    ADMINISTRADOR_CODE = '857281478'
    DEFAULT_PASSWORD = ''


# ============================================================================
# CONFIGURACIÓN DE MODOS
# ============================================================================

class ModeConfig:
    """Configuración de modos de operación."""
    
    MODO_PRODUCTO = 'Producto'
    MODO_PENDIENTE = 'Pendiente'
    MODO_CAMARERO = 'Camarero'
    
    ESCRITURA_NOMBRES = 'nombres'
    ESCRITURA_PRODUCTOS = 'productos'
    ESCRITURA_MONEDAS = 'monedas'
    ESCRITURA_PASSWORD = 'password'


# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

class LogConfig:
    """Configuración de logging."""
    
    LOG_FILE = DATA_DIR / 'tpv.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'


# ============================================================================
# VALIDACIÓN DE CONFIGURACIÓN
# ============================================================================

def validate_config() -> bool:
    """
    Valida que la configuración sea correcta.
    
    Returns:
        bool: True si la configuración es válida, False en caso contrario.
    """
    errors = []
    
    # Verificar que el archivo de icono existe
    if not ICON_FILE.exists():
        errors.append(f"Archivo de icono no encontrado: {ICON_FILE}")
    
    # Verificar que el directorio de datos existe
    if not DATA_DIR.exists():
        errors.append(f"Directorio de datos no encontrado: {DATA_DIR}")
    
    # Verificar valores numéricos
    if WindowConfig.MIN_WIDTH <= 0 or WindowConfig.MIN_HEIGHT <= 0:
        errors.append("Las dimensiones de la ventana deben ser positivas")
    
    if TicketConfig.DEFAULT_IVA < 0 or TicketConfig.DEFAULT_IVA > 100:
        errors.append("El IVA debe estar entre 0 y 100")
    
    if errors:
        for error in errors:
            print(f"ERROR DE CONFIGURACIÓN: {error}")
        return False
    
    return True


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'WindowConfig',
    'ColorScheme',
    'TicketConfig',
    'PrinterConfig',
    'EncryptionConfig',
    'ProductConfig',
    'UIConfig',
    'KeyboardConfig',
    'CalendarConfig',
    'SecurityConfig',
    'ModeConfig',
    'LogConfig',
    'DATA_FILE',
    'IMAGES_FILE',
    'ICON_FILE',
    'IMAGES_SOURCE_DIR',
    'validate_config'
]