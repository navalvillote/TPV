"""
Controlador de impresión.

Este módulo maneja la impresión de tickets y la apertura de caja registradora.
"""

from typing import List, Optional
import win32print
import win32ui
from config.settings import PrinterConfig
from utils.formatters import obtener_listado_lineas


class PrinterController:
    """Controlador para gestión de impresoras."""
    
    def __init__(self):
        """Inicializa el controlador de impresión."""
        self._impresoras_disponibles: List[str] = []
        self._actualizar_lista_impresoras()
    
    def _actualizar_lista_impresoras(self) -> None:
        """Actualiza la lista de impresoras disponibles."""
        try:
            printers = win32print.EnumPrinters(
                win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
            )
            self._impresoras_disponibles = [impresora[2] for impresora in printers]
        except Exception as e:
            print(f"Error al obtener impresoras: {e}")
            self._impresoras_disponibles = []
    
    def obtener_impresoras_disponibles(self) -> List[str]:
        """
        Obtiene la lista de impresoras disponibles en el sistema.
        
        Returns:
            List[str]: Lista de nombres de impresoras
        """
        self._actualizar_lista_impresoras()
        return self._impresoras_disponibles.copy()
    
    def obtener_impresora_predeterminada(self) -> Optional[str]:
        """
        Obtiene el nombre de la impresora predeterminada del sistema.
        
        Returns:
            Optional[str]: Nombre de la impresora o None si hay error
        """
        try:
            return win32print.GetDefaultPrinter()
        except Exception as e:
            print(f"Error al obtener impresora predeterminada: {e}")
            return None
    
    def abrir_caja_registradora(self, nombre_impresora: str) -> bool:
        """
        Envía el comando para abrir la caja registradora.
        
        Args:
            nombre_impresora: Nombre de la impresora conectada a la caja
            
        Returns:
            bool: True si se envió el comando correctamente, False en caso contrario
        """
        if not nombre_impresora:
            print("No se ha especificado impresora para abrir caja")
            return False
        
        try:
            hprinter = win32print.OpenPrinter(nombre_impresora)
            try:
                # Crear un trabajo de impresión
                hprinter_job = win32print.StartDocPrinter(
                    hprinter, 
                    1, 
                    ("Abrir caja registradora", None, "RAW")
                )
                win32print.StartPagePrinter(hprinter)
                win32print.WritePrinter(hprinter, PrinterConfig.OPEN_DRAWER_CMD)
                win32print.EndPagePrinter(hprinter)
                win32print.EndDocPrinter(hprinter)
                return True
            finally:
                win32print.ClosePrinter(hprinter)
                
        except Exception as e:
            print(f"Error al abrir caja registradora: {e}")
            return False
    
    def imprimir_ticket(self, texto_ticket: str, nombre_impresora: str) -> bool:
        """
        Imprime un ticket en la impresora especificada.
        
        Args:
            texto_ticket: Texto del ticket a imprimir
            nombre_impresora: Nombre de la impresora
            
        Returns:
            bool: True si se imprimió correctamente, False en caso contrario
        """
        if not nombre_impresora:
            print("No se ha especificado impresora")
            return False
        
        try:
            # Obtener líneas formateadas
            lineas = obtener_listado_lineas(texto_ticket)
            
            # Imprimir
            return self._imprimir_lineas(lineas, nombre_impresora)
            
        except Exception as e:
            print(f"Error al imprimir ticket: {e}")
            return False
    
    def _imprimir_lineas(self, lineas: List[str], nombre_impresora: str) -> bool:
        """
        Imprime líneas de texto en la impresora.
        
        Args:
            lineas: Lista de líneas a imprimir
            nombre_impresora: Nombre de la impresora
            
        Returns:
            bool: True si se imprimió correctamente, False en caso contrario
        """
        try:
            hprinter = win32print.OpenPrinter(nombre_impresora)
            try:
                printer_info = win32print.GetPrinter(hprinter, 2)
                pdc = win32ui.CreateDC()
                pdc.CreatePrinterDC(printer_info['pPrinterName'])
                pdc.StartDoc("Impresión de ticket TPV")
                pdc.StartPage()
                
                # Configurar fuente
                fuente = win32ui.CreateFont({
                    "name": PrinterConfig.FONT_NAME,
                    "height": PrinterConfig.FONT_HEIGHT,
                })
                pdc.SelectObject(fuente)
                
                # Imprimir cada línea
                x, y = 0, 0
                for linea in lineas:
                    pdc.TextOut(x, y, linea)
                    y += PrinterConfig.LINE_SPACING
                
                pdc.EndPage()
                pdc.EndDoc()
                pdc.DeleteDC()
                return True
                
            finally:
                win32print.ClosePrinter(hprinter)
                
        except Exception as e:
            print(f"Error al imprimir líneas: {e}")
            return False
    
    def validar_impresora(self, nombre_impresora: str) -> bool:
        """
        Valida que una impresora exista en el sistema.
        
        Args:
            nombre_impresora: Nombre de la impresora a validar
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return nombre_impresora in self._impresoras_disponibles


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

_printer_controller = None


def get_printer_controller() -> PrinterController:
    """
    Obtiene la instancia global del controlador de impresión.
    
    Returns:
        PrinterController: Controlador de impresión
    """
    global _printer_controller
    if _printer_controller is None:
        _printer_controller = PrinterController()
    return _printer_controller


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'PrinterController',
    'get_printer_controller'
]