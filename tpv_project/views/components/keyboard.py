"""
Componente de teclado virtual.

Este módulo contiene el teclado virtual alfanumérico y numérico.
"""

from typing import Callable, List, Optional
from tkinter import Frame
from config.settings import KeyboardConfig, UIConfig
from views.components.base_widgets import BasePanel, MarcoConImagen
from utils.formatters import convertir_texto_multilnea


class TecladoVirtual(BasePanel):
    """Teclado virtual alfanumérico completo."""
    
    def __init__(self, parent, ancho: int, alto: int, fondo: str):
        """
        Inicializa el teclado virtual.
        
        Args:
            parent: Widget padre
            ancho: Ancho del teclado
            alto: Alto del teclado
            fondo: Color de fondo
        """
        super().__init__(parent, ancho, alto, fondo)
        
        self.teclas: List[MarcoConImagen] = []
        self.mayusculas = True
        self.callback_tecla: Optional[Callable] = None
        
        self._crear_teclas()
    
    def _crear_teclas(self) -> None:
        """Crea todas las teclas del teclado."""
        y = -65
        
        for fila in KeyboardConfig.TECLAS:
            y += 70
            x = -30
            
            for tecla in fila:
                tipo = 'tecla'
                
                # Determinar tipo de tecla y posición
                if tecla == '7':
                    x += 30
                elif tecla == '4':
                    x += 30
                elif tecla == '1':
                    x += 30
                elif tecla == 'Space':
                    tipo = 'tecla_space'
                    x += 70
                elif tecla == 'Shift':
                    tipo = 'tecla_doble'
                elif tecla == 'Delete':
                    tipo = 'tecla_doble'
                    x += 350
                elif tecla == '0':
                    tipo = 'tecla_doble'
                    x += 100
                elif tecla == '.':
                    x += 70
                
                x += 70
                
                # Crear tecla
                marco = MarcoConImagen(
                    self,
                    tecla,
                    tipo,
                    UIConfig.FONT_SIZE_XLARGE,
                    self.fondo
                )
                marco.colocar(x, y)
                
                # Invertir colores para teclas no numéricas
                if not tecla.isnumeric() and tipo != 'tecla_space':
                    marco.invertir_colores()
                
                # Vincular eventos
                marco.bind("<Button-1>", self._on_tecla_press)
                marco.bind("<ButtonRelease-1>", self._on_tecla_release)
                
                # Guardar referencia
                self.teclas.append(marco)
    
    def _on_tecla_press(self, event) -> None:
        """Maneja el evento de presionar una tecla."""
        event.widget.invertir_colores()
        
        if self.callback_tecla:
            tecla = event.widget.texto
            self.callback_tecla(tecla)
    
    def _on_tecla_release(self, event) -> None:
        """Maneja el evento de soltar una tecla."""
        event.widget.invertir_colores()
    
    def cambiar_mayusculas(self) -> None:
        """Cambia entre mayúsculas y minúsculas."""
        for tecla in self.teclas:
            texto = tecla.texto
            
            if texto.isalpha() and len(texto) == 1:
                if self.mayusculas:
                    tecla.cambiar_texto(texto.lower())
                else:
                    tecla.cambiar_texto(texto.upper())
        
        self.mayusculas = not self.mayusculas
    
    def vincular_callback(self, callback: Callable[[str], None]) -> None:
        """
        Vincula una función callback para cuando se presiona una tecla.
        
        Args:
            callback: Función que recibe la tecla presionada
        """
        self.callback_tecla = callback
    
    def obtener_estado_mayusculas(self) -> bool:
        """
        Obtiene el estado actual de mayúsculas.
        
        Returns:
            bool: True si está en mayúsculas, False si está en minúsculas
        """
        return self.mayusculas


