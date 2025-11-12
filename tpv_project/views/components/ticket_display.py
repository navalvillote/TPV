"""
Componente de visualización de tickets.

Este módulo contiene los componentes para mostrar tickets en pantalla.
"""

from tkinter import Label, CENTER, N
from tkinter import font as tkfont
from typing import Optional
from config.settings import UIConfig


class TicketDisplay(Label):
    """Componente para mostrar tickets en pantalla."""
    
    def __init__(self, parent, ancho: int, alto: int, color_fondo: str):
        """
        Inicializa el display de ticket.
        
        Args:
            parent: Widget padre
            ancho: Ancho en caracteres
            alto: Alto en líneas
            color_fondo: Color de fondo
        """
        super().__init__(parent)
        
        self.ancho = ancho
        self.alto = alto
        self.color_fondo = color_fondo
        self.texto = ""
        self.extendido = False
        self.bloqueado = False
        
        # Crear fuente
        self.fuente = tkfont.Font(
            family=UIConfig.FONT_FAMILY,
            size=UIConfig.FONT_SIZE_SMALL,
            weight="bold"
        )
        
        self.config(
            font=self.fuente,
            width=self.ancho,
            height=self.alto,
            text=self.texto,
            justify=CENTER,
            anchor=N,
            bg=self.color_fondo
        )
    
    def actualizar_texto(self, texto: str) -> None:
        """
        Actualiza el texto del ticket.
        
        Args:
            texto: Nuevo texto del ticket
        """
        self.texto = texto
        self.config(text=texto)
    
    def limpiar(self) -> None:
        """Limpia el texto del ticket."""
        self.texto = ""
        self.config(text="")
    
    def extender(self) -> None:
        """Extiende el display (aumenta el alto)."""
        if not self.bloqueado and not self.extendido:
            self.alto = 45
            self.config(height=self.alto)
            self.extendido = True
    
    def contraer(self) -> None:
        """Contrae el display (reduce el alto)."""
        if not self.bloqueado and self.extendido:
            self.alto = 22
            self.config(height=self.alto)
            self.extendido = False
    
    def alternar_extension(self) -> None:
        """Alterna entre extendido y contraído."""
        if self.extendido:
            self.contraer()
        else:
            self.extender()
    
    def bloquear(self) -> None:
        """Bloquea el display (no permite cambios de tamaño)."""
        self.bloqueado = True
    
    def desbloquear(self) -> None:
        """Desbloquea el display."""
        self.bloqueado = False
    
    def esta_bloqueado(self) -> bool:
        """
        Verifica si el display está bloqueado.
        
        Returns:
            bool: True si está bloqueado
        """
        return self.bloqueado
    
    def esta_extendido(self) -> bool:
        """
        Verifica si el display está extendido.
        
        Returns:
            bool: True si está extendido
        """
        return self.extendido
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca el display en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


class PantallaNumerico(Label):
    """Pantalla para el teclado numérico."""
    
    def __init__(self, parent, color_fondo: str):
        """
        Inicializa la pantalla.
        
        Args:
            parent: Widget padre
            color_fondo: Color de fondo
        """
        super().__init__(parent)
        
        self.color_fondo = color_fondo
        self.texto = " "
        self.imagen_tk = None
        
        # Crear fuente
        self.fuente = tkfont.Font(
            family=UIConfig.FONT_FAMILY,
            size=UIConfig.FONT_SIZE_XXLARGE,
            weight="bold"
        )
        
        # Cargar imagen de fondo
        self._cargar_imagen_fondo()
        
        # Configurar
        self.config(
            font=self.fuente,
            text=self.texto,
            bg=self.color_fondo,
            fg='green2',
            justify=CENTER,
            compound="center"
        )
    
    def _cargar_imagen_fondo(self) -> None:
        """Carga la imagen de fondo de la pantalla."""
        try:
            from core.image_manager import get_image_manager
            from PIL import ImageTk
            
            image_manager = get_image_manager()
            imagen = image_manager.obtener_imagen('pantalla')
            
            if imagen:
                self.imagen_tk = ImageTk.PhotoImage(imagen)
                self.config(image=self.imagen_tk)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar imagen de pantalla: {e}")
    
    def actualizar_texto(self, texto: str) -> None:
        """
        Actualiza el texto de la pantalla.
        
        Args:
            texto: Nuevo texto
        """
        self.texto = texto if texto else " "
        self.config(text=self.texto)
    
    def limpiar(self) -> None:
        """Limpia la pantalla."""
        self.texto = " "
        self.config(text=self.texto)
    
    def obtener_texto(self) -> str:
        """
        Obtiene el texto actual.
        
        Returns:
            str: Texto actual
        """
        return self.texto if self.texto != " " else ""
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca la pantalla en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


class EtiquetaInfo(Label):
    """Etiqueta informativa con ancho ajustable."""
    
    def __init__(self, parent, texto: str, tamano_fuente: int,
                 color_texto: str, color_fondo: str, ancho: int):
        """
        Inicializa la etiqueta.
        
        Args:
            parent: Widget padre
            texto: Texto inicial
            tamano_fuente: Tamaño de fuente
            color_texto: Color del texto
            color_fondo: Color de fondo
            ancho: Ancho en caracteres
        """
        super().__init__(parent)
        
        self.texto = texto
        self.tamano_fuente = tamano_fuente
        self.color_texto = color_texto
        self.color_fondo = color_fondo
        self.ancho = ancho
        
        # Crear fuente
        self.fuente = tkfont.Font(
            family=UIConfig.FONT_FAMILY,
            size=self.tamano_fuente,
            weight="bold"
        )
        
        self.config(
            font=self.fuente,
            text=self.texto,
            width=self.ancho,
            height=1,
            bg=self.color_fondo,
            fg=self.color_texto,
            justify='left'
        )
    
    def actualizar_texto(self, texto: str) -> None:
        """
        Actualiza el texto de la etiqueta.
        
        Args:
            texto: Nuevo texto
        """
        self.texto = texto
        self.config(text=texto)
    
    def cambiar_ancho(self, ancho: int) -> None:
        """
        Cambia el ancho de la etiqueta.
        
        Args:
            ancho: Nuevo ancho en caracteres
        """
        self.ancho = ancho
        self.config(width=ancho)
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca la etiqueta en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'TicketDisplay',
    'PantallaNumerico',
    'EtiquetaInfo'
]