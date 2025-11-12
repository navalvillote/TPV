"""
Vista del calendario y reportes.

Este módulo contiene la interfaz completa del calendario para consultar
ventas y generar reportes.
"""

import datetime
from typing import List, Optional, Callable
from tkinter import END
from config.settings import WindowConfig, ColorScheme, CalendarConfig
from views.components.base_widgets import BasePanel, MarcoConImagen, ListaConScroll
from views.components.ticket_display import TicketDisplay, EtiquetaInfo
from controllers.calendar_controller import CalendarController
from controllers.printer_controller import PrinterController
from utils.formatters import convertir_texto_multilnea


class CalendarView(BasePanel):
    """Vista del calendario con consulta de ventas y reportes."""
    
    def __init__(self, parent, calendar_controller: CalendarController,
                 printer_controller: PrinterController):
        """
        Inicializa la vista del calendario.
        
        Args:
            parent: Widget padre
            calendar_controller: Controlador del calendario
            printer_controller: Controlador de impresión
        """
        super().__init__(
            parent,
            WindowConfig.MIN_WIDTH,
            WindowConfig.MIN_HEIGHT,
            ColorScheme.PRIMARY_BG
        )
        
        self.calendar_controller = calendar_controller
        self.printer_controller = printer_controller
        
        # Fecha actual
        self.fecha_actual = datetime.date.today()
        
        # Componentes
        self.panel_calendario: Optional[BasePanel] = None
        self.panel_impresion: Optional[BasePanel] = None
        self.panel_listado: Optional[ListaConScroll] = None
        self.panel_botones_cabeza: Optional[BasePanel] = None
        self.panel_botones_pie: Optional[BasePanel] = None
        
        # Paneles de días/meses/años
        self.panel_dias: Optional[BasePanel] = None
        self.panel_meses: Optional[BasePanel] = None
        self.panel_anios: Optional[BasePanel] = None
        
        # Componentes
        self.fechado: Optional[MarcoConImagen] = None
        self.ticket_display: Optional[TicketDisplay] = None
        self.info_calendario: Optional[EtiquetaInfo] = None
        self.boton_imprimir: Optional[MarcoConImagen] = None
        self.boton_totales: Optional[MarcoConImagen] = None
        self.boton_comodin: Optional[MarcoConImagen] = None
        self.info_iva: Optional[MarcoConImagen] = None
        
        # Listas de marcos
        self.marcos_fecha: List[MarcoConImagen] = []  # [día, mes, año]
        self.marcos_dias: List[MarcoConImagen] = []
        self.marcos_meses: List[MarcoConImagen] = []
        self.marcos_anios: List[MarcoConImagen] = []
        
        # Estado
        self.iva_actual = 21.0
        self.tipo_total_actual = 0  # Índice en CalendarConfig.TOTALES
        self.modo_comodin = 'impresoras'  # impresoras, camarero
        
        # Callbacks
        self.callback_volver: Optional[Callable] = None
        self.callback_obtener_impresoras: Optional[Callable] = None
        
        # Crear interfaz
        self._crear_interfaz()
    
    def _crear_interfaz(self) -> None:
        """Crea todos los componentes de la vista."""
        self._crear_panel_impresion()
        self._crear_panel_calendario_listado()
        self._crear_panel_botones_cabeza()
        self._crear_panel_botones_pie()
    
    def _crear_panel_impresion(self) -> None:
        """Crea el panel de impresión con el ticket."""
        self.panel_impresion = BasePanel(
            self,
            216,
            WindowConfig.MIN_HEIGHT - 10,
            ColorScheme.SECONDARY_BG
        )
        self.panel_impresion.colocar(WindowConfig.MIN_WIDTH - 221, 5)
        
        # Fechado (pantalla de fecha)
        self.fechado = MarcoConImagen(
            self.panel_impresion,
            self.fecha_actual.strftime('%d/%m/%Y'),
            'pantalla',
            26,
            ColorScheme.SECONDARY_BG
        )
        self.fechado.colocar(0, 0)
        
        # Ticket display
        self.ticket_display = TicketDisplay(
            self.panel_impresion,
            30,
            41,
            ColorScheme.SECONDARY_BG
        )
        self.ticket_display.colocar(0, 61)
        
        # Botón imprimir
        self.boton_imprimir = MarcoConImagen(
            self.panel_impresion,
            'Imprimir',
            'tecla_envio',
            20,
            ColorScheme.SECONDARY_BG
        )
        self.boton_imprimir.invertir_colores()
        self.boton_imprimir.colocar(3, WindowConfig.MIN_HEIGHT - 88)
        self.boton_imprimir.bind("<Button-1>", self._on_imprimir_press)
        self.boton_imprimir.bind("<ButtonRelease-1>", self._on_imprimir_release)
    
    def _crear_panel_calendario_listado(self) -> None:
        """Crea el panel que contiene calendario y listado."""
        panel_contenedor = BasePanel(
            self,
            WindowConfig.MIN_WIDTH - 232,
            WindowConfig.MIN_HEIGHT - 164,
            ColorScheme.PRIMARY_BG
        )
        panel_contenedor.colocar(5, 82)
        
        # Calendario
        self._crear_calendario(panel_contenedor)
        
        # Listado
        self._crear_listado(panel_contenedor)
    
    def _crear_calendario(self, parent) -> None:
        """Crea el panel del calendario."""
        self.panel_calendario = BasePanel(parent, 500, 603, ColorScheme.DARK_BG)
        self.panel_calendario.colocar(0, 0)
        
        # Etiqueta informativa
        self.info_calendario = EtiquetaInfo(
            self.panel_calendario,
            '',
            14,
            'gray92',
            'gray32',
            49
        )
        self.info_calendario.colocar(2, 555)
        
        # Controles de fecha (día, mes, año)
        self._crear_controles_fecha()
        
        # Paneles de selección
        self._crear_panel_dias()
        self._crear_panel_meses()
        self._crear_panel_anios()
        
        # Mostrar panel de días por defecto
        self.panel_dias.traer_al_frente()
    
    def _crear_controles_fecha(self) -> None:
        """Crea los controles de día, mes y año."""
        x = 5
        y = 5
        
        # Día
        dia = self.fecha_actual.strftime('%A')
        dia = f'{dia[:3].upper()}, {str(self.fecha_actual.day).zfill(2)}'
        
        marco_dia = MarcoConImagen(
            self.panel_calendario,
            dia,
            'tecla_doble',
            20,
            self.panel_calendario.fondo
        )
        marco_dia.colocar(x, y)
        marco_dia.bind("<Button-1>", self._on_click_dia)
        marco_dia.bind("<ButtonRelease-1>", self._on_release_dia)
        self.marcos_fecha.append(marco_dia)
        
        # Mes
        x += 140
        mes = self.fecha_actual.strftime('%B')
        marco_mes = MarcoConImagen(
            self.panel_calendario,
            mes.upper(),
            'tecla_envio',
            20,
            self.panel_calendario.fondo
        )
        marco_mes.colocar(x, y)
        marco_mes.bind("<Button-1>", self._on_click_mes)
        marco_mes.bind("<ButtonRelease-1>", self._on_release_mes)
        self.marcos_fecha.append(marco_mes)
        
        # Año
        x += 210
        marco_anio = MarcoConImagen(
            self.panel_calendario,
            str(self.fecha_actual.year),
            'tecla_doble',
            20,
            self.panel_calendario.fondo
        )
        marco_anio.colocar(x, y)
        marco_anio.bind("<Button-1>", self._on_click_anio)
        marco_anio.bind("<ButtonRelease-1>", self._on_release_anio)
        self.marcos_fecha.append(marco_anio)
    
    def _crear_panel_dias(self) -> None:
        """Crea el panel de selección de días."""
        self.panel_dias = BasePanel(
            self.panel_calendario,
            500,
            460,
            ColorScheme.DARK_BG
        )
        self.panel_dias.colocar(0, 75)
        
        # Encabezados de días de la semana
        x = 10
        y = 5
        for dia in CalendarConfig.DIAS_SEMANA:
            etiq = EtiquetaInfo(
                self.panel_dias,
                dia,
                12,
                'SlateGray4',
                self.panel_dias.fondo,
                6
            )
            etiq.colocar(x, y)
            x += 70
        
        # Crear días del mes
        self._actualizar_dias()
    
    def _actualizar_dias(self) -> None:
        """Actualiza los botones de días según el mes actual."""
        # Limpiar días existentes
        for marco in self.marcos_dias:
            marco.destroy()
        self.marcos_dias.clear()
        
        # Obtener información del mes
        primer_dia = self.calendar_controller.obtener_primer_dia_semana(
            self.fecha_actual
        )
        num_dias = self.calendar_controller.obtener_dias_mes(self.fecha_actual)
        
        # Crear botones de días
        contador = 0
        for y_idx in range(6):
            posy = y_idx * 70 + 35
            for x_idx in range(7):
                if primer_dia <= contador < num_dias + primer_dia:
                    dia_num = contador - primer_dia + 1
                    posx = x_idx * 70 + 5
                    
                    marco = MarcoConImagen(
                        self.panel_dias,
                        str(dia_num),
                        'tecla',
                        20,
                        self.panel_dias.fondo
                    )
                    marco.colocar(posx, posy)
                    marco.dia = dia_num
                    
                    # Marcar día actual
                    if dia_num == self.fecha_actual.day:
                        marco.invertir_colores()
                    
                    marco.bind("<Button-1>", self._on_click_dia_especifico)
                    self.marcos_dias.append(marco)
                
                contador += 1
    
    def _crear_panel_meses(self) -> None:
        """Crea el panel de selección de meses."""
        self.panel_meses = BasePanel(
            self.panel_calendario,
            500,
            460,
            ColorScheme.DARK_BG
        )
        self.panel_meses.colocar(0, 75)
        
        # Crear botones de meses
        for mes_idx in range(12):
            y = (mes_idx // 2) * 75 + 8
            x = (mes_idx % 2) * 235 + 27
            
            fecha_mes = datetime.date(self.fecha_actual.year, mes_idx + 1, 1)
            nombre_mes = fecha_mes.strftime('%B')
            
            marco = MarcoConImagen(
                self.panel_meses,
                nombre_mes,
                'tecla_envio',
                20,
                self.panel_meses.fondo
            )
            marco.colocar(x, y)
            marco.mes = mes_idx + 1
            
            # Marcar mes actual
            if mes_idx + 1 == self.fecha_actual.month:
                marco.invertir_colores()
            
            marco.bind("<Button-1>", self._on_click_mes_especifico)
            self.marcos_meses.append(marco)
    
    def _crear_panel_anios(self) -> None:
        """Crea el panel de selección de años."""
        self.panel_anios = BasePanel(
            self.panel_calendario,
            500,
            460,
            ColorScheme.DARK_BG
        )
        self.panel_anios.colocar(0, 75)
        
        # Botones de navegación de rango de años
        anio_central = self.fecha_actual.year
        
        # Botón anterior
        marco_prev = MarcoConImagen(
            self.panel_anios,
            f'{anio_central - 22} - {anio_central - 8}',
            'tecla_envio',
            20,
            self.panel_anios.fondo
        )
        marco_prev.invertir_colores()
        marco_prev.colocar(27, 5)
        marco_prev.anio_base = anio_central - 15
        marco_prev.bind("<Button-1>", self._on_click_rango_anios)
        marco_prev.bind("<ButtonRelease-1>", self._on_release_rango_anios)
        self.marcos_anios.append(marco_prev)
        
        # Botón siguiente
        marco_next = MarcoConImagen(
            self.panel_anios,
            f'{anio_central + 8} - {anio_central + 22}',
            'tecla_envio',
            20,
            self.panel_anios.fondo
        )
        marco_next.invertir_colores()
        marco_next.colocar(262, 5)
        marco_next.anio_base = anio_central + 15
        marco_next.bind("<Button-1>", self._on_click_rango_anios)
        marco_next.bind("<ButtonRelease-1>", self._on_release_rango_anios)
        self.marcos_anios.append(marco_next)
        
        # Botones de años individuales
        self._actualizar_anios(anio_central)
    
    def _actualizar_anios(self, anio_central: int) -> None:
        """Actualiza los botones de años."""
        # Eliminar años individuales existentes (mantener los 2 primeros)
        for marco in self.marcos_anios[2:]:
            marco.destroy()
        self.marcos_anios = self.marcos_anios[:2]
        
        # Crear nuevos años
        anio_inicio = anio_central - 7
        
        for idx in range(15):
            y = (idx // 3) * 75 + 83
            x = (idx % 3) * 157 + 22
            
            anio = anio_inicio + idx
            
            marco = MarcoConImagen(
                self.panel_anios,
                str(anio),
                'tecla_doble',
                20,
                self.panel_anios.fondo
            )
            marco.colocar(x, y)
            marco.anio = anio
            
            # Marcar año actual
            if anio == self.fecha_actual.year:
                marco.invertir_colores()
            
            marco.bind("<Button-1>", self._on_click_anio_especifico)
            self.marcos_anios.append(marco)
    
    def _crear_listado(self, parent) -> None:
        """Crea el listado de tickets."""
        self.panel_listado = ListaConScroll(parent)
        self.panel_listado.place(
            x=WindowConfig.MIN_WIDTH - 232 - 287 - 15,
            y=0,
            width=287,
            height=604
        )
        
        # Vincular evento de selección
        self.panel_listado.vincular_evento_seleccion(self._on_seleccion_ticket)
        
        # Cargar tickets del día actual
        self._cargar_tickets_dia()
    
    def _crear_panel_botones_cabeza(self) -> None:
        """Crea el panel de botones superiores."""
        self.panel_botones_cabeza = BasePanel(
            self,
            792,
            75,
            ColorScheme.PRIMARY_BG
        )
        self.panel_botones_cabeza.colocar(5, 5)
        
        x = 0
        y = 2
        
        # Botón IVA -
        boton_iva_menos = MarcoConImagen(
            self.panel_botones_cabeza,
            '-',
            'tecla',
            20,
            self.panel_botones_cabeza.fondo
        )
        boton_iva_menos.colocar(x, y)
        boton_iva_menos.incremento = -0.5
        boton_iva_menos.bind("<Button-1>", self._on_click_iva)
        boton_iva_menos.bind("<ButtonRelease-1>", self._on_release_iva)
        
        # IVA actual
        x += 67
        self.info_iva = MarcoConImagen(
            self.panel_botones_cabeza,
            f'{self.iva_actual}% de IVA',
            'tecla_envio',
            20,
            self.panel_botones_cabeza.fondo
        )
        self.info_iva.invertir_colores()
        self.info_iva.colocar(x, y)
        
        # Botón IVA +
        x += 206
        boton_iva_mas = MarcoConImagen(
            self.panel_botones_cabeza,
            '+',
            'tecla',
            20,
            self.panel_botones_cabeza.fondo
        )
        boton_iva_mas.colocar(x, y)
        boton_iva_mas.incremento = 0.5
        boton_iva_mas.bind("<Button-1>", self._on_click_iva)
        boton_iva_mas.bind("<ButtonRelease-1>", self._on_release_iva)
        
        # Botón comodín
        x += 160
        self.boton_comodin = MarcoConImagen(
            self.panel_botones_cabeza,
            'Asignar\nImpresoras',
            'tecla_envio',
            16,
            self.panel_botones_cabeza.fondo
        )
        self.boton_comodin.colocar(x, y)
        self.boton_comodin.bind("<Button-1>", self._on_click_comodin)
        self.boton_comodin.bind("<ButtonRelease-1>", self._on_release_comodin)
        
        # Botón volver
        x += 210
        boton_volver = MarcoConImagen(
            self.panel_botones_cabeza,
            'Volver',
            'tecla_marco',
            20,
            self.panel_botones_cabeza.fondo
        )
        boton_volver.invertir_colores()
        boton_volver.colocar(x, y)
        boton_volver.bind("<Button-1>", self._on_click_volver)
        boton_volver.bind("<ButtonRelease-1>", self._on_release_volver)
    
    def _crear_panel_botones_pie(self) -> None:
        """Crea el panel de botones inferiores (totales)."""
        self.panel_botones_pie = BasePanel(
            self,
            792,
            75,
            ColorScheme.PRIMARY_BG
        )
        self.panel_botones_pie.colocar(5, 688)
        
        x = 110
        y = 5
        
        # Botón anterior
        boton_prev = MarcoConImagen(
            self.panel_botones_pie,
            '<<',
            'tecla',
            20,
            self.panel_botones_pie.fondo
        )
        boton_prev.colocar(x, y)
        boton_prev.direccion = -1
        boton_prev.bind("<Button-1>", self._on_click_cambiar_total)
        boton_prev.bind("<ButtonRelease-1>", self._on_release_cambiar_total)
        
        # Botón totales (actual)
        x += 67
        nombre_total, _ = CalendarConfig.TOTALES[self.tipo_total_actual]
        self.boton_totales = MarcoConImagen(
            self.panel_botones_pie,
            nombre_total,
            'tecla_space',
            20,
            self.panel_botones_pie.fondo
        )
        self.boton_totales.invertir_colores()
        self.boton_totales.colocar(x, y)
        self.boton_totales.bind("<Button-1>", self._on_click_mostrar_total)
        self.boton_totales.bind("<ButtonRelease-1>", self._on_release_mostrar_total)
        
        # Botón siguiente
        x += 416
        boton_next = MarcoConImagen(
            self.panel_botones_pie,
            '>>',
            'tecla',
            20,
            self.panel_botones_pie.fondo
        )
        boton_next.colocar(x, y)
        boton_next.direccion = 1
        boton_next.bind("<Button-1>", self._on_click_cambiar_total)
        boton_next.bind("<ButtonRelease-1>", self._on_release_cambiar_total)
    
    # ========================================================================
    # EVENTOS DE DÍA
    # ========================================================================
    
    def _on_click_dia(self, event) -> None:
        """Muestra el panel de días."""
        event.widget.invertir_colores()
        self.panel_dias.traer_al_frente()
    
    def _on_release_dia(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_dia_especifico(self, event) -> None:
        """Selecciona un día específico."""
        # Desmarcar días anteriores
        for marco in self.marcos_dias:
            if marco.invertido:
                marco.invertir_colores()
        
        # Marcar día seleccionado
        event.widget.invertir_colores()
        
        # Actualizar fecha
        nueva_fecha = datetime.date(
            self.fecha_actual.year,
            self.fecha_actual.month,
            event.widget.dia
        )
        self._cambiar_fecha(nueva_fecha)
    
    # ========================================================================
    # EVENTOS DE MES
    # ========================================================================
    
    def _on_click_mes(self, event) -> None:
        """Muestra el panel de meses."""
        event.widget.invertir_colores()
        self.panel_meses.traer_al_frente()
    
    def _on_release_mes(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_mes_especifico(self, event) -> None:
        """Selecciona un mes específico."""
        # Desmarcar meses anteriores
        for marco in self.marcos_meses:
            if not marco.invertido:
                marco.invertir_colores()
        
        # Marcar mes seleccionado
        event.widget.invertir_colores()
        
        # Calcular nueva fecha
        num_dias = self.calendar_controller.obtener_dias_mes(
            datetime.date(self.fecha_actual.year, event.widget.mes, 1)
        )
        
        dia = min(self.fecha_actual.day, num_dias)
        
        nueva_fecha = datetime.date(
            self.fecha_actual.year,
            event.widget.mes,
            dia
        )
        
        # Actualizar control de mes
        self.marcos_fecha[1].cambiar_texto(nueva_fecha.strftime('%B').upper())
        
        self._cambiar_fecha(nueva_fecha)
    
    # ========================================================================
    # EVENTOS DE AÑO
    # ========================================================================
    
    def _on_click_anio(self, event) -> None:
        """Muestra el panel de años."""
        event.widget.invertir_colores()
        self.panel_anios.traer_al_frente()
    
    def _on_release_anio(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_rango_anios(self, event) -> None:
        """Cambia el rango de años mostrados."""
        event.widget.invertir_colores()
        self._actualizar_anios(event.widget.anio_base)
        
        # Actualizar botones de navegación
        self.marcos_anios[0].anio_base = event.widget.anio_base - 15
        self.marcos_anios[0].cambiar_texto(
            f'{event.widget.anio_base - 22} - {event.widget.anio_base - 8}'
        )
        
        self.marcos_anios[1].anio_base = event.widget.anio_base + 15
        self.marcos_anios[1].cambiar_texto(
            f'{event.widget.anio_base + 8} - {event.widget.anio_base + 22}'
        )
    
    def _on_release_rango_anios(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_anio_especifico(self, event) -> None:
        """Selecciona un año específico."""
        # Desmarcar años anteriores
        for i, marco in enumerate(self.marcos_anios[2:], 2):
            if marco.invertido:
                marco.invertir_colores()
        
        # Marcar año seleccionado
        event.widget.invertir_colores()
        
        # Actualizar fecha
        nueva_fecha = datetime.date(
            event.widget.anio,
            self.fecha_actual.month,
            self.fecha_actual.day
        )
        
        # Actualizar control de año
        self.marcos_fecha[2].cambiar_texto(str(event.widget.anio))
        
        # Cargar recibos del nuevo año
        self.calendar_controller.receipt_manager = (
            self.calendar_controller.data_manager.cargar_recibos_anuales(
                event.widget.anio
            )
        )
        
        self._cambiar_fecha(nueva_fecha)
    
    # ========================================================================
    # EVENTOS DE TICKETS Y REPORTES
    # ========================================================================
    
    def _on_seleccion_ticket(self, event) -> None:
        """Maneja la selección de un ticket del listado."""
        if self.modo_comodin == 'impresoras':
            # Obtener selección
            ticket_str = self.panel_listado.obtener_seleccion()
            if ticket_str:
                # Extraer fecha del ticket
                fecha_str = ticket_str.split(' - ')[0] if ' - ' in ticket_str else ticket_str
                
                # Buscar y mostrar ticket
                recibos_dia = self.calendar_controller.obtener_recibos_dia(
                    self.fecha_actual
                )
                
                for recibo in recibos_dia:
                    if recibo.fecha.startswith(fecha_str):
                        texto = recibo.generar_texto_ticket(self.iva_actual)
                        self.ticket_display.actualizar_texto(texto)
                        break
    
    def _on_click_mostrar_total(self, event) -> None:
        """Muestra el reporte del total actual."""
        event.widget.invertir_colores()
        
        _, tipo = CalendarConfig.TOTALES[self.tipo_total_actual]
        
        # Generar reporte según tipo
        if tipo == 'día':
            texto = self.calendar_controller.generar_reporte_diario(
                self.fecha_actual,
                self.iva_actual
            )
        elif tipo == 'mes':
            texto = self.calendar_controller.generar_reporte_mensual(
                self.fecha_actual,
                self.iva_actual
            )
        elif tipo == 'día a día':
            texto = self.calendar_controller.generar_reporte_dia_a_dia(
                self.fecha_actual,
                self.iva_actual
            )
        else:  # efectivo o tarjeta
            texto = self.calendar_controller.generar_reporte_por_metodo(
                self.fecha_actual,
                tipo,
                self.iva_actual
            )
        
        self.ticket_display.actualizar_texto(texto)
    
    def _on_release_mostrar_total(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_cambiar_total(self, event) -> None:
        """Cambia el tipo de total mostrado."""
        event.widget.invertir_colores()
        
        # Cambiar índice
        self.tipo_total_actual += event.widget.direccion
        
        # Circular
        if self.tipo_total_actual < 0:
            self.tipo_total_actual = len(CalendarConfig.TOTALES) - 1
        elif self.tipo_total_actual >= len(CalendarConfig.TOTALES):
            self.tipo_total_actual = 0
        
        # Actualizar texto
        nombre, _ = CalendarConfig.TOTALES[self.tipo_total_actual]
        self.boton_totales.cambiar_texto(nombre)
    
    def _on_release_cambiar_total(self, event) -> None:
        event.widget.invertir_colores()
    
    # ========================================================================
    # EVENTOS DE CONTROLES
    # ========================================================================
    
    def _on_click_iva(self, event) -> None:
        """Cambia el IVA."""
        event.widget.invertir_colores()
        
        self.iva_actual += event.widget.incremento
        
        # Validar límites
        if self.iva_actual < 0:
            self.iva_actual = 0
        elif self.iva_actual > 100:
            self.iva_actual = 100
        
        # Actualizar visualización
        self.info_iva.cambiar_texto(f'{self.iva_actual}% de IVA')
    
    def _on_release_iva(self, event) -> None:
        """Maneja la liberación del botón IVA."""
        event.widget.invertir_colores()
    
    def _on_click_comodin(self, event) -> None:
        """Cambia la funcionalidad del botón comodín."""
        event.widget.invertir_colores()
        
        if self.modo_comodin == 'impresoras':
            # Cargar lista de impresoras si hay callback
            if self.callback_obtener_impresoras:
                impresoras = self.callback_obtener_impresoras()
                self.panel_listado.limpiar()
                for impresora in impresoras:
                    self.panel_listado.agregar_item(impresora)
                
                self.info_calendario.actualizar_texto('Seleccione impresora')
        else:
            # Modo camarero u otros
            self._cargar_tickets_dia()
    
    def _on_release_comodin(self, event) -> None:
        event.widget.invertir_colores()
    
    def _on_click_volver(self, event) -> None:
        """Vuelve a la pantalla anterior."""
        event.widget.invertir_colores()
    
    def _on_release_volver(self, event) -> None:
        event.widget.invertir_colores()
        
        if self.callback_volver:
            self.callback_volver()
    
    def _on_imprimir_press(self, event) -> None:
        """Imprime el ticket actual."""
        event.widget.invertir_colores()
        
        texto = self.ticket_display.cget('text')
        if texto and self.printer_controller:
            # Obtener impresora principal
            impresoras = self.callback_obtener_impresoras() if self.callback_obtener_impresoras else ['', '']
            if impresoras and impresoras[0]:
                self.printer_controller.imprimir_ticket(texto, impresoras[0])
    
    def _on_imprimir_release(self, event) -> None:
        """Maneja la liberación del botón imprimir."""
        event.widget.invertir_colores()
    
    # ========================================================================
    # MÉTODOS AUXILIARES
    # ========================================================================
    
    def _cambiar_fecha(self, nueva_fecha: datetime.date) -> None:
        """
        Cambia la fecha actual y actualiza la interfaz.
        
        Args:
            nueva_fecha: Nueva fecha a establecer
        """
        self.fecha_actual = nueva_fecha
        self.calendar_controller.establecer_fecha(nueva_fecha)
        
        # Actualizar fechado
        self.fechado.cambiar_texto(nueva_fecha.strftime('%d/%m/%Y'))
        
        # Actualizar control de día
        dia = nueva_fecha.strftime('%A')
        dia = f'{dia[:3].upper()}, {str(nueva_fecha.day).zfill(2)}'
        self.marcos_fecha[0].cambiar_texto(dia)
        
        # Actualizar días si es necesario
        self._actualizar_dias()
        
        # Cargar tickets
        self._cargar_tickets_dia()
        
        # Limpiar ticket
        self.ticket_display.limpiar()
        
        # Mostrar panel de días
        self.panel_dias.traer_al_frente()
    
    def _cargar_tickets_dia(self) -> None:
        """Carga los tickets del día actual en el listado."""
        self.panel_listado.limpiar()
        
        recibos = self.calendar_controller.obtener_recibos_dia(self.fecha_actual)
        
        for recibo in recibos:
            self.panel_listado.agregar_item(recibo.fecha)
    
    def vincular_callback_volver(self, callback: Callable) -> None:
        """
        Vincula el callback para el botón volver.
        
        Args:
            callback: Función a llamar al presionar volver
        """
        self.callback_volver = callback
    
    def vincular_callback_impresoras(self, callback: Callable) -> None:
        """
        Vincula el callback para obtener impresoras.
        
        Args:
            callback: Función que retorna la lista de impresoras
        """
        self.callback_obtener_impresoras = callback
    
    def establecer_iva(self, iva: float) -> None:
        """
        Establece el IVA actual.
        
        Args:
            iva: Valor del IVA
        """
        self.iva_actual = iva
        self.info_iva.cambiar_texto(f'{iva}% de IVA')
    
    def inicializar(self) -> None:
        """Inicializa la vista con los datos actuales."""
        self.fecha_actual = datetime.date.today()
        self._cambiar_fecha(self.fecha_actual)


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'CalendarView'
]