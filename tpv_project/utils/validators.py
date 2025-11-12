"""
Validadores para la aplicación TPV.

Este módulo contiene funciones de validación para diferentes tipos de datos.
"""

from typing import Optional
import re


def validar_precio(precio: str) -> bool:
    """
    Valida que un precio sea correcto.
    
    Args:
        precio: Precio como string
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    try:
        valor = float(precio)
        return valor >= 0
    except (ValueError, TypeError):
        return False


def validar_nombre_producto(nombre: str) -> bool:
    """
    Valida que un nombre de producto sea válido.
    
    Args:
        nombre: Nombre del producto
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not nombre or len(nombre.strip()) == 0:
        return False
    
    if len(nombre) > 50:
        return False
    
    return True


def validar_nombre_cliente(nombre: str) -> bool:
    """
    Valida que un nombre de cliente sea válido.
    
    Args:
        nombre: Nombre del cliente
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not nombre or len(nombre.strip()) == 0:
        return False
    
    if len(nombre) > 100:
        return False
    
    return True


def validar_cantidad(cantidad: int) -> bool:
    """
    Valida que una cantidad sea válida.
    
    Args:
        cantidad: Cantidad de productos
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    try:
        return int(cantidad) > 0
    except (ValueError, TypeError):
        return False


def validar_iva(iva: float) -> bool:
    """
    Valida que un porcentaje de IVA sea válido.
    
    Args:
        iva: Porcentaje de IVA
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    try:
        valor = float(iva)
        return 0 <= valor <= 100
    except (ValueError, TypeError):
        return False


def validar_password(password: str) -> bool:
    """
    Valida que una contraseña sea válida.
    
    Args:
        password: Contraseña a validar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not password:
        return False
    
    # Permitir contraseñas numéricas y alfanuméricas
    if len(password) < 4:
        return False
    
    if len(password) > 22:
        return False
    
    return True


def validar_familia(familia: str, familias_validas: list) -> bool:
    """
    Valida que una familia de productos sea válida.
    
    Args:
        familia: Familia a validar
        familias_validas: Lista de familias válidas
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    return familia in familias_validas


def validar_estado_pago(estado: str, estados_validos: list) -> bool:
    """
    Valida que un estado de pago sea válido.
    
    Args:
        estado: Estado a validar
        estados_validos: Lista de estados válidos
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    return estado in estados_validos


def sanitizar_texto(texto: str) -> str:
    """
    Sanitiza un texto eliminando caracteres peligrosos.
    
    Args:
        texto: Texto a sanitizar
        
    Returns:
        str: Texto sanitizado
    """
    # Eliminar caracteres de control excepto saltos de línea y tabulaciones
    texto_limpio = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', texto)
    return texto_limpio.strip()


def validar_tecla_alfanumerica(tecla: str) -> bool:
    """
    Valida que una tecla sea alfanumérica o especial permitida.
    
    Args:
        tecla: Tecla a validar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    teclas_especiales = ['Space', 'Delete', 'Shift', '-', '.', 'Ñ', 'Ü', 'Ç']
    
    if tecla in teclas_especiales:
        return True
    
    return len(tecla) == 1 and (tecla.isalnum() or tecla == ' ')


def validar_tecla_numerica(tecla: str) -> bool:
    """
    Valida que una tecla sea numérica.
    
    Args:
        tecla: Tecla a validar
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    teclas_especiales = ['Delete', '.', 'del', 'ok']
    
    if tecla in teclas_especiales:
        return True
    
    return tecla.isdigit()


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'validar_precio',
    'validar_nombre_producto',
    'validar_nombre_cliente',
    'validar_cantidad',
    'validar_iva',
    'validar_password',
    'validar_familia',
    'validar_estado_pago',
    'sanitizar_texto',
    'validar_tecla_alfanumerica',
    'validar_tecla_numerica'
]