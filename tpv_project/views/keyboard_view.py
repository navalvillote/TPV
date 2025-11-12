"""
Vista del teclado virtual con sus diferentes modos.

Este módulo contiene la interfaz completa del teclado virtual y sus
modos de operación (Producto, Pendiente, Camarero, Password).
"""

from typing import Optional, Callable, List
from tkinter import END
from config.settings import WindowConfig, ColorScheme, ModeConfig, ProductConfig
from views.components.base_widgets import BasePanel, MarcoConImagen, ListaConScroll
from views.components.keyboard import TecladoVirtual, GestorEntradaTexto
from views.components.ticket_display import EtiquetaInfo
from utils.formatters import convertir_texto_multilnea, formatear_numero_moneda
from utils.validators import sanitizar_texto


class KeyboardView(BasePanel):
    """Vista del teclado virtual con diferentes modos de operación."""
    
    def __init__(self, parent):
        """
        Inicializa la vista del teclado.
        
        Args:
            parent: Widget padre
        """
        super().__init__(
            parent,
            WindowConfig.MIN_WIDTH,
            WindowConfig.MIN_HEIGHT,
            ColorScheme.PRIMARY_BG
        )
        
        # Componentes principales
        self.teclado: Optional[TecladoVirtual] = None
        self.panel_teclado: Optional[BasePanel] = None
        self.panel_ocultar: Optional[BasePanel] = None
        self.panel_listado: Optional[BasePanel] = None  # Panel contenedor del listado
        self.entrada: Optional[MarcoConImagen] = None
        self.boton_volver: Optional[MarcoConImagen] = None
        self.info: Optional[EtiquetaInfo] = None
        self.listado: Optional[ListaConScroll] = None
        
        # Paneles de modos
        self.panel_modos: Optional[BasePanel] = None
        self.panel_producto: Optional[BasePanel] = None
        self.panel_pendiente: Optional[BasePanel] = None
        self.panel_camarero: Optional[BasePanel] = None
        self.panel_password: Optional[BasePanel] = None
        
        # Gestor de entrada
        self.gestor_entrada = GestorEntradaTexto()
        
        # Estado
        self.modo_actual = ModeConfig.MODO_PRODUCTO
        self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
        
        # Callbacks
        self.callback_volver: Optional[Callable] = None
        self.callback_guardar_producto: Optional[Callable] = None
        self.callback_eliminar_producto: Optional[Callable] = None
        self.callback_seleccion_producto: Optional[Callable] = None
        self.callback_guardar_pendiente: Optional[Callable] = None
        self.callback_eliminar_cliente: Optional[Callable] = None
        self.callback_agregar_cliente: Optional[Callable] = None
        self.callback_verificar_password: Optional[Callable] = None
        
        # Crear interfaz
        self._crear_interfaz()
    
    def _crear_interfaz(self) -> None:
        """Crea todos los componentes de la vista."""
        # Orden importante: crear primero los paneles de fondo
        self._crear_panel_modos()
        self._crear_panel_password()
        self._crear_panel_teclado()
        
        # Luego los controles que deben estar al frente
        self._crear_entrada()
        self._crear_boton_volver()
        self._crear_info()
        self._crear_listado()  # El listado debe crearse al final para estar al frente
    
    def _crear_panel_teclado(self) -> None:
        """Crea el panel del teclado virtual."""
        self.panel_teclado = BasePanel(
            self,
            WindowConfig.MIN_WIDTH,
            290,
            ColorScheme.PRIMARY_BG
        )
        self.panel_teclado.colocar(0, 445)
        
        # Crear teclado
        self.teclado = TecladoVirtual(
            self.panel_teclado,
            WindowConfig.MIN_WIDTH,
            290,
            ColorScheme.PRIMARY_BG
        )
        self.teclado.colocar(0, 0)
        
        # Vincular callback
        self.teclado.vincular_callback(self._procesar_tecla)
        
        # Panel para ocultar teclado (no usado actualmente)
        self.panel_ocultar = BasePanel(
            self,
            750,
            290,
            ColorScheme.PRIMARY_BG
        )
        self.panel_ocultar.colocar(0, 445)
        self.panel_ocultar.enviar_al_fondo()
    
    def _crear_entrada(self) -> None:
        """Crea el campo de entrada de texto."""
        self.entrada = MarcoConImagen(
            self,
            '',
            'textbox',
            20,
            ColorScheme.PRIMARY_BG
        )
        self.entrada.colocar(40, 370)
    
    def _crear_boton_volver(self) -> None:
        """Crea el botón volver."""
        self.boton_volver = MarcoConImagen(
            self,
            'Volver',
            'tecla_envio',
            24,
            ColorScheme.PRIMARY_BG
        )
        self.boton_volver.invertir_colores()
        self.boton_volver.colocar(771, 370)
        self.boton_volver.bind("<Button-1>", self._on_volver_press)
        self.boton_volver.bind("<ButtonRelease-1>", self._on_volver_release)
    
    def _crear_info(self) -> None:
        """Crea la etiqueta informativa."""
        self.info = EtiquetaInfo(
            self,
            '',
            12,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            54
        )
        self.info.colocar(40, 45)
    
    def _crear_listado(self) -> None:
        """Crea el listado de selección."""
        self.panel_listado = BasePanel(
            self,
            380,
            310,
            'black'
        )
        self.panel_listado.colocar(WindowConfig.MIN_WIDTH - 430, 45)
        
        self.listado = ListaConScroll(self.panel_listado)
        self.listado.expandir()
        
        # Vincular eventos
        self.listado.vincular_evento_seleccion(self._on_seleccion_lista)
        self.listado.listbox.bind("<Key>", self._on_tecla_lista)
        
        # IMPORTANTE: Traer el panel al frente para que sea visible
        self.panel_listado.traer_al_frente()
        self.panel_listado.lift()  # Forzar que esté al frente
    
    def _crear_panel_modos(self) -> None:
        """Crea el panel contenedor de todos los modos."""
        self.panel_modos = BasePanel(
            self,
            WindowConfig.MIN_WIDTH,
            365,
            ColorScheme.PRIMARY_BG
        )
        self.panel_modos.colocar(0, 0)
        
        # Crear paneles de cada modo
        self._crear_modo_producto()
        self._crear_modo_pendiente()
        self._crear_modo_camarero()
    
    # ========================================================================
    # MODO PRODUCTO
    # ========================================================================
    
    def _crear_modo_producto(self) -> None:
        """Crea el panel del modo Producto."""
        self.panel_producto = BasePanel(
            self.panel_modos,
            WindowConfig.MIN_WIDTH - 430,
            225,
            ColorScheme.PRIMARY_BG
        )
        self.panel_producto.colocar(0, 130)
        
        x = 40
        y = 25
        dis = 180
        
        # Botones de acción
        boton_guardar = MarcoConImagen(
            self.panel_producto,
            'Guardar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_guardar.colocar(x, y)
        boton_guardar.accion = 'guardar'
        boton_guardar.bind("<Button-1>", self._on_click_producto)
        boton_guardar.bind("<ButtonRelease-1>", self._on_release_producto)
        
        boton_eliminar = MarcoConImagen(
            self.panel_producto,
            'Eliminar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_eliminar.colocar(x + dis, y)
        boton_eliminar.accion = 'eliminar'
        boton_eliminar.bind("<Button-1>", self._on_click_producto)
        boton_eliminar.bind("<ButtonRelease-1>", self._on_release_producto)
        
        boton_limpiar = MarcoConImagen(
            self.panel_producto,
            'Limpiar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_limpiar.colocar(x + dis * 2, y)
        boton_limpiar.accion = 'limpiar'
        boton_limpiar.bind("<Button-1>", self._on_click_producto)
        boton_limpiar.bind("<ButtonRelease-1>", self._on_release_producto)
        
        # Etiquetas
        y = 105
        x = 43
        
        EtiquetaInfo(
            self.panel_producto,
            'Familia',
            12,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            16
        ).colocar(x, y)
        
        EtiquetaInfo(
            self.panel_producto,
            'Nombre',
            12,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            16
        ).colocar(x + dis, y)
        
        EtiquetaInfo(
            self.panel_producto,
            'Precio',
            12,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            16
        ).colocar(x + dis * 2, y)
        
        # Marcos de información
        y = 125
        x = 40
        
        self.producto_familia = MarcoConImagen(
            self.panel_producto,
            '',
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.producto_familia.colocar(x, y)
        self.producto_familia.datos = ''
        self.producto_familia.accion = 'familia'
        self.producto_familia.bind("<Button-1>", self._on_click_producto)
        self.producto_familia.bind("<ButtonRelease-1>", self._on_release_producto)
        
        self.producto_nombre = MarcoConImagen(
            self.panel_producto,
            '',
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.producto_nombre.colocar(x + dis, y)
        self.producto_nombre.datos = ''
        self.producto_nombre.accion = 'nombre'
        self.producto_nombre.invertir_colores()  # Activo por defecto
        self.producto_nombre.bind("<Button-1>", self._on_click_producto)
        self.producto_nombre.bind("<ButtonRelease-1>", self._on_release_producto)
        
        self.producto_precio = MarcoConImagen(
            self.panel_producto,
            '',
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.producto_precio.colocar(x + dis * 2, y)
        self.producto_precio.datos = ''
        self.producto_precio.accion = 'precio'
        self.producto_precio.bind("<Button-1>", self._on_click_producto)
        self.producto_precio.bind("<ButtonRelease-1>", self._on_release_producto)
    
    def _on_click_producto(self, event) -> None:
        """Maneja los clics en los controles del modo Producto."""
        event.widget.invertir_colores()
    
    def _on_release_producto(self, event) -> None:
        """Maneja la liberación de clics en modo Producto."""
        accion = event.widget.accion
        
        if accion == 'familia':
            # Cambiar familia
            texto = event.widget.texto
            if texto == 'Bebida':
                nuevo = 'Comida'
            elif texto == 'Comida':
                nuevo = 'Otros'
            else:
                nuevo = 'Bebida'
            
            event.widget.cambiar_texto(nuevo)
            event.widget.datos = nuevo
            
            # Recargar lista inmediatamente
            self._cargar_productos_por_familia(nuevo)
            
            # Limpiar campos de producto al cambiar familia
            self.producto_nombre.cambiar_texto('')
            self.producto_nombre.datos = ''
            self.producto_precio.cambiar_texto('')
            self.producto_precio.datos = ''
            self.entrada.cambiar_texto('')
            self.gestor_entrada.limpiar()
            
            # No tocar la inversión de colores de familia
            # Solo asegurar que nombre está activo por defecto
            if not self.producto_nombre.invertido:
                self.producto_nombre.invertir_colores()
            if self.producto_precio.invertido:
                self.producto_precio.invertir_colores()
            
            self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
            self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_PRODUCTOS)
        
        elif accion == 'nombre':
            # Activar nombre y desactivar precio
            if not self.producto_nombre.invertido:
                self.producto_nombre.invertir_colores()
            if self.producto_precio.invertido:
                self.producto_precio.invertir_colores()
            
            # Establecer modo texto
            self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
            self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_PRODUCTOS)
            
            # Cargar el contenido en la entrada
            self._actualizar_entrada_producto()
        
        elif accion == 'precio':
            # Activar precio y desactivar nombre
            if self.producto_nombre.invertido:
                self.producto_nombre.invertir_colores()
            if not self.producto_precio.invertido:
                self.producto_precio.invertir_colores()
            
            # Establecer modo numérico
            self.modo_escritura = ModeConfig.ESCRITURA_MONEDAS
            self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_MONEDAS)
            
            # Cargar el contenido en la entrada
            self._actualizar_entrada_producto()
        
        elif accion == 'guardar':
            self._guardar_producto()
            event.widget.invertir_colores()
        
        elif accion == 'eliminar':
            self._eliminar_producto()
            event.widget.invertir_colores()
        
        elif accion == 'limpiar':
            self._limpiar_producto()
            event.widget.invertir_colores()
    
    def _actualizar_entrada_producto(self) -> None:
        """Actualiza la entrada según el campo activo."""
        if self.producto_nombre.invertido:
            texto = self.producto_nombre.datos
            lineas = texto.split('\n')
            self.entrada.cambiar_texto(' '.join(lineas))
        else:
            self.entrada.cambiar_texto(self.producto_precio.datos)
    
    def _cargar_productos_por_familia(self, familia: str) -> None:
        """Carga productos de una familia en el listado."""
        if self.callback_seleccion_producto:
            productos = self.callback_seleccion_producto(familia)
            self.listado.limpiar()
            
            if productos:
                for producto in productos:
                    self.listado.agregar_item(
                        f"{producto.nombre} - {producto.precio:.2f}€"
                    )
                self.info.actualizar_texto(
                    convertir_texto_multilnea(
                        f'{len(productos)} productos en {familia}', 54
                    )
                )
            else:
                self.info.actualizar_texto(
                    convertir_texto_multilnea(
                        f'No hay productos en {familia}', 54
                    )
                )
    
    def _guardar_producto(self) -> None:
        """Guarda el producto actual."""
        if not self.producto_familia.datos:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe seleccionar una familia', 54)
            )
            return
        
        if not self.producto_nombre.datos:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe ingresar un nombre', 54)
            )
            return
        
        if not self.producto_precio.datos:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe ingresar un precio', 54)
            )
            return
        
        if self.callback_guardar_producto:
            exito = self.callback_guardar_producto(
                self.producto_nombre.datos,
                float(self.producto_precio.datos),
                self.producto_familia.datos
            )
            
            if exito:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Producto guardado correctamente', 54)
                )
                
                # Actualizar lista inmediatamente
                self._cargar_productos_por_familia(self.producto_familia.datos)
                
                self._limpiar_producto()
            else:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Error al guardar producto', 54)
                )
    
    def _eliminar_producto(self) -> None:
        """Elimina el producto actual."""
        if not self.producto_nombre.datos:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe seleccionar un producto', 54)
            )
            return
        
        # Guardar familia antes de eliminar
        familia_actual = self.producto_familia.datos
        
        if self.callback_eliminar_producto:
            exito = self.callback_eliminar_producto(self.producto_nombre.datos)
            
            if exito:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Producto eliminado correctamente', 54)
                )
                
                # Actualizar lista inmediatamente
                if familia_actual:
                    self._cargar_productos_por_familia(familia_actual)
                
                self._limpiar_producto()
            else:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Error al eliminar producto', 54)
                )
    
    def _limpiar_producto(self) -> None:
        """Limpia los campos del producto."""
        # Guardar familia actual antes de limpiar
        familia_actual = self.producto_familia.datos
        
        # No limpiar la familia, solo los otros campos
        self.producto_nombre.cambiar_texto('')
        self.producto_nombre.datos = ''
        
        self.producto_precio.cambiar_texto('')
        self.producto_precio.datos = ''
        
        self.entrada.cambiar_texto('')
        self.gestor_entrada.limpiar()
        
        # Asegurar que nombre está activo y precio no
        if not self.producto_nombre.invertido:
            self.producto_nombre.invertir_colores()
        if self.producto_precio.invertido:
            self.producto_precio.invertir_colores()
        
        # Establecer modo de escritura para texto (nombres de productos)
        self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
        self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_PRODUCTOS)
        
        # Recargar listado de la familia actual
        if familia_actual:
            self._cargar_productos_por_familia(familia_actual)
    
    # ========================================================================
    # MODO PENDIENTE
    # ========================================================================
    
    def _crear_modo_pendiente(self) -> None:
        """Crea el panel del modo Pendiente."""
        self.panel_pendiente = BasePanel(
            self.panel_modos,
            WindowConfig.MIN_WIDTH - 430,
            225,
            ColorScheme.PRIMARY_BG
        )
        self.panel_pendiente.colocar(0, 130)
        
        x = 40
        y = 25
        dis = 180
        
        # Botones de acción
        self.pendiente_boton_principal = MarcoConImagen(
            self.panel_pendiente,
            'Guardar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        self.pendiente_boton_principal.colocar(x, y)
        self.pendiente_boton_principal.accion = 'guardar'
        self.pendiente_boton_principal.bind("<Button-1>", self._on_click_pendiente)
        self.pendiente_boton_principal.bind("<ButtonRelease-1>", self._on_release_pendiente)
        
        boton_eliminar = MarcoConImagen(
            self.panel_pendiente,
            'Eliminar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_eliminar.colocar(x + dis, y)
        boton_eliminar.accion = 'eliminar'
        boton_eliminar.bind("<Button-1>", self._on_click_pendiente)
        boton_eliminar.bind("<ButtonRelease-1>", self._on_release_pendiente)
        
        boton_agregar = MarcoConImagen(
            self.panel_pendiente,
            'Agregar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_agregar.colocar(x + dis * 2, y)
        boton_agregar.accion = 'agregar'
        boton_agregar.bind("<Button-1>", self._on_click_pendiente)
        boton_agregar.bind("<ButtonRelease-1>", self._on_release_pendiente)
        
        # Filtros
        y = 125
        
        self.pendiente_todos = MarcoConImagen(
            self.panel_pendiente,
            convertir_texto_multilnea('TODOS LOS CLIENTES'.upper()),
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.pendiente_todos.colocar(x, y)
        self.pendiente_todos.invertir_colores()
        self.pendiente_todos.accion = 'todos'
        self.pendiente_todos.bind("<Button-1>", self._on_click_pendiente)
        self.pendiente_todos.bind("<ButtonRelease-1>", self._on_release_pendiente)
        
        self.pendiente_pendientes = MarcoConImagen(
            self.panel_pendiente,
            convertir_texto_multilnea('CLIENTES CON TICKETS PENDIENTES'.upper()),
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.pendiente_pendientes.colocar(x + dis, y)
        self.pendiente_pendientes.accion = 'pendientes'
        self.pendiente_pendientes.bind("<Button-1>", self._on_click_pendiente)
        self.pendiente_pendientes.bind("<ButtonRelease-1>", self._on_release_pendiente)
        
        self.pendiente_pagados = MarcoConImagen(
            self.panel_pendiente,
            convertir_texto_multilnea('CLIENTES SIN DEUDAS ASOCIADAS'.upper()),
            'tecla_marco',
            12,
            ColorScheme.PRIMARY_BG
        )
        self.pendiente_pagados.colocar(x + dis * 2, y)
        self.pendiente_pagados.accion = 'pagados'
        self.pendiente_pagados.bind("<Button-1>", self._on_click_pendiente)
        self.pendiente_pagados.bind("<ButtonRelease-1>", self._on_release_pendiente)
    
    def _on_click_pendiente(self, event) -> None:
        """Maneja los clics en modo Pendiente."""
        event.widget.invertir_colores()
    
    def _on_release_pendiente(self, event) -> None:
        """Maneja la liberación de clics en modo Pendiente."""
        accion = event.widget.accion
        
        if accion in ['todos', 'pendientes', 'pagados']:
            # Reiniciar filtros
            if not self.pendiente_todos.invertido:
                self.pendiente_todos.invertir_colores()
            if not self.pendiente_pendientes.invertido:
                self.pendiente_pendientes.invertir_colores()
            if not self.pendiente_pagados.invertido:
                self.pendiente_pagados.invertir_colores()
            
            # Activar filtro seleccionado
            event.widget.invertir_colores()
            
            # Cargar clientes según filtro
            self._cargar_clientes_filtrado(accion)
        
        elif accion == 'guardar':
            self._guardar_pendiente()
            event.widget.invertir_colores()
        
        elif accion == 'eliminar':
            self._eliminar_cliente()
            event.widget.invertir_colores()
        
        elif accion == 'agregar':
            self._agregar_cliente()
            event.widget.invertir_colores()
    
    def _cargar_clientes_filtrado(self, filtro: str) -> None:
        """Carga clientes según el filtro."""
        # Este método debe ser implementado con los callbacks apropiados
        pass
    
    def _guardar_pendiente(self) -> None:
        """Guarda el ticket como pendiente."""
        nombre_cliente = self.entrada.cget('text').strip()
        
        if not nombre_cliente:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe ingresar un nombre de cliente', 54)
            )
            return
        
        if self.callback_guardar_pendiente:
            exito = self.callback_guardar_pendiente(nombre_cliente)
            
            if exito:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Ticket guardado como pendiente', 54)
                )
                self.entrada.cambiar_texto('')
                self.gestor_entrada.limpiar()
            else:
                self.info.actualizar_texto(
                    convertir_texto_multilnea('Error al guardar ticket', 54)
                )
    
    def _eliminar_cliente(self) -> None:
        """Elimina un cliente."""
        nombre_cliente = self.entrada.cget('text').strip()
        
        if not nombre_cliente:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe seleccionar un cliente', 54)
            )
            return
        
        if self.callback_eliminar_cliente:
            exito, mensaje = self.callback_eliminar_cliente(nombre_cliente)
            self.info.actualizar_texto(convertir_texto_multilnea(mensaje, 54))
            
            if exito:
                self.entrada.cambiar_texto('')
                self.gestor_entrada.limpiar()
    
    def _agregar_cliente(self) -> None:
        """Agrega un nuevo cliente."""
        nombre_cliente = self.entrada.cget('text').strip()
        
        if not nombre_cliente:
            self.info.actualizar_texto(
                convertir_texto_multilnea('Debe ingresar un nombre', 54)
            )
            return
        
        if self.callback_agregar_cliente:
            exito, mensaje = self.callback_agregar_cliente(nombre_cliente)
            self.info.actualizar_texto(convertir_texto_multilnea(mensaje, 54))
            
            if exito:
                self.entrada.cambiar_texto('')
                self.gestor_entrada.limpiar()
    
    # ========================================================================
    # MODO CAMARERO
    # ========================================================================
    
    def _crear_modo_camarero(self) -> None:
        """Crea el panel del modo Camarero."""
        self.panel_camarero = BasePanel(
            self.panel_modos,
            WindowConfig.MIN_WIDTH - 430,
            225,
            ColorScheme.PRIMARY_BG
        )
        self.panel_camarero.colocar(0, 130)
        
        x = 40
        y = 25
        dis = 180
        
        # Botones
        boton_tickets = MarcoConImagen(
            self.panel_camarero,
            'Tickets',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_tickets.colocar(x, y)
        boton_tickets.accion = 'tickets'
        boton_tickets.bind("<Button-1>", self._on_click_camarero)
        boton_tickets.bind("<ButtonRelease-1>", self._on_release_camarero)
        
        boton_eliminar = MarcoConImagen(
            self.panel_camarero,
            'Eliminar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_eliminar.colocar(x + dis, y)
        boton_eliminar.accion = 'eliminar'
        boton_eliminar.bind("<Button-1>", self._on_click_camarero)
        boton_eliminar.bind("<ButtonRelease-1>", self._on_release_camarero)
        
        boton_agregar = MarcoConImagen(
            self.panel_camarero,
            'Agregar',
            'tecla_marco',
            20,
            ColorScheme.PRIMARY_BG
        )
        boton_agregar.colocar(x + dis * 2, y)
        boton_agregar.accion = 'agregar'
        boton_agregar.bind("<Button-1>", self._on_click_camarero)
        boton_agregar.bind("<ButtonRelease-1>", self._on_release_camarero)
    
    def _on_click_camarero(self, event) -> None:
        """Maneja los clics en modo Camarero."""
        event.widget.invertir_colores()
    
    def _on_release_camarero(self, event) -> None:
        """Maneja la liberación de clics en modo Camarero."""
        accion = event.widget.accion
        
        if accion == 'tickets':
            # Ver tickets del camarero
            pass
        elif accion == 'eliminar':
            # Eliminar camarero
            pass
        elif accion == 'agregar':
            # Agregar camarero
            pass
        
        event.widget.invertir_colores()
    
    # ========================================================================
    # MODO PASSWORD
    # ========================================================================
    
    def _crear_panel_password(self) -> None:
        """Crea el panel del modo Password."""
        self.panel_password = BasePanel(
            self,
            WindowConfig.MIN_WIDTH,
            365,
            ColorScheme.PRIMARY_BG
        )
        self.panel_password.colocar(0, 0)
        
        x = 45
        y = 75
        
        # Mensaje
        self.password_mensaje = EtiquetaInfo(
            self.panel_password,
            '',
            16,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            77
        )
        self.password_mensaje.colocar(x, y)
        
        # Label
        y += 75
        self.password_label = EtiquetaInfo(
            self.panel_password,
            'Ingresa Password',
            16,
            ColorScheme.TEXT_NORMAL,
            ColorScheme.PRIMARY_BG,
            18
        )
        self.password_label.colocar(x, y)
        
        # Campo password
        y += 30
        self.password_campo = MarcoConImagen(
            self.panel_password,
            '',
            'tecla_space',
            24,
            ColorScheme.PRIMARY_BG
        )
        self.password_campo.invertir_colores()
        self.password_campo.colocar(x, y)
        self.password_campo.valor_real = ''  # Valor real del password
        
        # Botón enviar
        boton_enviar = MarcoConImagen(
            self.panel_password,
            'Aceptar',
            'tecla_envio',
            24,
            ColorScheme.PRIMARY_BG
        )
        boton_enviar.invertir_colores()
        boton_enviar.colocar(x + 465, y)
        boton_enviar.accion = 'enviar'
        boton_enviar.bind("<Button-1>", self._on_click_password)
        boton_enviar.bind("<ButtonRelease-1>", self._on_release_password)
        
        # Botón administrar
        self.password_boton_admin = MarcoConImagen(
            self.panel_password,
            'Administrar\nContraseña',
            'tecla_envio',
            18,
            ColorScheme.PRIMARY_BG
        )
        self.password_boton_admin.invertir_colores()
        self.password_boton_admin.colocar(x + 725, y)
        self.password_boton_admin.accion = 'admin'
        self.password_boton_admin.bind("<Button-1>", self._on_click_password)
        self.password_boton_admin.bind("<ButtonRelease-1>", self._on_release_password)
        
        # Ocultar por defecto
        self.panel_password.enviar_al_fondo()
    
    def _on_click_password(self, event) -> None:
        """Maneja los clics en modo Password."""
        event.widget.invertir_colores()
    
    def _on_release_password(self, event) -> None:
        """Maneja la liberación de clics en modo Password."""
        accion = event.widget.accion
        
        if accion == 'enviar':
            if self.callback_verificar_password:
                password = self.password_campo.valor_real
                resultado = self.callback_verificar_password(password)
                
                if resultado['valido']:
                    self.password_mensaje.actualizar_texto(resultado['mensaje'])
                    # Volver al panel principal
                    if self.callback_volver:
                        self.callback_volver()
                else:
                    self.password_mensaje.actualizar_texto(resultado['mensaje'])
                    self._limpiar_password()
        
        elif accion == 'admin':
            # Administrar contraseña
            pass
        
        event.widget.invertir_colores()
    
    def _limpiar_password(self) -> None:
        """Limpia el campo de password."""
        self.password_campo.cambiar_texto('')
        self.password_campo.valor_real = ''
    
    # ========================================================================
    # PROCESAMIENTO DE TECLADO
    # ========================================================================
    
    def _procesar_tecla(self, tecla: str) -> None:
        """
        Procesa una tecla presionada en el teclado virtual.
        
        Args:
            tecla: Tecla presionada
        """
        if self.modo_escritura == ModeConfig.ESCRITURA_PASSWORD:
            self._procesar_password(tecla)
        elif self.modo_escritura == ModeConfig.ESCRITURA_MONEDAS:
            self._procesar_moneda(tecla)
        else:
            self._procesar_texto(tecla)
    
    def _procesar_password(self, tecla: str) -> None:
        """Procesa entrada de password."""
        if tecla == 'Space':
            return
        
        if tecla == 'Shift':
            self.teclado.cambiar_mayusculas()
        elif tecla == 'Delete':
            if self.password_campo.valor_real:
                self.password_campo.valor_real = self.password_campo.valor_real[:-1]
                texto_oculto = self.password_campo.texto
                if texto_oculto:
                    self.password_campo.cambiar_texto(texto_oculto[:-1])
        else:
            if len(self.password_campo.valor_real) < 22:
                self.password_campo.valor_real += tecla
                self.password_campo.cambiar_texto(self.password_campo.texto + '*')
    
    def _procesar_moneda(self, tecla: str) -> None:
        """Procesa entrada de moneda (solo números)."""
        # CRÍTICO: Solo procesar números y Delete
        if not (tecla.isdigit() or tecla == 'Delete'):
            # Ignorar silenciosamente cualquier otra tecla (letras, símbolos, etc)
            return
        
        texto_actual = self.entrada.texto
        
        # Si hay texto no numérico (por error), limpiarlo
        if texto_actual and not texto_actual.replace('.', '').replace(',', '').isdigit():
            texto_actual = ''
        
        try:
            nuevo_texto = formatear_numero_moneda(tecla, texto_actual)
        except ValueError:
            # Si hay algún error, limpiar y empezar de nuevo
            nuevo_texto = ''
        
        self.entrada.cambiar_texto(nuevo_texto)
        
        # Actualizar datos del producto
        if self.modo_actual == ModeConfig.MODO_PRODUCTO:
            self.producto_precio.datos = nuevo_texto
            self.producto_precio.cambiar_texto(nuevo_texto)
    
    def _procesar_texto(self, tecla: str) -> None:
        """Procesa entrada de texto normal."""
        if tecla == 'Shift':
            self.teclado.cambiar_mayusculas()
            self.gestor_entrada.mayusculas = self.teclado.obtener_estado_mayusculas()
            return
        
        # Validar que la tecla es válida (letra, número, espacio, guion, punto, etc)
        if not (tecla.isalnum() or tecla in [' ', '-', '.', 'Ñ', 'Ü', 'Ç'] or tecla == 'Space' or tecla == 'Delete'):
            return  # Ignorar teclas no válidas
        
        # Configurar modo de escritura en el gestor
        self.gestor_entrada.establecer_modo(self.modo_escritura)
        
        # Aplicar lógica según modo
        if self.modo_escritura == ModeConfig.ESCRITURA_NOMBRES:
            self._aplicar_modo_nombres(tecla)
        elif self.modo_escritura == ModeConfig.ESCRITURA_PRODUCTOS:
            self._aplicar_modo_productos(tecla)
        
        # Procesar tecla
        texto = self.gestor_entrada.procesar_tecla(tecla)
        
        # Actualizar entrada
        self.entrada.cambiar_texto(texto)
        
        # Actualizar datos según modo
        self._actualizar_datos_modo()
    
    def _aplicar_modo_nombres(self, tecla: str) -> None:
        """Aplica lógica de nombres propios."""
        if tecla.isalpha() or tecla == ' ':
            texto_actual = self.gestor_entrada.obtener_texto()
            
            if len(texto_actual) == 0:
                if not self.gestor_entrada.mayusculas:
                    self.teclado.cambiar_mayusculas()
                    self.gestor_entrada.mayusculas = True
            else:
                if texto_actual[-1] == ' ':
                    if not self.gestor_entrada.mayusculas:
                        self.teclado.cambiar_mayusculas()
                        self.gestor_entrada.mayusculas = True
                else:
                    if self.gestor_entrada.mayusculas:
                        self.teclado.cambiar_mayusculas()
                        self.gestor_entrada.mayusculas = False
    
    def _aplicar_modo_productos(self, tecla: str) -> None:
        """Aplica lógica de productos (solo primera mayúscula)."""
        if tecla.isalpha() or tecla == ' ':
            texto_actual = self.gestor_entrada.obtener_texto()
            
            if len(texto_actual) == 0:
                if not self.gestor_entrada.mayusculas:
                    self.teclado.cambiar_mayusculas()
                    self.gestor_entrada.mayusculas = True
            else:
                if self.gestor_entrada.mayusculas:
                    self.teclado.cambiar_mayusculas()
                    self.gestor_entrada.mayusculas = False
    
    def _actualizar_datos_modo(self) -> None:
        """Actualiza los datos según el modo actual."""
        texto = self.gestor_entrada.obtener_texto()
        
        if self.modo_actual == ModeConfig.MODO_PRODUCTO:
            texto_formato = convertir_texto_multilnea(texto)
            
            if self.producto_nombre.invertido:
                self.producto_nombre.cambiar_texto(texto_formato)
                self.producto_nombre.datos = texto
            elif self.producto_precio.invertido:
                self.producto_precio.cambiar_texto(texto)
                self.producto_precio.datos = texto
    
    # ========================================================================
    # EVENTOS GENERALES
    # ========================================================================
    
    def _on_volver_press(self, event) -> None:
        """Maneja el clic en volver."""
        event.widget.invertir_colores()
    
    def _on_volver_release(self, event) -> None:
        """Maneja la liberación del botón volver."""
        event.widget.invertir_colores()
        
        self.info.actualizar_texto('')
        
        if self.callback_volver:
            self.callback_volver()
    
    def _on_seleccion_lista(self, event) -> None:
        """Maneja la selección de un elemento del listado."""
        seleccion = self.listado.obtener_seleccion()
        
        if seleccion:
            if self.modo_actual == ModeConfig.MODO_PRODUCTO:
                # Extraer nombre y precio
                if ' - ' in seleccion:
                    nombre, precio_str = seleccion.split(' - ')
                    precio = precio_str.replace('€', '').strip()
                    
                    # Actualizar campos
                    texto_formato = convertir_texto_multilnea(nombre)
                    self.producto_nombre.cambiar_texto(texto_formato)
                    self.producto_nombre.datos = nombre
                    
                    self.producto_precio.cambiar_texto(precio)
                    self.producto_precio.datos = precio
                    
                    # Actualizar entrada según campo activo
                    if self.producto_nombre.invertido:
                        self.entrada.cambiar_texto(nombre)
                        self.gestor_entrada.establecer_texto(nombre)
                        self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
                        self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_PRODUCTOS)
                    else:
                        self.entrada.cambiar_texto(precio)
                        self.gestor_entrada.establecer_texto(precio)
                        self.modo_escritura = ModeConfig.ESCRITURA_MONEDAS
                        self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_MONEDAS)
            
            elif self.modo_actual == ModeConfig.MODO_PENDIENTE:
                # Extraer nombre del cliente
                if ' - ' in seleccion:
                    nombre = seleccion.split(' - ')[0]
                else:
                    nombre = seleccion
                
                self.entrada.cambiar_texto(nombre)
                self.gestor_entrada.establecer_texto(nombre)
                self.modo_escritura = ModeConfig.ESCRITURA_NOMBRES
                self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_NOMBRES)
            
            elif self.modo_actual == ModeConfig.MODO_CAMARERO:
                self.entrada.cambiar_texto(seleccion)
                self.gestor_entrada.establecer_texto(seleccion)
                self.modo_escritura = ModeConfig.ESCRITURA_NOMBRES
                self.gestor_entrada.establecer_modo(ModeConfig.ESCRITURA_NOMBRES)
    
    def _on_tecla_lista(self, event) -> None:
        """Maneja las teclas en el listado."""
        # Deshabilitar la autoselección con espacio
        if event.keysym == 'space':
            return "break"
    
    # ========================================================================
    # MÉTODOS PÚBLICOS
    # ========================================================================
    
    def cambiar_modo(self, modo: str) -> None:
        """
        Cambia el modo de operación del teclado.
        
        Args:
            modo: Modo a activar (Producto, Pendiente, Camarero, Password)
        """
        self.modo_actual = modo
        
        # Ocultar todos los paneles
        self.panel_producto.enviar_al_fondo()
        self.panel_pendiente.enviar_al_fondo()
        self.panel_camarero.enviar_al_fondo()
        self.panel_password.enviar_al_fondo()
        
        # Limpiar entrada e info
        self.entrada.cambiar_texto('')
        self.gestor_entrada.limpiar()
        self.info.actualizar_texto('')
        
        # Mostrar panel correspondiente
        if modo == ModeConfig.MODO_PRODUCTO:
            self.panel_producto.traer_al_frente()
            self.panel_modos.traer_al_frente()
            self.modo_escritura = ModeConfig.ESCRITURA_PRODUCTOS
            
            # Inicializar familia por defecto si está vacía
            if not self.producto_familia.datos:
                self.producto_familia.cambiar_texto('Bebida')
                self.producto_familia.datos = 'Bebida'
            
            # Asegurar que nombre está activo
            if not self.producto_nombre.invertido:
                self.producto_nombre.invertir_colores()
            if self.producto_precio.invertido:
                self.producto_precio.invertir_colores()
            
        elif modo == ModeConfig.MODO_PENDIENTE:
            self.panel_pendiente.traer_al_frente()
            self.panel_modos.traer_al_frente()
            self.modo_escritura = ModeConfig.ESCRITURA_NOMBRES
            
            # Activar filtro "todos" por defecto
            if not self.pendiente_todos.invertido:
                self.pendiente_todos.invertir_colores()
            
        elif modo == ModeConfig.MODO_CAMARERO:
            self.panel_camarero.traer_al_frente()
            self.panel_modos.traer_al_frente()
            self.modo_escritura = ModeConfig.ESCRITURA_NOMBRES
            
        elif modo == 'Password':
            self.panel_password.traer_al_frente()
            self.modo_escritura = ModeConfig.ESCRITURA_PASSWORD
            self._limpiar_password()
            self.password_mensaje.actualizar_texto('Introduzca contraseña para acceder')
        
        # IMPORTANTE: Siempre traer el listado al frente para que sea visible
        if self.panel_listado:
            self.panel_listado.traer_al_frente()
            self.panel_listado.lift()
        
        # También traer al frente la entrada, info y botón volver
        self.entrada.lift()
        self.boton_volver.lift()
        self.info.lift()
    
    def establecer_texto_boton_volver(self, texto: str) -> None:
        """
        Establece el texto del botón volver.
        
        Args:
            texto: Nuevo texto
        """
        self.boton_volver.cambiar_texto(texto)
    
    def cargar_lista(self, items: List[str], colores: Optional[List[str]] = None) -> None:
        """
        Carga elementos en el listado.
        
        Args:
            items: Lista de elementos a mostrar
            colores: Lista de colores para cada item (opcional)
        """
        self.listado.limpiar()
        
        for i, item in enumerate(items):
            color = colores[i] if colores and i < len(colores) else None
            self.listado.agregar_item(item, color)
    
    def actualizar_info(self, mensaje: str) -> None:
        """
        Actualiza el mensaje informativo.
        
        Args:
            mensaje: Mensaje a mostrar
        """
        self.info.actualizar_texto(convertir_texto_multilnea(mensaje, 54))
    
    def limpiar_entrada(self) -> None:
        """Limpia el campo de entrada."""
        self.entrada.cambiar_texto('')
        self.gestor_entrada.limpiar()
    
    # ========================================================================
    # VINCULAR CALLBACKS
    # ========================================================================
    
    def vincular_callback_volver(self, callback: Callable) -> None:
        """Vincula el callback para el botón volver."""
        self.callback_volver = callback
    
    def vincular_callback_guardar_producto(self, callback: Callable) -> None:
        """Vincula el callback para guardar producto."""
        self.callback_guardar_producto = callback
    
    def vincular_callback_eliminar_producto(self, callback: Callable) -> None:
        """Vincula el callback para eliminar producto."""
        self.callback_eliminar_producto = callback
    
    def vincular_callback_seleccion_producto(self, callback: Callable) -> None:
        """Vincula el callback para seleccionar productos por familia."""
        self.callback_seleccion_producto = callback
    
    def vincular_callback_guardar_pendiente(self, callback: Callable) -> None:
        """Vincula el callback para guardar ticket pendiente."""
        self.callback_guardar_pendiente = callback
    
    def vincular_callback_eliminar_cliente(self, callback: Callable) -> None:
        """Vincula el callback para eliminar cliente."""
        self.callback_eliminar_cliente = callback
    
    def vincular_callback_agregar_cliente(self, callback: Callable) -> None:
        """Vincula el callback para agregar cliente."""
        self.callback_agregar_cliente = callback
    
    def vincular_callback_verificar_password(self, callback: Callable) -> None:
        """Vincula el callback para verificar password."""
        self.callback_verificar_password = callback


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'KeyboardView'
]