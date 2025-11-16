"""
Vista principal completa de la aplicación TPV.

Este módulo contiene la ventana principal integrada con todas las vistas:
- Panel principal de ventas
- Vista de calendario
- Vista de teclado virtual
"""

from tkinter import Tk, messagebox
from typing import Optional, List
from config.settings import (
    WindowConfig, ColorScheme, ICON_FILE, 
    ModeConfig, ProductConfig, TicketConfig
)
from views.components.base_widgets import BasePanel, ImageLabel, MarcoConImagen
from views.components.keyboard import TecladoNumerico
from views.components.ticket_display import TicketDisplay, PantallaNumerico, EtiquetaInfo
from views.calendar_view import CalendarView
from views.keyboard_view import KeyboardView
from controllers.receipt_controller import ReceiptController
from controllers.printer_controller import PrinterController
from controllers.calendar_controller import CalendarController
from data.data_manager import DataManager
from models.product import Product
from utils.formatters import formatear_numero_moneda, convertir_texto_multilnea


class MainWindow(Tk):
    """Ventana principal de la aplicación con todas las vistas integradas."""
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super().__init__()
        
        # Configuración básica de la ventana
        self.title(WindowConfig.TITLE)
        
        # Establecer icono
        try:
            self.iconbitmap(str(ICON_FILE))
        except:
            print("No se pudo cargar el icono")
        
        # Dimensiones
        self.minsize(WindowConfig.MIN_WIDTH, WindowConfig.MIN_HEIGHT)
        self.geometry(f"{WindowConfig.MIN_WIDTH}x{WindowConfig.MIN_HEIGHT}")
        
        # Controladores (se establecerán después)
        self.receipt_controller: Optional[ReceiptController] = None
        self.printer_controller: Optional[PrinterController] = None
        self.calendar_controller: Optional[CalendarController] = None
        self.data_manager: Optional[DataManager] = None
        
        # Variables de estado
        self.camarero_actual = ""
        self.camarero_anterior = ""
        self.modo_incremento = 1  # 1 para añadir, -1 para quitar

        # CORRECCIÓN: Variables para modo reordenar
        self.modo_reordenar_activo = False
        self.producto_reordenar_1 = None  # Primer producto seleccionado
        self.producto_reordenar_2 = None  # Segundo producto seleccionado
        
        # Contenedor principal
        self.contenedor: Optional[BasePanel] = None
        
        # Paneles del menú principal
        self.panel_principal: Optional[BasePanel] = None
        self.panel_productos_bebidas: Optional[BasePanel] = None
        self.panel_productos_comidas: Optional[BasePanel] = None
        self.panel_productos_otros: Optional[BasePanel] = None
        self.panel_impagos: Optional[BasePanel] = None
        self.panel_camareros: Optional[BasePanel] = None
        
        # Vistas adicionales
        self.calendar_view: Optional[CalendarView] = None
        self.keyboard_view: Optional[KeyboardView] = None
        
        # Componentes del panel principal
        self.panel_titulo: Optional[BasePanel] = None
        self.panel_numericos: Optional[BasePanel] = None
        self.panel_impresion: Optional[BasePanel] = None
        self.panel_pie: Optional[BasePanel] = None
        
        self.teclado_numerico: Optional[TecladoNumerico] = None
        self.pantalla_numerica: Optional[PantallaNumerico] = None
        self.ticket_display: Optional[TicketDisplay] = None
        
        # Controles del título
        self.logo: Optional[ImageLabel] = None
        self.boton_apagar: Optional[ImageLabel] = None
        self.boton_camarero: Optional[ImageLabel] = None
        self.etiqueta_camarero_actual: Optional[EtiquetaInfo] = None
        self.marco_camarero_anterior: Optional[MarcoConImagen] = None
        
        # Listas de componentes
        self.marcos_productos: List[MarcoConImagen] = []
        self.marcos_impagos: List[MarcoConImagen] = []
        self.marcos_camareros: List[MarcoConImagen] = []
        self.marcos_pie: List[MarcoConImagen] = []
        self.botones_pago: List[ImageLabel] = []
        
        # Vincular evento de teclado físico
        self.bind("<Key>", self._on_tecla_fisica)

        # CORRECCIÓN: Vincular evento de redimensionado
        self.bind("<Configure>", self._on_ventana_redimensionada)
    
    def establecer_controladores(self, receipt_controller: ReceiptController,
                                 printer_controller: PrinterController,
                                 calendar_controller: CalendarController,
                                 data_manager: DataManager) -> None:
        """
        Establece los controladores necesarios.
        
        Args:
            receipt_controller: Controlador de recibos
            printer_controller: Controlador de impresión
            calendar_controller: Controlador de calendario
            data_manager: Gestor de datos
        """
        self.receipt_controller = receipt_controller
        self.printer_controller = printer_controller
        self.calendar_controller = calendar_controller
        self.data_manager = data_manager
    
    def crear_interfaz(self) -> None:
        """Crea toda la interfaz de usuario."""
        self._crear_contenedor_principal()
        self._crear_panel_principal()
        self._crear_vistas_adicionales()
        
        # Mostrar panel principal por defecto
        # self.panel_principal.traer_al_frente()
    
    def _crear_contenedor_principal(self) -> None:
        """Crea el contenedor principal centrado."""
        self.contenedor = BasePanel(
            self,
            WindowConfig.MIN_WIDTH,
            WindowConfig.MIN_HEIGHT,
            WindowConfig.BACKGROUND_COLOR
        )
        self.contenedor.colocar(0, 0)
    
    def _crear_panel_principal(self) -> None:
        """Crea el panel principal de ventas."""
        self.panel_principal = BasePanel(
            self.contenedor,
            WindowConfig.MIN_WIDTH,
            WindowConfig.MIN_HEIGHT,
            ColorScheme.PRIMARY_BG
        )
        self.panel_principal.colocar(0, 0)
        
        # Crear componentes del panel principal
        self._crear_titulo()
        self._crear_panel_productos()
        self._crear_panel_numericos()
        self._crear_panel_impresion()
        self._crear_panel_pie()
        
        # CORRECCIÓN: Crear panel de camareros AL FINAL
        # para que quede por encima de todo
        self._crear_panel_camareros()
    
    def _crear_titulo(self) -> None:
        """Crea el panel del título con logo y controles."""
        self.panel_titulo = BasePanel(
            self.panel_principal,
            WindowConfig.MIN_WIDTH - 226,
            76,
            ColorScheme.PRIMARY_BG
        )
        self.panel_titulo.colocar(5, 5)
        
        x = 0
        y = 2
        
        # Logo
        self.logo = ImageLabel(
            self.panel_titulo,
            'logo',
            ColorScheme.PRIMARY_BG
        )
        self.logo.colocar(x, y)
        
        # Etiqueta informativa
        x += 95
        etiq_texto = 'Está atendiendo el camarero:'
        etiq = EtiquetaInfo(
            self.panel_titulo,
            etiq_texto,
            14,
            ColorScheme.TEXT_NORMAL,
            'gray92',
            38
        )
        etiq.colocar(x, y + 2)
        
        # Camarero actual
        self.etiqueta_camarero_actual = EtiquetaInfo(
            self.panel_titulo,
            '',
            14,
            'Gray10',
            'gray92',
            38
        )
        self.etiqueta_camarero_actual.colocar(x, y + 38)
        
        # Camarero anterior
        x += 395
        self.marco_camarero_anterior = MarcoConImagen(
            self.panel_titulo,
            '',
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.marco_camarero_anterior.colocar(x, y)
        self.marco_camarero_anterior.invertir_colores()
        self.marco_camarero_anterior.bind("<Button-1>", self._on_camarero_anterior_press)
        self.marco_camarero_anterior.bind("<ButtonRelease-1>", self._on_camarero_anterior_release)
        
        # Botón seleccionar camarero
        x += 158
        self.boton_camarero = ImageLabel(
            self.panel_titulo,
            'barman',
            ColorScheme.PRIMARY_BG
        )
        self.boton_camarero.colocar(x, y + 2)
        self.boton_camarero.bind("<Button-1>", self._on_boton_camarero_press)
        self.boton_camarero.bind("<ButtonRelease-1>", self._on_boton_camarero_release)
        
        # Botón apagar
        x += 77
        self.boton_apagar = ImageLabel(
            self.panel_titulo,
            'apagado',
            ColorScheme.PRIMARY_BG
        )
        self.boton_apagar.colocar(x, y)
        self.boton_apagar.bind("<Button-1>", self._on_apagar_press)
        self.boton_apagar.bind("<ButtonRelease-1>", self._on_apagar_release)
    
    def _crear_panel_productos(self) -> None:
        """Crea los paneles de productos."""
        ancho = WindowConfig.MIN_WIDTH - 232
        alto = WindowConfig.MIN_HEIGHT - 164
        
        # Panel bebidas
        self.panel_productos_bebidas = BasePanel(
            self.panel_principal,
            ancho,
            alto,
            ColorScheme.BEBIDAS
        )
        self.panel_productos_bebidas.colocar(5, 82)
        
        # Panel comidas
        self.panel_productos_comidas = BasePanel(
            self.panel_principal,
            ancho,
            alto,
            ColorScheme.COMIDAS
        )
        self.panel_productos_comidas.colocar(5, 82)
        
        # Panel otros
        self.panel_productos_otros = BasePanel(
            self.panel_principal,
            ancho,
            alto,
            ColorScheme.OTROS
        )
        self.panel_productos_otros.colocar(5, 82)
        
        # Panel impagos
        self.panel_impagos = BasePanel(
            self.panel_principal,
            ancho,
            alto,
            ColorScheme.PENDIENTE
        )
        self.panel_impagos.colocar(5, 82)
    
    def _crear_panel_numericos(self) -> None:
        """Crea el panel del teclado numérico."""
        self.panel_numericos = BasePanel(
            self.panel_principal,
            216,
            346,
            ColorScheme.SECONDARY_BG
        )
        self.panel_numericos.colocar(WindowConfig.MIN_WIDTH - 221, 5)
        
        # Pantalla
        self.pantalla_numerica = PantallaNumerico(
            self.panel_numericos,
            ColorScheme.SECONDARY_BG
        )
        self.pantalla_numerica.colocar(0, 0)
        
        # Teclado numérico
        self.teclado_numerico = TecladoNumerico(
            self.panel_numericos,
            216,
            280,
            ColorScheme.SECONDARY_BG
        )
        self.teclado_numerico.colocar(0, 62)
        self.teclado_numerico.vincular_callback(self._on_tecla_numerica)
    
    def _crear_panel_impresion(self) -> None:
        """Crea el panel de impresión con el ticket."""
        self.panel_impresion = BasePanel(
            self.panel_principal,
            216,
            412,
            ColorScheme.SECONDARY_BG
        )
        self.panel_impresion.colocar(WindowConfig.MIN_WIDTH - 221, 351)

        # CORRECCIÓN: Guardar posiciones y dimensiones originales del PANEL
        self.panel_impresion_x_original = WindowConfig.MIN_WIDTH - 221
        self.panel_impresion_y_original = 351
        self.panel_impresion_ancho_original = 216
        self.panel_impresion_alto_original = 412
        
        # CORRECCIÓN: Guardar posiciones y dimensiones originales
        self.ticket_x_original = 0
        self.ticket_y_original = 0
        self.ticket_ancho_original = 30
        self.ticket_alto_original = 22
        
        # Dimensiones expandidas
        self.ticket_ancho_expandido = 60  # Doble del ancho
        self.ticket_alto_expandido = 45   # Alto expandido
        
        # Ticket display
        self.ticket_display = TicketDisplay(
            self.panel_impresion,
            self.ticket_ancho_original,
            self.ticket_alto_original,
            ColorScheme.SECONDARY_BG
        )
        self.ticket_display.colocar(self.ticket_x_original, self.ticket_y_original)
        
        # CORRECCIÓN: Vincular clic para expansión personalizada
        self.ticket_display.bind("<Button-1>", self._on_ticket_click)
        
        # Botones de pago
        self._crear_botones_pago()
    
    def _crear_botones_pago(self) -> None:
        """Crea los botones de pago."""
        tipos_pago = ['efectivo', 'guardar', 'tarjeta']
        
        for i, tipo in enumerate(tipos_pago):
            x = i * 70 + 4
            y = 342
            
            nombre_imagen = f'tecla_{tipo}'
            boton = ImageLabel(self.panel_impresion, nombre_imagen, 
                             ColorScheme.SECONDARY_BG)
            boton.colocar(x, y)
            boton.tipo_pago = tipo
            
            boton.bind("<Button-1>", self._on_boton_pago_press)
            boton.bind("<ButtonRelease-1>", self._on_boton_pago_release)
            
            self.botones_pago.append(boton)
    
    def _crear_panel_pie(self) -> None:
        """Crea el panel del pie con opciones."""
        self.panel_pie = BasePanel(
            self.panel_principal,
            WindowConfig.MIN_WIDTH - 226,
            76,
            ColorScheme.PRIMARY_BG
        )
        self.panel_pie.colocar(5, WindowConfig.MIN_HEIGHT - 86)
        
        opciones = [
            ('AÑADIR\nCONSUMICION', 'modificar'),
            ('MOSTRAR\nCONSUMICIONES', 'consumiciones'),
            ('GESTIONAR\nPRODUCTOS', 'productos'),
            ('REORDENAR\nPRODUCTOS', 'ordenar'),
            ('TICKETS\nPENDIENTES\nDE PAGO', 'impagos')
        ]
        
        x = 3
        for texto, identificador in opciones:
            marco = MarcoConImagen(
                self.panel_pie,
                texto,
                'tecla_marco',
                12,
                ColorScheme.PRIMARY_BG
            )
            marco.colocar(x, 6)
            marco.invertir_colores()
            marco.identificador = identificador
            
            marco.bind("<Button-1>", self._on_boton_pie_press)
            marco.bind("<ButtonRelease-1>", self._on_boton_pie_release)
            
            self.marcos_pie.append(marco)
            x += 158
    
    def _crear_panel_camareros(self) -> None:
        """Crea el panel de selección de camareros."""
        # CORRECCIÓN: Dimensiones originales del área de productos
        ancho_original = WindowConfig.MIN_WIDTH - 232
        alto_original = WindowConfig.MIN_HEIGHT - 164
        
        self.panel_camareros = BasePanel(
            self.panel_principal,
            ancho_original,
            alto_original,
            'black'
        )
        self.panel_camareros.colocar(5, 82)
        
        # CORRECCIÓN: Guardar dimensiones y posiciones originales
        self.panel_camareros_ancho_original = ancho_original
        self.panel_camareros_alto_original = alto_original
        self.panel_camareros_x_original = 5
        self.panel_camareros_y_original = 82
        
        # Título (ajustado para el nuevo tamaño)
        self.titulo_camareros = EtiquetaInfo(
            self.panel_camareros,
            'SELECCIONE UN CAMARERO',
            16,
            'white',
            'black',
            50
        )
        self.titulo_camareros.colocar(50, 20)
    
    def _crear_vistas_adicionales(self) -> None:
        """Crea las vistas de calendario y teclado virtual."""
        # Vista de calendario
        self.calendar_view = CalendarView(
            self.contenedor,
            self.calendar_controller,
            self.printer_controller
        )
        self.calendar_view.colocar(0, 0)
        self.calendar_view.vincular_callback_volver(self._volver_desde_calendario)
        self.calendar_view.vincular_callback_impresoras(self._obtener_impresoras)
        self.calendar_view.establecer_iva(self.data_manager.iva)
        self.calendar_view.enviar_al_fondo()
        
        # Vista de teclado virtual
        self.keyboard_view = KeyboardView(self.contenedor)
        self.keyboard_view.colocar(0, 0)
        self.keyboard_view.vincular_callback_volver(self._volver_desde_teclado)
        self.keyboard_view.vincular_callback_guardar_producto(self._guardar_producto)
        self.keyboard_view.vincular_callback_eliminar_producto(self._eliminar_producto)
        self.keyboard_view.vincular_callback_seleccion_producto(self._obtener_productos_familia)
        self.keyboard_view.vincular_callback_guardar_pendiente(self._guardar_ticket_pendiente)
        self.keyboard_view.vincular_callback_eliminar_cliente(self._eliminar_cliente)
        self.keyboard_view.vincular_callback_agregar_cliente(self._agregar_cliente)
        self.keyboard_view.vincular_callback_verificar_password(self._verificar_password)

        # Vincular callbacks de camareros
        self.keyboard_view.vincular_callback_eliminar_camarero(self._eliminar_camarero)
        self.keyboard_view.vincular_callback_agregar_camarero(self._agregar_camarero)
        self.keyboard_view.vincular_callback_obtener_camareros(self._obtener_camareros)
        self.keyboard_view.vincular_callback_ver_tickets_camarero(self._ver_tickets_camarero)

        # Vincular callbacks de tickets pendientes
        self.keyboard_view.vincular_callback_cargar_clientes_filtrado(self._cargar_clientes_filtrado_callback)
        self.keyboard_view.vincular_callback_cargar_ticket_pendiente(self._cargar_ticket_pendiente_callback)
        self.keyboard_view.vincular_callback_unir_tickets(self._unir_tickets_callback)

        self.keyboard_view.enviar_al_fondo()

    # ========================================================================
    # MÉTODOS: Centrar ventana y redimensionar
    # ========================================================================

    def _on_ventana_redimensionada(self, event) -> None:
        """
        Maneja el evento de redimensionado de la ventana.
        Centra el contenedor principal.
        """
        # Solo procesar eventos de la ventana principal, no de widgets hijos
        if event.widget != self:
            return
        
        # Obtener dimensiones actuales de la ventana
        ancho_ventana = event.width
        alto_ventana = event.height
        
        # Si el contenedor existe, centrarlo
        if self.contenedor:
            self._centrar_contenedor(ancho_ventana, alto_ventana)

    def _centrar_contenedor(self, ancho_ventana: int, alto_ventana: int) -> None:
        """
        Centra el contenedor principal en la ventana.
        
        Args:
            ancho_ventana: Ancho actual de la ventana
            alto_ventana: Alto actual de la ventana
        """
        # Calcular posición centrada
        x_centrado = (ancho_ventana - WindowConfig.MIN_WIDTH) // 2
        y_centrado = (alto_ventana - WindowConfig.MIN_HEIGHT) // 2
        
        # Asegurar que no quede fuera de la ventana (valores negativos)
        x_centrado = max(0, x_centrado)
        y_centrado = max(0, y_centrado)
        
        # Reposicionar el contenedor
        self.contenedor.place(x=x_centrado, y=y_centrado)

    def maximizar_ventana(self) -> None:
        """Maximiza la ventana manteniendo el contenido centrado."""
        self.state('zoomed')  # Windows
        # Para Linux/Mac usar: self.attributes('-zoomed', True)

    def restaurar_ventana(self) -> None:
        """Restaura el tamaño normal de la ventana."""
        self.state('normal')
        self.geometry(f"{WindowConfig.MIN_WIDTH}x{WindowConfig.MIN_HEIGHT}")
        
    # ========================================================================
    # MÉTODOS: Expandir y contraer panel de camareros
    # ========================================================================

    def _expandir_panel_camareros(self) -> None:
        """Expande el panel de camareros para cubrir toda la pantalla."""
        # Cambiar tamaño a pantalla completa
        self.panel_camareros.config(
            width=WindowConfig.MIN_WIDTH,
            height=WindowConfig.MIN_HEIGHT
        )
        # Mover a posición (0, 0)
        self.panel_camareros.place(x=0, y=0)
        
        # Reposicionar el título
        self.titulo_camareros.place(x=WindowConfig.MIN_WIDTH // 2 - 300, y=20)


    def _contraer_panel_camareros(self) -> None:
        """Contrae el panel de camareros a su tamaño y posición original."""
        # Restaurar tamaño original
        self.panel_camareros.config(
            width=self.panel_camareros_ancho_original,
            height=self.panel_camareros_alto_original
        )
        # Restaurar posición original
        self.panel_camareros.place(
            x=self.panel_camareros_x_original,
            y=self.panel_camareros_y_original
        )
        
        # Reposicionar el título
        self.titulo_camareros.place(x=100, y=20)

    # ========================================================================
    # CARGA DE DATOS
    # ========================================================================
    
    def cargar_productos(self, productos: List[Product]) -> None:
        """Carga los productos en los paneles."""
        # Limpiar marcos existentes
        for marco in self.marcos_productos:
            marco.destroy()
        self.marcos_productos.clear()
        
        # Posiciones por familia
        posiciones = {
            'Bebida': {'x': 5, 'y': 5},
            'Comida': {'x': 5, 'y': 5},
            'Otros': {'x': 5, 'y': 5}
        }
        
        for producto in productos:
            familia = producto.familia
            
            # Determinar panel
            if familia == 'Bebida':
                panel = self.panel_productos_bebidas
            elif familia == 'Comida':
                panel = self.panel_productos_comidas
            else:
                panel = self.panel_productos_otros
            
            # Crear marco
            texto = convertir_texto_multilnea(producto.nombre).upper()
            marco = MarcoConImagen(
                panel,
                texto,
                'tecla_marco',
                12,
                panel.fondo
            )
            
            # Posicionar
            pos = posiciones[familia]
            marco.colocar(pos['x'], pos['y'])
            
            # Actualizar posición
            pos['x'] += 157
            if pos['x'] > 780:
                pos['x'] = 5
                pos['y'] += 75
            
            # Datos
            marco.nombre_producto = producto.nombre
            
            # Eventos
            marco.bind("<Button-1>", self._on_producto_press)
            marco.bind("<ButtonRelease-1>", self._on_producto_release)
            
            self.marcos_productos.append(marco)
        
        # Mostrar bebidas por defecto
        self.panel_productos_bebidas.traer_al_frente()
    
    def cargar_camareros(self) -> None:
        """Carga los camareros en el panel de selección."""
        # Limpiar marcos existentes
        for marco in self.marcos_camareros:
            marco.destroy()
        self.marcos_camareros.clear()
        
        # CORRECCIÓN: Obtener camareros desde la base de datos
        camareros = self.data_manager.waiters.obtener_todos()
        
        print(f"DEBUG: Camareros cargados desde DB: {camareros}")  # Para debug
        
        # Posición inicial (ajustada para el tamaño normal)
        x_inicio = 5
        y_inicio = 60  # Debajo del título
        x = x_inicio
        y = y_inicio
        ancho_boton = 152
        alto_boton = 70
        espaciado_x = 157
        espaciado_y = 75
        max_columnas = 5
        
        # Botón de gestión (primer botón)
        boton_gestion = MarcoConImagen(
            self.panel_camareros,
            'GESTIONAR\nCAMAREROS',
            'tecla_marco',
            14,
            self.panel_camareros.fondo
        )
        boton_gestion.colocar(x, y)
        boton_gestion.invertir_colores()
        boton_gestion.es_gestion = True
        boton_gestion.bind("<Button-1>", self._on_camarero_seleccion_press)
        boton_gestion.bind("<ButtonRelease-1>", self._on_camarero_seleccion_release)
        self.marcos_camareros.append(boton_gestion)
        
        # Avanzar a la siguiente posición
        x += espaciado_x
        columna = 1
        
        # CORRECCIÓN: Añadir cada camarero de la base de datos
        for camarero in camareros:
            # Control de posición (máximo 5 columnas)
            if columna >= max_columnas:
                x = x_inicio
                y += espaciado_y
                columna = 0
            
            # Formatear texto del camarero
            texto = convertir_texto_multilnea(camarero, 14).upper()
            
            # Crear marco para el camarero
            marco = MarcoConImagen(
                self.panel_camareros,
                texto,
                'tecla_marco',
                14,
                self.panel_camareros.fondo
            )
            marco.colocar(x, y)
            marco.nombre_camarero = camarero
            marco.es_gestion = False
            
            # Vincular eventos
            marco.bind("<Button-1>", self._on_camarero_seleccion_press)
            marco.bind("<ButtonRelease-1>", self._on_camarero_seleccion_release)
            
            self.marcos_camareros.append(marco)
            
            # Avanzar posición
            x += espaciado_x
            columna += 1
        
        print(f"DEBUG: Total marcos camareros creados: {len(self.marcos_camareros)}")


    
    def actualizar_impagos(self) -> None:
        """Actualiza el panel de tickets impagados."""
        # Limpiar existentes
        for marco in self.marcos_impagos:
            marco.destroy()
        self.marcos_impagos.clear()
        
        x = 5
        y = 5
        
        # Botón nuevo ticket (solo si no estamos en modo unir)
        if self.marcos_pie[4].texto == 'TICKETS\nPENDIENTES\nDE PAGO':
            boton_nuevo = MarcoConImagen(
                self.panel_impagos,
                'CREAR NUEVO\nTICKET',
                'tecla_marco',
                12,
                self.panel_impagos.fondo
            )
            boton_nuevo.colocar(x, y)
            boton_nuevo.invertir_colores()
            boton_nuevo.es_nuevo = True
            boton_nuevo.bind("<Button-1>", self._on_impago_press)
            boton_nuevo.bind("<ButtonRelease-1>", self._on_impago_release)
            self.marcos_impagos.append(boton_nuevo)
            
            x += 157
        
        # Tickets impagados
        recibos_pendientes = self.data_manager.receipts_pending
        
        for recibo in recibos_pendientes:
            if x > 780:
                x = 5
                y += 75
            
            texto = convertir_texto_multilnea(recibo.nombre).upper()
            marco = MarcoConImagen(
                self.panel_impagos,
                texto,
                'tecla_marco',
                12,
                self.panel_impagos.fondo
            )
            marco.colocar(x, y)
            marco.fecha_recibo = recibo.fecha
            marco.nombre_cliente = recibo.nombre
            marco.es_nuevo = False
            
            marco.bind("<Button-1>", self._on_impago_press)
            marco.bind("<ButtonRelease-1>", self._on_impago_release)
            
            self.marcos_impagos.append(marco)
            x += 157
    
    # ========================================================================
    # EVENTOS DE TECLADO NUMÉRICO
    # ========================================================================
        
    def _on_tecla_numerica(self, tecla: str) -> None:
        """Procesa las teclas del teclado numérico."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        # Obtener el texto sin el símbolo €
        texto_actual = self.pantalla_numerica.obtener_texto()
        # Limpiar el símbolo € si existe
        texto_actual = texto_actual.replace('€', '').strip()
        
        if tecla == 'del':
            nuevo_texto = formatear_numero_moneda('Delete', texto_actual)
        elif tecla == 'ok':
            if texto_actual:
                precio = float(texto_actual)
                self.receipt_controller.agregar_producto_varios(
                    precio,
                    self.modo_incremento
                )
                self._actualizar_ticket()
                nuevo_texto = ""
            else:
                nuevo_texto = texto_actual
        else:
            nuevo_texto = formatear_numero_moneda(tecla, texto_actual)
        
        if nuevo_texto:
            self.pantalla_numerica.actualizar_texto(nuevo_texto + '€')
        else:
            self.pantalla_numerica.limpiar()


    def _on_tecla_fisica(self, event) -> None:
        """Procesa las teclas del teclado físico."""
        tecla = event.keysym
        
        # Solo procesar en panel principal
        if self.panel_principal.winfo_ismapped():
            if tecla.isdigit():
                self._on_tecla_numerica(tecla)
            elif tecla in ['Delete', 'BackSpace']:
                self._on_tecla_numerica('del')
            elif tecla == 'Return':
                self._on_tecla_numerica('ok')
            elif tecla == 'Escape':
                self._salir()
    
    # ========================================================================
    # EVENTOS DE PRODUCTOS
    # ========================================================================
    
    def _on_producto_press(self, event) -> None:
        """Maneja el clic en un producto."""
        # Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        # CORRECCIÓN: Si estamos en modo reordenar
        if self.modo_reordenar_activo:
            self._manejar_seleccion_reordenar(event.widget)
            return
        
        # Modo normal: añadir/quitar producto
        event.widget.invertir_colores()
        
        nombre = event.widget.nombre_producto
        self.receipt_controller.agregar_producto(nombre, self.modo_incremento)
        self._actualizar_ticket()



    def _on_producto_release(self, event) -> None:
        """Maneja la liberación del clic en producto."""
        # Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        # CORRECCIÓN: Si estamos en modo reordenar, no hacer nada aquí
        if self.modo_reordenar_activo:
            return
        
        # Modo normal: restaurar colores
        event.widget.invertir_colores()
        

    # ========================================================================
    # EVENTOS DE PAGO
    # ========================================================================
    
    def _on_boton_pago_press(self, event) -> None:
        """Maneja el clic en botón de pago."""
        event.widget.invertir_colores()
    
    def _on_boton_pago_release(self, event) -> None:
        """Maneja la liberación del botón de pago."""
        # Si estamos en modo reordenar, salir
        if self.modo_reordenar_activo:
            self._cambiar_modo_reordenar()
        event.widget.invertir_colores()
        
        tipo = event.widget.tipo_pago
        
        if tipo == 'efectivo':
            self._pagar_efectivo()
        elif tipo == 'tarjeta':
            self._pagar_tarjeta()
        elif tipo == 'guardar':
            self._abrir_modo_guardar()
    
    def _pagar_efectivo(self) -> None:
        """Procesa el pago en efectivo."""
        if self.receipt_controller.recibo_tiene_productos():
            # Abrir caja
            if self.data_manager.printers[0]:
                self.printer_controller.abrir_caja_registradora(
                    self.data_manager.printers[0]
                )
            
            # Finalizar
            self.receipt_controller.finalizar_recibo_efectivo(self.camarero_actual)
            self._actualizar_ticket()
            self.pantalla_numerica.limpiar()
    
    def _pagar_tarjeta(self) -> None:
        """Procesa el pago con tarjeta."""
        if self.receipt_controller.recibo_tiene_productos():
            self.receipt_controller.finalizar_recibo_tarjeta(self.camarero_actual)
            self._actualizar_ticket()
            self.pantalla_numerica.limpiar()
    
    def _abrir_modo_guardar(self) -> None:
        """Abre el modo guardar ticket pendiente o gestión de tickets."""
        if self.receipt_controller.recibo_tiene_productos():
            # Si HAY productos en el ticket, abrir modo guardar ticket
            self.keyboard_view.cambiar_modo(ModeConfig.MODO_PENDIENTE)
            self.keyboard_view.establecer_texto_boton_volver('Volver')
            self.keyboard_view.traer_al_frente()
        else:
            # Si NO hay productos, abrir gestión de tickets pendientes
            self._abrir_gestion_tickets_pendientes()

    def _abrir_gestion_tickets_pendientes(self) -> None:
        """Abre la pantalla de gestión de tickets pendientes."""
        # Cambiar a modo pendiente
        self.keyboard_view.cambiar_modo(ModeConfig.MODO_PENDIENTE)
        self.keyboard_view.establecer_texto_boton_volver('Volver')
        
        # Cargar clientes con tickets pendientes
        self._cargar_clientes_con_tickets()
        
        # Mostrar vista
        self.keyboard_view.traer_al_frente()

    def _cargar_clientes_con_tickets(self) -> None:
        """Carga la lista de clientes con sus tickets pendientes."""
        # Obtener todos los recibos pendientes
        recibos_pendientes = self.data_manager.receipts_pending
        
        # Agrupar por cliente y contar tickets
        clientes_dict = {}
        for recibo in recibos_pendientes:
            nombre_cliente = recibo.nombre
            if nombre_cliente not in clientes_dict:
                clientes_dict[nombre_cliente] = {
                    'count': 0,
                    'total': 0.0
                }
            clientes_dict[nombre_cliente]['count'] += 1
            clientes_dict[nombre_cliente]['total'] += recibo.calcular_total()
        
        # Crear lista formateada
        items = []
        colores = []
        
        for nombre_cliente in sorted(clientes_dict.keys()):
            info = clientes_dict[nombre_cliente]
            tickets_count = info['count']
            total = info['total']
            
            # Formato: "Nombre Cliente - 3 tickets - 45.50€"
            item = f"{nombre_cliente} - {tickets_count} ticket{'s' if tickets_count > 1 else ''} - {total:.2f}€"
            items.append(item)
            
            # Color según número de tickets
            if tickets_count > 3:
                colores.append('red')  # Muchos tickets
            elif tickets_count > 1:
                colores.append('orange')  # Varios tickets
            else:
                colores.append('black')  # Un ticket
        
        # Cargar en el listado
        if items:
            self.keyboard_view.cargar_lista(items, colores)
            mensaje = f'{len(items)} cliente{"s" if len(items) > 1 else ""} con tickets pendientes'
        else:
            self.keyboard_view.cargar_lista(['No hay tickets pendientes'], None)
            mensaje = 'No hay tickets pendientes de pago'
        
        self.keyboard_view.actualizar_info(mensaje)
    
    # ========================================================================
    # EVENTOS DEL PIE
    # ========================================================================
    
    def _on_boton_pie_press(self, event) -> None:
        """Maneja el clic en botón del pie."""
        event.widget.invertir_colores()
    
    def _on_boton_pie_release(self, event) -> None:
        """Maneja la liberación del botón del pie."""
        event.widget.invertir_colores()
        
        identificador = event.widget.identificador
        
        # CORRECCIÓN: Si estamos en modo reordenar y pulsamos otro botón (no "ordenar")
        # salir automáticamente del modo reordenar
        if self.modo_reordenar_activo and identificador != 'ordenar':
            self._cambiar_modo_reordenar()  # Desactivar modo reordenar
        
        if identificador == 'modificar':
            self._cambiar_modo_modificar()
        elif identificador == 'consumiciones':
            self._cambiar_panel_productos()
        elif identificador == 'productos':
            self._abrir_gestion_productos()
        elif identificador == 'ordenar':
            # Llamar a _cambiar_modo_reordenar
            self._cambiar_modo_reordenar()
        elif identificador == 'impagos':
            self._mostrar_impagos()
    
    def _cambiar_modo_modificar(self) -> None:
        """Cambia entre modo añadir y quitar."""
        if self.modo_incremento == 1:
            self.modo_incremento = -1
            self.marcos_pie[0].cambiar_texto('QUITAR\nCONSUMICION')
            self._cambiar_color_productos('Gray18')
        else:
            self.modo_incremento = 1
            self.marcos_pie[0].cambiar_texto('AÑADIR\nCONSUMICION')
            self._restaurar_color_productos()
        
        # Invertir botones
        for marco in self.marcos_productos:
            marco.invertir_colores()
    
    def _cambiar_panel_productos(self) -> None:
        """Cambia entre paneles de productos."""
        texto = self.marcos_pie[1].texto
        
        if 'BEBIDAS' in texto or 'CONSUMICIONES' in texto:
            self.marcos_pie[1].cambiar_texto('MOSTRANDO\nCOMIDAS')
            self.panel_productos_comidas.traer_al_frente()
        elif 'COMIDAS' in texto:
            self.marcos_pie[1].cambiar_texto('MOSTRANDO\nOTROS')
            self.panel_productos_otros.traer_al_frente()
        else:
            self.marcos_pie[1].cambiar_texto('MOSTRANDO\nBEBIDAS')
            self.panel_productos_bebidas.traer_al_frente()
    
    def _abrir_gestion_productos(self) -> None:
        """Abre la gestión de productos."""
        self.keyboard_view.cambiar_modo(ModeConfig.MODO_PRODUCTO)
        
        # Cargar productos de la primera familia por defecto (Bebida)
        self.keyboard_view.producto_familia.cambiar_texto('Bebida')
        self.keyboard_view.producto_familia.datos = 'Bebida'
        
        # Cargar lista de productos
        productos_bebida = self.data_manager.products.obtener_productos_por_familia('Bebida')
        self.keyboard_view.listado.limpiar()
        for producto in productos_bebida:
            self.keyboard_view.listado.agregar_item(
                f"{producto.nombre} - {producto.precio:.2f}€"
            )
        
        self.keyboard_view.traer_al_frente()
    
    def _cambiar_modo_reordenar(self) -> None:
        """Activa/desactiva el modo reordenar productos."""
        if not self.modo_reordenar_activo:
            # ACTIVAR modo reordenar
            self.modo_reordenar_activo = True
            self.marcos_pie[3].cambiar_texto('SALIR DE\nREORDENAR')

            # CORRECCIÓN: Mostrar panel de productos (bebidas por defecto)
            self.panel_productos_bebidas.traer_al_frente()
            
            # Cambiar color de fondo de productos a color especial
            self._cambiar_color_productos(ColorScheme.REORDER)
            
            # Invertir colores de todos los productos
            for marco in self.marcos_productos:
                if not marco.invertido:
                    marco.invertir_colores()
            
            # Limpiar selecciones previas
            self.producto_reordenar_1 = None
            self.producto_reordenar_2 = None
            
        else:
            # DESACTIVAR modo reordenar
            self.modo_reordenar_activo = False
            self.marcos_pie[3].cambiar_texto('REORDENAR\nPRODUCTOS')
            
            # Restaurar colores originales
            self._restaurar_color_productos()
            
            # Restaurar estado de inversión
            for marco in self.marcos_productos:
                if marco.invertido:
                    marco.invertir_colores()
            
            # Limpiar selecciones
            self.producto_reordenar_1 = None
            self.producto_reordenar_2 = None
    
    def _mostrar_impagos(self) -> None:
        """Muestra el panel de tickets impagados."""
        texto_actual = self.marcos_pie[4].texto
        
        if 'UNIR TICKETS' in texto_actual:
            # Modo unir
            self.marcos_pie[4].cambiar_texto('TICKETS\nPENDIENTES\nDE PAGO')
            self.panel_impagos.cambiar_fondo(ColorScheme.PENDIENTE)
        else:
            # Modo normal
            self.marcos_pie[4].cambiar_texto('UNIR TICKETS\nDEL MISMO\nCLIENTE')
            self.panel_impagos.cambiar_fondo(ColorScheme.PENDIENTE_DARK)
        
        self.actualizar_impagos()
        self.panel_impagos.traer_al_frente()
    
    # ========================================================================
    # EVENTOS DE IMPAGOS
    # ========================================================================
    
    def _on_impago_press(self, event) -> None:
        """Maneja el clic en ticket impagado."""
        event.widget.invertir_colores()
    
    def _on_impago_release(self, event) -> None:
        """Maneja la liberación del clic en impagado."""
        event.widget.invertir_colores()
        
        if hasattr(event.widget, 'es_nuevo') and event.widget.es_nuevo:
            # Crear nuevo ticket
            self.pantalla_numerica.limpiar()
            self.receipt_controller.crear_nuevo_recibo(self.camarero_actual)
            self._actualizar_ticket()
            self.marcos_pie[4].cambiar_texto('GESTIÓN DE\nTICKETS')
            self.marcos_pie[1].cambiar_texto('MOSTRANDO\nBEBIDAS')
            self.panel_productos_bebidas.traer_al_frente()
        else:
            # Cargar ticket existente
            if 'UNIR TICKETS' in self.marcos_pie[4].texto:
                # Modo unir tickets del mismo cliente
                self._unir_tickets_cliente(event.widget.nombre_cliente)
            else:
                # Cargar ticket normal
                self.receipt_controller.cargar_recibo_pendiente(event.widget.fecha_recibo)
                self._actualizar_ticket()
                self.panel_productos_bebidas.traer_al_frente()
    
    def _unir_tickets_cliente(self, nombre_cliente: str) -> None:
        """Une todos los tickets de un cliente."""
        recibo_unido = self.receipt_controller.unir_recibos_pendientes_cliente(
            nombre_cliente
        )
        
        if recibo_unido:
            self.actualizar_impagos()
            self._actualizar_ticket()
    
    # ========================================================================
    # EVENTOS DE CAMAREROS
    # ========================================================================
    
    def _on_camarero_anterior_press(self, event) -> None:
        """Maneja el clic en camarero anterior."""
        event.widget.invertir_colores()
        
        if event.widget.texto:
            # Intercambiar camareros
            temp_nombre = self.camarero_actual
            temp_texto = self.etiqueta_camarero_actual.texto
            
            self.camarero_actual = self.camarero_anterior
            self.etiqueta_camarero_actual.actualizar_texto(self.camarero_anterior)
            
            self.camarero_anterior = temp_nombre
            self.marco_camarero_anterior.cambiar_texto(
                convertir_texto_multilnea(temp_nombre)
            )
    
    def _on_camarero_anterior_release(self, event) -> None:
        """Maneja la liberación del clic."""
        event.widget.invertir_colores()
    
    def _on_boton_camarero_press(self, event) -> None:
        """Maneja el clic en botón camarero."""
        event.widget.invertir_colores()
    
    def _on_boton_camarero_release(self, event) -> None:
        """Maneja la liberación del botón camarero."""
        # Si estamos en modo reordenar, salir
        if self.modo_reordenar_activo:
            self._cambiar_modo_reordenar()
        event.widget.invertir_colores()
        self.cargar_camareros()
        self.panel_camareros.traer_al_frente()
    
    def _on_camarero_seleccion_press(self, event) -> None:
        """Maneja el clic en selección de camarero."""
        event.widget.invertir_colores()
    
    def _on_camarero_seleccion_release(self, event) -> None:
        """Maneja la liberación de selección de camarero."""
        event.widget.invertir_colores()
        
        if hasattr(event.widget, 'es_gestion') and event.widget.es_gestion:
            # Abrir gestión de camareros
            self.keyboard_view.cambiar_modo(ModeConfig.MODO_CAMARERO)
            self.keyboard_view.traer_al_frente()
        else:
            # Seleccionar camarero
            if self.camarero_actual:
                self.camarero_anterior = self.camarero_actual
                self.marco_camarero_anterior.cambiar_texto(
                    convertir_texto_multilnea(self.camarero_actual)
                )
            
            self.camarero_actual = event.widget.nombre_camarero
            self.etiqueta_camarero_actual.actualizar_texto(self.camarero_actual)
            
            # CORRECCIÓN: Volver al panel principal y mostrar bebidas
            self._contraer_panel_camareros()
            self.panel_principal.traer_al_frente()
            self.panel_productos_bebidas.traer_al_frente()

    def _verificar_camarero_seleccionado(self) -> bool:
        """
        Verifica si hay un camarero seleccionado.
        
        Returns:
            bool: True si hay camarero seleccionado, False en caso contrario
        """
        if not self.camarero_actual:
            # CORRECCIÓN: Mostrar panel de camareros si no hay ninguno seleccionado
            self.panel_camareros.traer_al_frente()
            return False
        return True     
    
    def _on_apagar_press(self, event) -> None:
        """Maneja el clic en botón apagar."""
        event.widget.invertir_colores()
    
    def _on_apagar_release(self, event) -> None:
        """Maneja la liberación del botón apagar."""
        event.widget.invertir_colores()
        
        if messagebox.askyesno(
            "Apagar Sistema",
            "¿Está seguro que desea apagar el equipo?"
        ):
            import os
            os.system("shutdown /s /t 0")

    # ========================================================================
    # APLICAR VERIFICACIÓN EN TODOS LOS BOTONES PRINCIPALES
    # ========================================================================

    def _on_bebidas_press(self, event) -> None:
        """Maneja el clic en el botón de bebidas."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_bebidas_release(self, event) -> None:
        """Maneja la liberación del botón de bebidas."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.panel_productos_bebidas.traer_al_frente()


    def _on_comidas_press(self, event) -> None:
        """Maneja el clic en el botón de comidas."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_comidas_release(self, event) -> None:
        """Maneja la liberación del botón de comidas."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.panel_productos_comidas.traer_al_frente()


    def _on_otros_press(self, event) -> None:
        """Maneja el clic en el botón de otros."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_otros_release(self, event) -> None:
        """Maneja la liberación del botón de otros."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.panel_productos_otros.traer_al_frente()


    def _on_varios_press(self, event) -> None:
        """Maneja el clic en el botón de varios."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_varios_release(self, event) -> None:
        """Maneja la liberación del botón de varios."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_mas_press(self, event) -> None:
        """Maneja el clic en el botón de incremento."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_mas_release(self, event) -> None:
        """Maneja la liberación del botón de incremento."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.modo_incremento = not self.modo_incremento


    def _on_cobrar_press(self, event) -> None:
        """Maneja el clic en el botón de cobrar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_cobrar_release(self, event) -> None:
        """Maneja la liberación del botón de cobrar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self._cobrar()


    def _on_imprimir_press(self, event) -> None:
        """Maneja el clic en el botón de imprimir."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_imprimir_release(self, event) -> None:
        """Maneja la liberación del botón de imprimir."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.printer_controller.imprimir_ticket(
            self.receipt_controller.receipt,
            self.camarero_actual
        )


    def _on_limpiar_press(self, event) -> None:
        """Maneja el clic en el botón de limpiar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_limpiar_release(self, event) -> None:
        """Maneja la liberación del botón de limpiar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.receipt_controller.limpiar_ticket()
        self._actualizar_ticket()
        self.pantalla_numerica.limpiar()


    def _on_quitar_press(self, event) -> None:
        """Maneja el clic en el botón de quitar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_quitar_release(self, event) -> None:
        """Maneja la liberación del botón de quitar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.receipt_controller.quitar_ultimo()
        self._actualizar_ticket()


    def _on_pendiente_press(self, event) -> None:
        """Maneja el clic en el botón de pendiente."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_pendiente_release(self, event) -> None:
        """Maneja la liberación del botón de pendiente."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.keyboard_view.cambiar_modo(ModeConfig.MODO_PENDIENTE)
        self.keyboard_view.traer_al_frente()


    def _on_gestionar_press(self, event) -> None:
        """Maneja el clic en el botón de gestionar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_gestionar_release(self, event) -> None:
        """Maneja la liberación del botón de gestionar."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.keyboard_view.cambiar_modo(ModeConfig.MODO_PRODUCTO)
        self.keyboard_view.traer_al_frente()


    def _on_calendario_press(self, event) -> None:
        """Maneja el clic en el botón de calendario."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()


    def _on_calendario_release(self, event) -> None:
        """Maneja la liberación del botón de calendario."""
        # CORRECCIÓN: Verificar camarero antes de continuar
        if not self._verificar_camarero_seleccionado():
            return
        
        event.widget.invertir_colores()
        self.calendar_view.traer_al_frente()
    
    # ========================================================================
    # CALLBACKS PARA TECLADO VIRTUAL
    # ========================================================================

     
    def _volver_desde_teclado(self) -> None:
        """Vuelve desde el teclado virtual al panel principal."""
        # Actualizar productos si estábamos en modo producto

        if self.keyboard_view.modo_actual == ModeConfig.MODO_PRODUCTO:
            productos = self.data_manager.products.obtener_todos()
            self.cargar_productos(productos)
            print("DEBUG: Productos recargados al volver del teclado virtual")
        
        # Actualizar impagos si estábamos en modo pendiente
        elif self.keyboard_view.modo_actual == ModeConfig.MODO_PENDIENTE:
            self.actualizar_impagos()
            print("DEBUG: Impagos recargados al volver del teclado virtual")
        # Si estábamos en modo camarero, recargar lista de camareros
        elif self.keyboard_view.modo_actual == ModeConfig.MODO_CAMARERO:
            self.cargar_camareros()
            print("DEBUG: Camareros recargados al volver del teclado virtual")
        
        self.panel_principal.traer_al_frente()
    

    def _guardar_producto(self, nombre: str, precio: float, familia: str) -> bool:
        """
        Callback para guardar un producto.
        
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            from models.product import Product
            
            # Verificar si existe
            producto_existente = self.data_manager.products.obtener_producto(nombre)
            
            if producto_existente:
                # Actualizar
                self.data_manager.products.actualizar_producto(
                    nombre, precio, familia
                )
            else:
                # Crear nuevo
                producto = Product(nombre, precio, familia)
                self.data_manager.products.agregar_producto(producto)
            
            # Guardar
            self.data_manager.guardar_datos_generales()
            return True
            
        except Exception as e:
            print(f"Error al guardar producto: {e}")
            return False
    
    def _eliminar_producto(self, nombre: str) -> bool:
        """
        Callback para eliminar un producto.
        
        Returns:
            bool: True si se eliminó correctamente
        """
        try:
            exito = self.data_manager.products.eliminar_producto(nombre)
            
            if exito:
                self.data_manager.guardar_datos_generales()
            
            return exito
            
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            return False
    
    def _obtener_productos_familia(self, familia: str) -> List[Product]:
        """
        Callback para obtener productos de una familia.
        
        Returns:
            List[Product]: Lista de productos
        """
        return self.data_manager.products.obtener_productos_por_familia(familia)
    
    def _guardar_ticket_pendiente(self, nombre_cliente: str) -> bool:
        """
        Callback para guardar un ticket como pendiente.
        
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            self.receipt_controller.guardar_recibo_pendiente(
                nombre_cliente,
                self.camarero_actual
            )
            return True
            
        except Exception as e:
            print(f"Error al guardar ticket pendiente: {e}")
            return False
    
    def _eliminar_cliente(self, nombre_cliente: str) -> tuple:
        """
        Callback para eliminar un cliente.
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            # Verificar si tiene pendientes
            if self.data_manager.cliente_tiene_pendientes(nombre_cliente):
                return False, f"{nombre_cliente} tiene tickets pendientes de pago"
            
            # Eliminar
            exito = self.data_manager.customers.eliminar_cliente(nombre_cliente)
            
            if exito:
                self.data_manager.guardar_datos_generales()
                return True, f"{nombre_cliente} ha sido eliminado"
            else:
                return False, f"{nombre_cliente} no existe en la base de datos"
                
        except Exception as e:
            return False, f"Error al eliminar: {str(e)}"
    
    def _agregar_cliente(self, nombre_cliente: str) -> tuple:
        """
        Callback para agregar un cliente.
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            if self.data_manager.customers.existe_cliente(nombre_cliente):
                return False, f"{nombre_cliente} ya existe en la base de datos"
            
            self.data_manager.customers.agregar_cliente(nombre_cliente)
            self.data_manager.guardar_datos_generales()
            
            return True, f"{nombre_cliente} ha sido agregado"
            
        except Exception as e:
            return False, f"Error al agregar: {str(e)}"
    
    def _verificar_password(self, password: str) -> dict:
        """
        Callback para verificar password.
        
        Returns:
            dict: {'valido': bool, 'mensaje': str}
        """
        if password == self.data_manager.password:
            return {
                'valido': True,
                'mensaje': 'Acceso concedido'
            }
        else:
            return {
                'valido': False,
                'mensaje': 'Contraseña incorrecta'
            }
    
    # ========================================================================
    # CALLBACKS PARA CALENDARIO
    # ========================================================================
    
    def _volver_desde_calendario(self) -> None:
        """Vuelve desde el calendario al panel principal."""
        self.panel_principal.traer_al_frente()
        self.panel_productos_bebidas.traer_al_frente()
    
    def _obtener_impresoras(self) -> List[str]:
        """
        Callback para obtener lista de impresoras.
        
        Returns:
            List[str]: Lista de nombres de impresoras
        """
        return self.data_manager.printers
    
    # ========================================================================
    # CALLBACKS PARA CAMAREROS
    # ========================================================================

    def _eliminar_camarero(self, nombre_camarero: str) -> tuple:
        """
        Callback para eliminar un camarero.
        
        Args:
            nombre_camarero: Nombre del camarero a eliminar
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            # Verificar si existe
            if not self.data_manager.waiters.existe_camarero(nombre_camarero):
                return False, f"{nombre_camarero} no existe en el sistema"
            
            # Eliminar camarero
            exito = self.data_manager.waiters.eliminar_camarero(nombre_camarero)
            
            if exito:
                # Guardar cambios
                self.data_manager.guardar_datos_generales()
                
                # Recargar lista en panel principal
                self.cargar_camareros()
                
                return True, f"{nombre_camarero} ha sido eliminado"
            else:
                return False, f"Error al eliminar {nombre_camarero}"
                
        except Exception as e:
            return False, f"Error: {str(e)}"


    def _agregar_camarero(self, nombre_camarero: str) -> tuple:
        """
        Callback para agregar un camarero.
        
        Args:
            nombre_camarero: Nombre del camarero a agregar
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        try:
            # Validar nombre
            if not nombre_camarero or len(nombre_camarero.strip()) == 0:
                return False, "Debe ingresar un nombre válido"
            
            # Verificar si ya existe
            if self.data_manager.waiters.existe_camarero(nombre_camarero):
                return False, f"{nombre_camarero} ya existe en el sistema"
            
            # Agregar camarero
            self.data_manager.waiters.agregar_camarero(nombre_camarero)
            
            # Guardar cambios
            self.data_manager.guardar_datos_generales()
            
            # Recargar lista en panel principal
            self.cargar_camareros()
            
            return True, f"{nombre_camarero} ha sido agregado"
            
        except Exception as e:
            return False, f"Error: {str(e)}"


    def _obtener_camareros(self) -> List[str]:
        """
        Callback para obtener la lista de camareros.
        
        Returns:
            List[str]: Lista de nombres de camareros
        """
        try:
            return self.data_manager.waiters.obtener_todos()
        except Exception as e:
            print(f"Error al obtener camareros: {e}")
            return []


    def _ver_tickets_camarero(self, nombre_camarero: str) -> None:
        """
        Callback para ver los tickets de un camarero.
        
        Args:
            nombre_camarero: Nombre del camarero
        """
        try:
            # Ir a la vista de calendario con filtro de camarero
            self.calendar_view.establecer_filtro_camarero(nombre_camarero)
            self.calendar_view.traer_al_frente()
            self.calendar_view.inicializar()
            
        except Exception as e:
            print(f"Error al ver tickets del camarero: {e}")

    # ========================================================================
    # CALLBACKS TICKETS PENDIENTES
    # ========================================================================

    def _cargar_clientes_filtrado_callback(self, filtro: str) -> None:
        """
        Callback para cargar clientes según filtro.
        
        Args:
            filtro: 'todos', 'pendientes' o 'pagados'
        """
        if filtro == 'todos':
            # Todos los clientes (con y sin tickets)
            todos_clientes = self.data_manager.customers.obtener_todos()
            recibos_pendientes = self.data_manager.receipts_pending
            
            # Agrupar tickets por cliente
            tickets_por_cliente = {}
            for recibo in recibos_pendientes:
                nombre = recibo.nombre
                if nombre not in tickets_por_cliente:
                    tickets_por_cliente[nombre] = []
                tickets_por_cliente[nombre].append(recibo)
            
            # Crear lista
            items = []
            colores = []
            
            for cliente in sorted(todos_clientes):
                if cliente in tickets_por_cliente:
                    tickets = tickets_por_cliente[cliente]
                    count = len(tickets)
                    total = sum(r.calcular_total() for r in tickets)
                    item = f"{cliente} - {count} ticket{'s' if count > 1 else ''} - {total:.2f}€"
                    color = 'red' if count > 3 else 'orange' if count > 1 else 'black'
                else:
                    item = f"{cliente} - Sin tickets"
                    color = 'green'
                
                items.append(item)
                colores.append(color)
            
            self.keyboard_view.cargar_lista(items, colores)
            self.keyboard_view.actualizar_info(f'{len(items)} clientes totales')
        
        elif filtro == 'pendientes':
            # Solo clientes con tickets pendientes
            self._cargar_clientes_con_tickets()
        
        elif filtro == 'pagados':
            # Clientes sin tickets pendientes
            todos_clientes = self.data_manager.customers.obtener_todos()
            clientes_con_tickets = set(r.nombre for r in self.data_manager.receipts_pending)
            
            clientes_sin_tickets = [c for c in todos_clientes if c not in clientes_con_tickets]
            
            items = [f"{cliente} - Sin deudas" for cliente in sorted(clientes_sin_tickets)]
            colores = ['green'] * len(items)
            
            self.keyboard_view.cargar_lista(items, colores)
            self.keyboard_view.actualizar_info(f'{len(items)} clientes sin deudas')

    def _cargar_ticket_pendiente_callback(self, nombre_cliente: str) -> None:
        """
        Callback para cargar un ticket pendiente.
        
        Args:
            nombre_cliente: Nombre del cliente
        """
        # Obtener recibos del cliente
        recibos_cliente = self.data_manager.obtener_recibos_pendientes_cliente(nombre_cliente)
        
        if not recibos_cliente:
            self.keyboard_view.actualizar_info(f'{nombre_cliente} no tiene tickets pendientes')
            return
        
        # Si hay varios tickets, preguntar cuál cargar o unirlos
        if len(recibos_cliente) > 1:
            mensaje = f'{nombre_cliente} tiene {len(recibos_cliente)} tickets. Use "Unir Tickets" o seleccione uno específico'
            self.keyboard_view.actualizar_info(mensaje)
            return
        
        # Cargar el único ticket
        recibo = recibos_cliente[0]
        self.receipt_controller.establecer_recibo_actual(recibo)
        
        # Eliminar de pendientes (se volverá a guardar si no se paga)
        self.data_manager.eliminar_recibo_pendiente(recibo.fecha)
        self.data_manager.guardar_datos_generales()
        
        # Actualizar ticket en pantalla
        self._actualizar_ticket()
        
        # Volver al panel principal
        self.keyboard_view.enviar_al_fondo()
        self.panel_principal.traer_al_frente()
        self.panel_productos_bebidas.traer_al_frente()
        
        self.keyboard_view.actualizar_info(f'Ticket de {nombre_cliente} cargado')

    def _unir_tickets_callback(self, nombre_cliente: str) -> tuple:
        """
        Callback para unir todos los tickets de un cliente.
        
        Args:
            nombre_cliente: Nombre del cliente
        
        Returns:
            tuple: (bool, str) - (éxito, mensaje)
        """
        # Obtener recibos del cliente
        recibos_cliente = self.data_manager.obtener_recibos_pendientes_cliente(nombre_cliente)
        
        if not recibos_cliente:
            return False, f'{nombre_cliente} no tiene tickets pendientes'
        
        if len(recibos_cliente) == 1:
            return False, f'{nombre_cliente} solo tiene 1 ticket, no hay nada que unir'
        
        # Unir tickets
        recibo_unido = self.data_manager.unir_recibos_pendientes(nombre_cliente)
        
        if recibo_unido:
            # Guardar cambios
            self.data_manager.guardar_datos_generales()
            
            # Actualizar lista de impagos si está visible
            if self.panel_impagos.winfo_ismapped():
                self.actualizar_impagos()
            
            total = recibo_unido.calcular_total()
            return True, f'{len(recibos_cliente)} tickets unidos. Total: {total:.2f}€'
        
        return False, 'Error al unir tickets'
        
    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================
    
    def _actualizar_ticket(self) -> None:
        """Actualiza la visualización del ticket."""
        texto = self.receipt_controller.generar_texto_ticket()
        self.ticket_display.actualizar_texto(texto)

    def _on_ticket_click(self, event) -> None:
        """Maneja el clic en el ticket para expandir/contraer."""
        if self.ticket_display.esta_extendido():
            self._contraer_ticket()
        else:
            self._expandir_ticket()

    def _expandir_ticket(self) -> None:
        """Expande el ticket hacia la izquierda, arriba y abajo."""
        # Bloquear para evitar cambios durante expansión
        self.ticket_display.bloquear()
        
        # CORRECCIÓN: Calcular dimensiones expandidas
        ancho_expandido = self.panel_impresion_ancho_original * 2  # 432 (doble de 216)
        alto_expandido = self.panel_impresion_alto_original * 2    # 824 (doble de 412)
        
        # CORRECCIÓN: Calcular nueva posición X (mover hacia la izquierda)
        nuevo_x = self.panel_impresion_x_original - self.panel_impresion_ancho_original
        
        # CORRECCIÓN: Calcular nueva posición Y (mover hacia arriba)
        nuevo_y = self.panel_impresion_y_original - self.panel_impresion_alto_original
        
        # CORRECCIÓN: Ajustar para no salir de la pantalla por arriba
        if nuevo_y < 0:
            nuevo_y = 0
            alto_expandido = self.panel_impresion_y_original + self.panel_impresion_alto_original
        
        # Expandir el panel_impresion
        self.panel_impresion.config(width=ancho_expandido, height=alto_expandido)
        self.panel_impresion.place(x=nuevo_x, y=nuevo_y)
        
        # CORRECCIÓN: Traer el panel de impresión AL FRENTE por encima de todo
        self.panel_impresion.lift()
        self.panel_impresion.tkraise()
        
        # Expandir el ticket_display para llenar el panel
        self.ticket_display.config(
            width=self.ticket_ancho_expandido,
            height=self.ticket_alto_expandido
        )
        self.ticket_display.place(x=0, y=0)
        
        # CORRECCIÓN: Traer el ticket al frente también
        self.ticket_display.lift()
        
        # Marcar como extendido
        self.ticket_display.extendido = True
        
        # Reposicionar botones de pago en la parte inferior del panel expandido
        y_botones = alto_expandido - 76
        for i, boton in enumerate(self.botones_pago):
            x = i * 70 + 4
            boton.place(x=x, y=y_botones)
            # CORRECCIÓN: Asegurar que los botones estén al frente también
            boton.lift()
        
        # Ocultar teclado numérico y pantalla
        self.panel_numericos.enviar_al_fondo()


    def _contraer_ticket(self) -> None:
        """Contrae el ticket a su tamaño y posición original."""
        # Restaurar dimensiones originales del panel_impresion
        self.panel_impresion.config(width=216, height=412)
        self.panel_impresion.place(x=WindowConfig.MIN_WIDTH - 221, y=351)
        
        # Restaurar dimensiones del ticket_display
        self.ticket_display.config(
            width=self.ticket_ancho_original,
            height=self.ticket_alto_original
        )
        self.ticket_display.place(x=self.ticket_x_original, y=self.ticket_y_original)
        
        # Marcar como contraído
        self.ticket_display.extendido = False
        
        # Desbloquear
        self.ticket_display.desbloquear()
        
        # Restaurar posición de botones de pago
        y_botones = 342
        for i, boton in enumerate(self.botones_pago):
            x = i * 70 + 4
            boton.place(x=x, y=y_botones)
        
        # CORRECCIÓN: Restaurar orden de capas (z-order) original
        # Enviar panel de impresión a su capa normal
        self.panel_impresion.lower(self.panel_titulo)
        
        # Mostrar teclado numérico y pantalla
        self.panel_numericos.traer_al_frente()
        self.panel_numericos.lift()
    
    def _cambiar_color_productos(self, color: str) -> None:
        """Cambia el color de fondo de todos los productos."""
        for marco in self.marcos_productos:
            marco.cambiar_fondo(color)
        
        self.panel_productos_bebidas.cambiar_fondo(color)
        self.panel_productos_comidas.cambiar_fondo(color)
        self.panel_productos_otros.cambiar_fondo(color)
    
    def _restaurar_color_productos(self) -> None:
        """Restaura los colores originales de los productos."""
        for marco in self.marcos_productos:
            # Determinar color según familia
            producto_nombre = marco.nombre_producto
            producto = self.data_manager.products.obtener_producto(producto_nombre)
            
            if producto:
                if producto.familia == 'Bebida':
                    marco.cambiar_fondo(ColorScheme.BEBIDAS)
                elif producto.familia == 'Comida':
                    marco.cambiar_fondo(ColorScheme.COMIDAS)
                else:
                    marco.cambiar_fondo(ColorScheme.OTROS)
        
        self.panel_productos_bebidas.cambiar_fondo(ColorScheme.BEBIDAS)
        self.panel_productos_comidas.cambiar_fondo(ColorScheme.COMIDAS)
        self.panel_productos_otros.cambiar_fondo(ColorScheme.OTROS)

    def _manejar_seleccion_reordenar(self, marco_producto) -> None:
        """
        Maneja la selección de productos en modo reordenar.
        
        Args:
            marco_producto: Marco del producto seleccionado
        """
        # Si no hay primer producto seleccionado
        if self.producto_reordenar_1 is None:
            # Seleccionar como primer producto
            self.producto_reordenar_1 = marco_producto
            # CORRECCIÓN: DESACTIVAR (invertir para que se vea desactivado)
            if marco_producto.invertido:
                marco_producto.invertir_colores()
            return
        
        # Si se hace clic en el mismo producto (deseleccionar)
        if self.producto_reordenar_1 == marco_producto:
            # Deseleccionar (volver a activar)
            if not marco_producto.invertido:
                marco_producto.invertir_colores()
            self.producto_reordenar_1 = None
            return
        
        # Si ya hay un primer producto, este es el segundo
        self.producto_reordenar_2 = marco_producto
        
        # CORRECCIÓN: DESACTIVAR el segundo producto antes de intercambiar
        if marco_producto.invertido:
            marco_producto.invertir_colores()
        
        # Intercambiar posiciones
        self._intercambiar_productos()

    def _intercambiar_productos(self) -> None:
        """Intercambia las posiciones de dos productos seleccionados."""
        if not self.producto_reordenar_1 or not self.producto_reordenar_2:
            return
        
        # Obtener nombres de los productos
        nombre1 = self.producto_reordenar_1.nombre_producto
        nombre2 = self.producto_reordenar_2.nombre_producto
        
        # Obtener productos completos desde el gestor
        producto1 = self.data_manager.products.obtener_producto(nombre1)
        producto2 = self.data_manager.products.obtener_producto(nombre2)
        
        if not producto1 or not producto2:
            print(f"Error: No se encontraron los productos {nombre1} o {nombre2}")
            return
        
        # Verificar que sean de la misma familia
        if producto1.familia != producto2.familia:
            print(f"Error: Los productos deben ser de la misma familia")
            # CORRECCIÓN: Reactivar el primer producto (estaba desactivado)
            if not self.producto_reordenar_1.invertido:
                self.producto_reordenar_1.invertir_colores()
            # El segundo producto ya está desactivado, reactivarlo también
            if not self.producto_reordenar_2.invertido:
                self.producto_reordenar_2.invertir_colores()
            self.producto_reordenar_1 = None
            self.producto_reordenar_2 = None
            return
        
        # Obtener posiciones actuales
        pos1 = self.producto_reordenar_1.place_info()
        pos2 = self.producto_reordenar_2.place_info()
        
        # Intercambiar posiciones visuales
        self.producto_reordenar_1.place(x=pos2['x'], y=pos2['y'])
        self.producto_reordenar_2.place(x=pos1['x'], y=pos1['y'])
        
        # Intercambiar en la lista de marcos
        idx1 = self.marcos_productos.index(self.producto_reordenar_1)
        idx2 = self.marcos_productos.index(self.producto_reordenar_2)
        self.marcos_productos[idx1], self.marcos_productos[idx2] = \
            self.marcos_productos[idx2], self.marcos_productos[idx1]
        
        # Intercambiar en la base de datos
        self._intercambiar_productos_db(nombre1, nombre2)
        
        # CORRECCIÓN: REACTIVAR ambos productos (estaban desactivados)
        if not self.producto_reordenar_1.invertido:
            self.producto_reordenar_1.invertir_colores()
        if not self.producto_reordenar_2.invertido:
            self.producto_reordenar_2.invertir_colores()
        
        # Limpiar selecciones
        self.producto_reordenar_1 = None
        self.producto_reordenar_2 = None

    def _intercambiar_productos_db(self, nombre1: str, nombre2: str) -> None:
        """
        Intercambia el orden de dos productos en la base de datos.
        
        Args:
            nombre1: Nombre del primer producto
            nombre2: Nombre del segundo producto
        """
        # Obtener todos los productos
        todos_productos = self.data_manager.products.obtener_todos()
        
        # Encontrar índices
        idx1 = None
        idx2 = None
        
        for i, prod in enumerate(todos_productos):
            if prod.nombre == nombre1:
                idx1 = i
            elif prod.nombre == nombre2:
                idx2 = i
        
        if idx1 is not None and idx2 is not None:
            # Intercambiar en la lista
            todos_productos[idx1], todos_productos[idx2] = \
                todos_productos[idx2], todos_productos[idx1]
            
            # Limpiar y recargar productos en el gestor
            self.data_manager.products.limpiar()
            for producto in todos_productos:
                self.data_manager.products.agregar_producto(producto)
            
            # Guardar en disco
            self.data_manager.guardar_datos_generales()
            
            print(f"Productos intercambiados: {nombre1} ↔ {nombre2}")     
    
    def _salir(self) -> None:
        """Sale de la aplicación."""
        if messagebox.askyesno(
            "Salir",
            "¿Está seguro que desea salir de la aplicación?"
        ):
            # Guardar datos antes de salir
            try:
                self.data_manager.guardar_datos_generales()
                self.data_manager.guardar_recibos_anuales(
                    self.receipt_controller.receipt_manager
                )
            except Exception as e:
                print(f"Error al guardar datos: {e}")
            
            self.destroy()
    
    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================
    
    def inicializar_datos(self) -> None:
        """Inicializa los datos al arrancar la aplicación."""
        # Cargar productos
        productos = self.data_manager.products.obtener_todos()
        self.cargar_productos(productos)
        
        # Actualizar ticket inicial
        self._actualizar_ticket()
        
        # Cargar impagos
        self.actualizar_impagos()
        
        # CORRECCIÓN: Verificar que hay camareros en la DB
        camareros = self.data_manager.waiters.obtener_todos()
        print(f"DEBUG inicializar_datos: Camareros en DB: {camareros}")
        
        # CORRECCIÓN: Cargar camareros en el panel
        self.cargar_camareros()
        
        # CORRECCIÓN: Establecer que NO hay camarero seleccionado
        self.camarero_actual = None
        
        # CORRECCIÓN: Actualizar etiqueta
        self.etiqueta_camarero_actual.actualizar_texto('(Seleccione camarero)')
        
        # CORRECCIÓN: Expandir panel de camareros para cubrir toda la pantalla
        self._expandir_panel_camareros()
        
        # CORRECCIÓN: Mostrar panel de camareros al inicio (traer al frente)
        self.panel_camareros.traer_al_frente()


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'MainWindow'
]