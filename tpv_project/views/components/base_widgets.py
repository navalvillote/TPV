"""
Componentes base de la interfaz.

Este módulo contiene las clases base para crear widgets personalizados.
"""

from tkinter import Frame, Label, Listbox, Scrollbar, LEFT, RIGHT, Y, BOTH, N, CENTER
from tkinter import font as tkfont
from typing import Optional, Callable
from PIL import ImageTk
from config.settings import UIConfig, ColorScheme
from core.image_manager import get_image_manager


class BasePanel(Frame):
    """Panel base personalizado."""
    
    def __init__(self, parent, ancho: int, alto: int, fondo: str):
        """
        Inicializa el panel.
        
        Args:
            parent: Widget padre
            ancho: Ancho del panel
            alto: Alto del panel
            fondo: Color de fondo
        """
        super().__init__(parent)
        self.ancho = ancho
        self.alto = alto
        self.fondo = fondo
        
        self.config(
            bg=self.fondo,
            width=self.ancho,
            height=self.alto
        )
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca el panel en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)
    
    def expandir(self) -> None:
        """Expande el panel para ocupar todo el espacio disponible."""
        self.pack(fill=BOTH, expand=True)
        self.pack_propagate(False)
    
    def cambiar_fondo(self, color: str) -> None:
        """
        Cambia el color de fondo.
        
        Args:
            color: Nuevo color
        """
        self.fondo = color
        self.config(bg=self.fondo)
    
    def traer_al_frente(self) -> None:
        """Trae el panel al frente."""
        self.tkraise()
    
    def enviar_al_fondo(self) -> None:
        """Envía el panel al fondo."""
        self.lower()


class BaseLabel(Label):
    """Label base personalizado."""
    
    def __init__(self, parent, texto: str, tamano_fuente: int,
                 color_texto: str, color_fondo: str):
        """
        Inicializa el label.
        
        Args:
            parent: Widget padre
            texto: Texto del label
            tamano_fuente: Tamaño de la fuente
            color_texto: Color del texto
            color_fondo: Color de fondo
        """
        super().__init__(parent)
        
        self.texto = texto
        self.tamano_fuente = tamano_fuente
        self.color_texto = color_texto
        self.color_fondo = color_fondo
        
        # Crear fuente
        self.fuente = tkfont.Font(
            family=UIConfig.FONT_FAMILY,
            size=self.tamano_fuente,
            weight="bold"
        )
        
        self.config(
            font=self.fuente,
            text=self.texto,
            bg=self.color_fondo,
            fg=self.color_texto
        )
    
    def cambiar_texto(self, nuevo_texto: str) -> None:
        """
        Cambia el texto del label.
        
        Args:
            nuevo_texto: Nuevo texto
        """
        self.texto = nuevo_texto
        self.config(text=nuevo_texto)
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca el label en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


class ImageLabel(Label):
    """Label con imagen."""
    
    def __init__(self, parent, nombre_imagen: str, color_fondo: str):
        """
        Inicializa el label con imagen.
        
        Args:
            parent: Widget padre
            nombre_imagen: Nombre de la imagen
            color_fondo: Color de fondo
        """
        super().__init__(parent)
        
        self.nombre_imagen = nombre_imagen
        self.color_fondo = color_fondo
        self.invertido = False
        
        # Cargar imagen
        self._cargar_imagen()
        
        self.config(bg=self.color_fondo)
    
    def _cargar_imagen(self) -> None:
        """Carga la imagen desde el gestor de imágenes."""
        image_manager = get_image_manager()
        
        sufijo = '_p' if self.invertido else ''
        nombre_completo = f'{self.nombre_imagen}{sufijo}'
        
        imagen = image_manager.obtener_imagen(nombre_completo)
        
        if imagen:
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.config(image=self.imagen_tk)
        else:
            print(f"Imagen no encontrada: {nombre_completo}")
    
    def invertir_colores(self) -> None:
        """Invierte los colores de la imagen."""
        self.invertido = not self.invertido
        self._cargar_imagen()
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca el label en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


