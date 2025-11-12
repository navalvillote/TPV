"""
Utilidades de formateo para la aplicación TPV.

Este módulo contiene funciones para formatear texto, números y fechas.
"""

from typing import List
from config.settings import TicketConfig


def formatear_numero_moneda(tecla: str, numero: str) -> str:
    """
    Formatea un número como moneda añadiendo o eliminando dígitos.
    
    Args:
        tecla: Tecla pulsada ('0'-'9' o 'Delete')
        numero: Número actual como string (puede estar vacío)
        
    Returns:
        str: Número formateado con 2 decimales o vacío
        
    Examples:
        >>> formatear_numero_moneda('5', '')
        '0.05'
        >>> formatear_numero_moneda('3', '0.05')
        '0.53'
        >>> formatear_numero_moneda('Delete', '0.53')
        '0.05'
    """
    if tecla == 'Delete':
        if numero != '':
            num = float(numero)
            num = num * 100
            num = int(num / 10)
            num = num / 100
            if num == 0:
                numero = ''
            else:
                numero = f'{num:.2f}'
    else:
        if len(numero) < 8:
            if numero != '':
                num = float(numero)
                num *= 10
                num = num + float(tecla) / 100
                numero = f'{num:.2f}'
            else:
                if tecla != '0':
                    num = int(tecla)
                    num /= 100
                    numero = f'{num:.2f}'
    
    return numero


def convertir_texto_multilnea(texto: str, limite: int = 14) -> str:
    """
    Convierte un texto en líneas con un máximo de caracteres.
    
    Args:
        texto: Texto a convertir
        limite: Número máximo de caracteres por línea
        
    Returns:
        str: Texto con saltos de línea insertados
        
    Examples:
        >>> convertir_texto_multilnea("Hola mundo", 5)
        'Hola\\nmundo'
    """
    lineas = []
    frase = ''
    lista = texto.split()
    
    for i in range(len(lista)):
        frase += lista[i]
        
        if i + 1 > len(lista):
            lineas.append(frase)
        elif i + 1 == len(lista):
            lineas.append(frase)
        else:
            if len(frase + ' ' + lista[i + 1]) > limite:
                lineas.append(frase)
                frase = ''
            else:
                frase += ' '
    
    return '\n'.join(lineas)


def formatear_linea_ticket(cantidad: int, nombre: str, precio: float) -> str:
    """
    Formatea una línea del ticket con la cantidad, nombre y precio.
    
    Args:
        cantidad: Cantidad de productos
        nombre: Nombre del producto
        precio: Precio unitario
        
    Returns:
        str: Línea formateada para el ticket
        
    Examples:
        >>> formatear_linea_ticket(2, "Café", 1.50)
        '2 x Café:..................3.00€'
    """
    suma = cantidad * float(precio)
    suma_str = f'{suma:.2f}'
    num_puntos = TicketConfig.LINE_WIDTH - (
        len(str(cantidad)) + len(nombre) + len(suma_str)
    )
    
    return f'{cantidad} x {nombre}:{"." * num_puntos}{suma_str}€'


def centrar_texto(texto: str, ancho: int = 30) -> str:
    """
    Centra un texto en un ancho determinado.
    
    Args:
        texto: Texto a centrar
        ancho: Ancho total
        
    Returns:
        str: Texto centrado con espacios
    """
    espacios_totales = ancho - len(texto)
    if espacios_totales <= 0:
        return texto
    
    espacios_izq = espacios_totales // 2
    espacios_der = espacios_totales - espacios_izq
    
    return ' ' * espacios_izq + texto + ' ' * espacios_der


def obtener_listado_lineas(texto: str) -> List[str]:
    """
    Convierte un texto en una lista de líneas centradas de 30 caracteres.
    
    Args:
        texto: Texto a procesar (con saltos de línea)
        
    Returns:
        List[str]: Lista de líneas centradas
    """
    lista = texto.split('\n')
    
    for i, linea in enumerate(lista):
        if len(linea) < 30:
            delante = ''
            detras = ''
            sw = -1
            for j in range(30 - len(linea)):
                sw *= -1
                if sw == 1:
                    delante += ' '
                else:
                    detras += ' '
            lista[i] = delante + linea + detras
    
    return lista


def formatear_precio(precio: float) -> str:
    """
    Formatea un precio con 2 decimales y símbolo de euro.
    
    Args:
        precio: Precio a formatear
        
    Returns:
        str: Precio formateado (ej: "12.50€")
    """
    return f'{precio:.2f}€'


def formatear_fecha_completa(fecha_str: str) -> str:
    """
    Formatea una fecha para mostrar de forma legible.
    
    Args:
        fecha_str: Fecha en formato DD/MM/YYYY - HH:MM:SS
        
    Returns:
        str: Fecha formateada
    """
    return fecha_str


def calcular_base_imponible(total: float, iva: float) -> float:
    """
    Calcula la base imponible dado un total con IVA incluido.
    
    Args:
        total: Precio total con IVA
        iva: Porcentaje de IVA
        
    Returns:
        float: Base imponible sin IVA
    """
    return total / (1 + iva / 100)


def calcular_iva(total: float, iva: float) -> float:
    """
    Calcula el importe del IVA dado un total con IVA incluido.
    
    Args:
        total: Precio total con IVA
        iva: Porcentaje de IVA
        
    Returns:
        float: Importe del IVA
    """
    base = calcular_base_imponible(total, iva)
    return total - base


def limpiar_texto_entrada(texto: str) -> str:
    """
    Limpia un texto de entrada eliminando espacios extras.
    
    Args:
        texto: Texto a limpiar
        
    Returns:
        str: Texto limpio
    """
    return ' '.join(texto.split())


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'formatear_numero_moneda',
    'convertir_texto_multilnea',
    'formatear_linea_ticket',
    'centrar_texto',
    'obtener_listado_lineas',
    'formatear_precio',
    'formatear_fecha_completa',
    'calcular_base_imponible',
    'calcular_iva',
    'limpiar_texto_entrada'
]