class TecladoNumerico(BasePanel):
    """Teclado numérico para el panel principal."""
    
    def __init__(self, parent, ancho: int, alto: int, fondo: str):
        """
        Inicializa el teclado numérico.
        
        Args:
            parent: Widget padre
            ancho: Ancho del teclado
            alto: Alto del teclado
            fondo: Color de fondo
        """
        super().__init__(parent, ancho, alto, fondo)
        
        self.teclas: List[MarcoConImagen] = []
        self.callback_tecla: Optional[Callable] = None
        
        self._crear_teclas()
    
    def _crear_teclas(self) -> None:
        """Crea todas las teclas del teclado numérico."""
        teclas_num = ['7', '8', '9', '4', '5', '6', '1', '2', '3', 
                      'del', '0', 'ok']
        
        contador = 0
        for y_idx in range(4):
            posy = y_idx * 70 + 3
            for x_idx in range(3):
                posx = x_idx * 70 + 3
                
                tecla = teclas_num[contador]
                
                marco = MarcoConImagen(
                    self,
                    tecla.upper(),
                    'tecla',
                    UIConfig.FONT_SIZE_LARGE,
                    self.fondo
                )
                marco.colocar(posx, posy)
                
                # Datos adicionales
                marco.tecla_valor = tecla
                
                # Invertir colores para teclas no numéricas
                if not tecla.isnumeric():
                    marco.invertir_colores()
                
                # Vincular eventos
                marco.bind("<Button-1>", self._on_tecla_press)
                marco.bind("<ButtonRelease-1>", self._on_tecla_release)
                
                self.teclas.append(marco)
                contador += 1
    
    def _on_tecla_press(self, event) -> None:
        """Maneja el evento de presionar una tecla."""
        event.widget.invertir_colores()
        
        if self.callback_tecla:
            tecla = event.widget.tecla_valor
            self.callback_tecla(tecla)
    
    def _on_tecla_release(self, event) -> None:
        """Maneja el evento de soltar una tecla."""
        event.widget.invertir_colores()
    
    def vincular_callback(self, callback: Callable[[str], None]) -> None:
        """
        Vincula una función callback para cuando se presiona una tecla.
        
        Args:
            callback: Función que recibe la tecla presionada
        """
        self.callback_tecla = callback


class GestorEntradaTexto:
    """Gestiona la entrada de texto desde el teclado virtual."""
    
    def __init__(self):
        """Inicializa el gestor de entrada."""
        self.texto = ""
        self.modo_escritura = "nombres"  # nombres, productos, monedas, password
        self.mayusculas = True
        self.max_lineas = KeyboardConfig.MAX_LINES
        self.max_chars_linea = KeyboardConfig.MAX_CHARS_PER_LINE
    
    def procesar_tecla(self, tecla: str) -> str:
        """
        Procesa una tecla presionada y actualiza el texto.
        
        Args:
            tecla: Tecla presionada
            
        Returns:
            str: Texto actualizado
        """
        if tecla == 'Shift':
            self.mayusculas = not self.mayusculas
            return self.texto
        
        elif tecla == 'Delete':
            if len(self.texto) > 0:
                self.texto = self.texto[:-1]
                if len(self.texto) == 0:
                    self.texto = ""
        
        elif tecla == 'Space':
            if self.texto != '':
                if self.texto[-1] != ' ':
                    self.texto += ' '
        
        else:
            # Agregar carácter
            self.texto += tecla
        
        # Controlar saltos de línea
        self._controlar_formato()
        
        return self.texto
    
    def _controlar_formato(self) -> None:
        """Controla el formato del texto (saltos de línea, límites)."""
        if self.modo_escritura in ['nombres', 'productos']:
            texto_formateado = convertir_texto_multilnea(
                self.texto,
                self.max_chars_linea
            )
            
            saltos = texto_formateado.count('\n')
            
            if saltos > self.max_lineas:
                # Eliminar último carácter
                self.texto = self.texto[:-1]
    
    def aplicar_modo_nombres(self) -> None:
        """Aplica lógica de nombres propios (primera letra mayúscula)."""
        if len(self.texto) == 0:
            if not self.mayusculas:
                self.mayusculas = True
        else:
            if self.texto[-1] == ' ':
                if not self.mayusculas:
                    self.mayusculas = True
            else:
                if self.mayusculas:
                    self.mayusculas = False
    
    def aplicar_modo_productos(self) -> None:
        """Aplica lógica de productos (solo primera letra mayúscula)."""
        if len(self.texto) == 0:
            if not self.mayusculas:
                self.mayusculas = True
        else:
            if self.mayusculas:
                self.mayusculas = False
    
    def limpiar(self) -> None:
        """Limpia el texto."""
        self.texto = ""
    
    def establecer_texto(self, texto: str) -> None:
        """
        Establece el texto directamente.
        
        Args:
            texto: Texto a establecer
        """
        self.texto = texto
    
    def obtener_texto(self) -> str:
        """
        Obtiene el texto actual.
        
        Returns:
            str: Texto actual
        """
        return self.texto
    
    def establecer_modo(self, modo: str) -> None:
        """
        Establece el modo de escritura.
        
        Args:
            modo: Modo ('nombres', 'productos', 'monedas', 'password')
        """
        self.modo_escritura = modo


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'TecladoVirtual',
    'TecladoNumerico',
    'GestorEntradaTexto'
]