class MarcoConImagen(Label):
    """Marco con imagen y texto superpuesto."""
    
    def __init__(self, parent, texto: str, nombre_imagen: str,
                 tamano_fuente: int, color_fondo: str):
        """
        Inicializa el marco.
        
        Args:
            parent: Widget padre
            texto: Texto a mostrar
            nombre_imagen: Nombre de la imagen de fondo
            tamano_fuente: Tamaño de la fuente
            color_fondo: Color de fondo
        """
        super().__init__(parent)
        
        self.texto = texto
        self.nombre_imagen = nombre_imagen
        self.tamano_fuente = tamano_fuente
        self.color_fondo = color_fondo
        self.invertido = False
        self.color_texto = ColorScheme.TEXT_NORMAL
        self.color_texto_alt = ColorScheme.TEXT_DARK
        
        # Crear fuente
        self.fuente = tkfont.Font(
            family=UIConfig.FONT_FAMILY,
            size=self.tamano_fuente,
            weight="bold"
        )
        
        self._actualizar()
        
        self.pack_propagate(False)
    
    def _actualizar(self) -> None:
        """Actualiza la apariencia del marco."""
        # Determinar colores
        color_final = self.color_texto if self.invertido else self.color_texto_alt
        
        # Cargar imagen
        image_manager = get_image_manager()
        sufijo = '_p' if self.invertido else ''
        nombre_completo = f'{self.nombre_imagen}{sufijo}'
        
        imagen = image_manager.obtener_imagen(nombre_completo)
        
        if imagen:
            self.imagen_tk = ImageTk.PhotoImage(imagen)
            self.config(image=self.imagen_tk)
        
        # Configurar
        self.config(
            font=self.fuente,
            compound="center",
            text=self.texto,
            bg=self.color_fondo,
            fg=color_final,
            justify=CENTER
        )
    
    def cambiar_texto(self, nuevo_texto: str) -> None:
        """
        Cambia el texto del marco.
        
        Args:
            nuevo_texto: Nuevo texto
        """
        self.texto = nuevo_texto
        self.config(text=nuevo_texto)
    
    def cambiar_fondo(self, color: str) -> None:
        """
        Cambia el color de fondo del marco.
        
        Args:
            color: Nuevo color de fondo
        """
        self.color_fondo = color
        self.config(bg=color)
    
    def invertir_colores(self) -> None:
        """Invierte los colores del marco."""
        self.invertido = not self.invertido
        self._actualizar()
    
    def colocar(self, x: int, y: int) -> None:
        """
        Coloca el marco en una posición.
        
        Args:
            x: Posición X
            y: Posición Y
        """
        self.place(x=x, y=y)


class ListaConScroll(Frame):
    """Lista con barra de scroll."""
    
    def __init__(self, parent):
        """
        Inicializa la lista.
        
        Args:
            parent: Widget padre
        """
        super().__init__(parent)
        
        # Crear listbox
        self.listbox = Listbox(
            self,
            font=(UIConfig.FONT_FAMILY, UIConfig.FONT_SIZE_MEDIUM),
            exportselection=False
        )
        
        # Crear scrollbar
        self.scrollbar = Scrollbar(self)
        
        # Sincronizar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        
        # Colocar
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)
    
    def expandir(self) -> None:
        """Expande la lista para ocupar todo el espacio."""
        self.pack(fill=BOTH, expand=True)
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    def limpiar(self) -> None:
        """Limpia todos los elementos de la lista."""
        self.listbox.delete(0, 'end')
    
    def agregar_item(self, texto: str, color: Optional[str] = None) -> None:
        """
        Agrega un item a la lista.
        
        Args:
            texto: Texto del item
            color: Color del texto (opcional)
        """
        self.listbox.insert('end', texto)
        
        if color:
            self.listbox.itemconfig(self.listbox.size() - 1, {'fg': color})
    
    def obtener_seleccion(self) -> Optional[str]:
        """
        Obtiene el item seleccionado.
        
        Returns:
            Optional[str]: Texto del item o None si no hay selección
        """
        seleccion = self.listbox.curselection()
        if seleccion:
            return self.listbox.get(seleccion[0])
        return None
    
    def obtener_indice_seleccion(self) -> Optional[int]:
        """
        Obtiene el índice del item seleccionado.
        
        Returns:
            Optional[int]: Índice o None si no hay selección
        """
        seleccion = self.listbox.curselection()
        if seleccion:
            return seleccion[0]
        return None
    
    def vincular_evento_seleccion(self, callback: Callable) -> None:
        """
        Vincula un evento cuando se selecciona un item.
        
        Args:
            callback: Función a llamar cuando se selecciona
        """
        self.listbox.bind("<<ListboxSelect>>", callback)


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'BasePanel',
    'BaseLabel',
    'ImageLabel',
    'MarcoConImagen',
    'ListaConScroll'
]