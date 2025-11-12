"""
Controlador de calendario y reportes.

Este módulo maneja la lógica del calendario y la generación de reportes.
"""

import datetime
from typing import Dict, List, Tuple, Optional
from models.receipt import Receipt, ReceiptManager
from config.settings import CalendarConfig, TicketConfig


class CalendarController:
    """Controlador para gestión de calendario y reportes."""
    
    def __init__(self, receipt_manager: ReceiptManager):
        """
        Inicializa el controlador de calendario.
        
        Args:
            receipt_manager: Gestor de recibos
        """
        self.receipt_manager = receipt_manager
        self._fecha_actual: datetime.date = datetime.date.today()
    
    def obtener_fecha_actual(self) -> datetime.date:
        """
        Obtiene la fecha actual seleccionada.
        
        Returns:
            datetime.date: Fecha actual
        """
        return self._fecha_actual
    
    def establecer_fecha(self, fecha: datetime.date) -> None:
        """
        Establece la fecha actual.
        
        Args:
            fecha: Nueva fecha
        """
        self._fecha_actual = fecha
    
    def obtener_dias_mes(self, fecha: datetime.date) -> int:
        """
        Obtiene el número de días de un mes.
        
        Args:
            fecha: Fecha del mes a consultar
            
        Returns:
            int: Número de días del mes
        """
        dia = datetime.timedelta(days=1)
        siguiente = fecha + dia
        
        while fecha.month == siguiente.month:
            fecha = fecha + dia
            siguiente = fecha + dia
        
        return fecha.day
    
    def obtener_primer_dia_semana(self, fecha: datetime.date) -> int:
        """
        Obtiene el día de la semana del primer día del mes.
        
        Args:
            fecha: Fecha del mes
            
        Returns:
            int: Día de la semana (0=Lunes, 6=Domingo)
        """
        primer_dia = datetime.date(fecha.year, fecha.month, 1)
        return primer_dia.weekday()
    
    def obtener_recibos_dia(self, fecha: datetime.date) -> List[Receipt]:
        """
        Obtiene todos los recibos de un día específico.
        
        Args:
            fecha: Fecha a consultar
            
        Returns:
            List[Receipt]: Lista de recibos del día
        """
        recibos_mes = self.receipt_manager.obtener_recibos_mes(fecha.month)
        fecha_str = fecha.strftime('%d/%m/%Y')
        
        recibos_dia = []
        for recibo in recibos_mes:
            fecha_recibo, _ = recibo.fecha.split(' - ')
            if fecha_recibo == fecha_str:
                recibos_dia.append(recibo)
        
        return recibos_dia
    
    def calcular_total_dia(self, fecha: datetime.date, 
                          metodo_pago: Optional[str] = None) -> float:
        """
        Calcula el total de ventas de un día.
        
        Args:
            fecha: Fecha a consultar
            metodo_pago: Filtrar por método de pago ('efectivo', 'tarjeta')
                        Si es None, suma todos
            
        Returns:
            float: Total de ventas
        """
        recibos = self.obtener_recibos_dia(fecha)
        
        total = 0.0
        for recibo in recibos:
            if metodo_pago is None or recibo.estado == metodo_pago:
                total += recibo.calcular_total()
        
        return total
    
    def calcular_total_mes(self, fecha: datetime.date,
                          metodo_pago: Optional[str] = None) -> float:
        """
        Calcula el total de ventas de un mes.
        
        Args:
            fecha: Fecha del mes a consultar
            metodo_pago: Filtrar por método de pago
            
        Returns:
            float: Total de ventas del mes
        """
        recibos_mes = self.receipt_manager.obtener_recibos_mes(fecha.month)
        
        total = 0.0
        for recibo in recibos_mes:
            if metodo_pago is None or recibo.estado == metodo_pago:
                total += recibo.calcular_total()
        
        return total
    
    def generar_reporte_diario(self, fecha: datetime.date, iva: float) -> str:
        """
        Genera un reporte de ventas diarias.
        
        Args:
            fecha: Fecha del reporte
            iva: Porcentaje de IVA
            
        Returns:
            str: Texto del reporte formateado
        """
        lineas = []
        lineas.append('')
        lineas.append('-' * 30)
        lineas.append('REPORTE DIARIO')
        lineas.append(fecha.strftime("%d de %B de %Y"))
        lineas.append('-' * 30)
        
        total_efectivo = self.calcular_total_dia(fecha, 'efectivo')
        total_tarjeta = self.calcular_total_dia(fecha, 'tarjeta')
        total = total_efectivo + total_tarjeta
        
        lineas.append(f'Efectivo: {total_efectivo:.2f}€')
        lineas.append(f'Tarjeta: {total_tarjeta:.2f}€')
        lineas.append('-' * 30)
        
        base = total / (1 + iva / 100)
        lineas.append(f'Base imponible: {base:.2f}€')
        
        importe_iva = total - base
        lineas.append(f'{iva}% de IVA: {importe_iva:.2f}€')
        
        lineas.append(f'Total: {total:.2f}€')
        lineas.append('-' * 30)
        lineas.append('.')
        
        return '\n'.join(lineas)
    
    def generar_reporte_mensual(self, fecha: datetime.date, iva: float) -> str:
        """
        Genera un reporte de ventas mensuales.
        
        Args:
            fecha: Fecha del mes
            iva: Porcentaje de IVA
            
        Returns:
            str: Texto del reporte formateado
        """
        lineas = []
        lineas.append('')
        lineas.append('-' * 30)
        lineas.append('REPORTE MENSUAL')
        lineas.append(fecha.strftime("%B de %Y"))
        lineas.append('-' * 30)
        
        total_efectivo = self.calcular_total_mes(fecha, 'efectivo')
        total_tarjeta = self.calcular_total_mes(fecha, 'tarjeta')
        total = total_efectivo + total_tarjeta
        
        lineas.append(f'Efectivo: {total_efectivo:.2f}€')
        lineas.append(f'Tarjeta: {total_tarjeta:.2f}€')
        lineas.append('-' * 30)
        
        base = total / (1 + iva / 100)
        lineas.append(f'Base imponible: {base:.2f}€')
        
        importe_iva = total - base
        lineas.append(f'{iva}% de IVA: {importe_iva:.2f}€')
        
        lineas.append(f'Total: {total:.2f}€')
        lineas.append('-' * 30)
        lineas.append('.')
        
        return '\n'.join(lineas)
    
    def generar_reporte_dia_a_dia(self, fecha: datetime.date, iva: float) -> str:
        """
        Genera un reporte día a día del mes.
        
        Args:
            fecha: Fecha del mes
            iva: Porcentaje de IVA
            
        Returns:
            str: Texto del reporte formateado
        """
        lineas = []
        lineas.append('')
        lineas.append('-' * 30)
        lineas.append('REPORTE DÍA A DÍA')
        lineas.append(fecha.strftime("%B de %Y"))
        lineas.append('-' * 30)
        
        num_dias = self.obtener_dias_mes(fecha)
        total_general = 0.0
        
        for dia in range(1, num_dias + 1):
            fecha_dia = datetime.date(fecha.year, fecha.month, dia)
            total_dia = self.calcular_total_dia(fecha_dia)
            total_general += total_dia
            
            fecha_str = fecha_dia.strftime("%d/%m/%Y")
            importe_str = f'{total_dia:.2f}'
            puntos = 30 - len(fecha_str) - len(importe_str) - 2
            lineas.append(f'{fecha_str}:{"." * puntos}{importe_str}€')
        
        lineas.append('-' * 30)
        
        base = total_general / (1 + iva / 100)
        lineas.append(f'Base imponible: {base:.2f}€')
        
        importe_iva = total_general - base
        lineas.append(f'{iva}% de IVA: {importe_iva:.2f}€')
        
        lineas.append(f'Total: {total_general:.2f}€')
        lineas.append('-' * 30)
        lineas.append('.')
        
        return '\n'.join(lineas)
    
    def generar_reporte_por_metodo(self, fecha: datetime.date, 
                                   metodo: str, iva: float) -> str:
        """
        Genera un reporte por método de pago día a día.
        
        Args:
            fecha: Fecha del mes
            metodo: Método de pago ('efectivo' o 'tarjeta')
            iva: Porcentaje de IVA
            
        Returns:
            str: Texto del reporte formateado
        """
        lineas = []
        lineas.append('')
        lineas.append('-' * 30)
        titulo = f'REPORTE {metodo.upper()}'
        lineas.append(titulo)
        lineas.append(fecha.strftime("%B de %Y"))
        lineas.append('-' * 30)
        
        num_dias = self.obtener_dias_mes(fecha)
        total_general = 0.0
        
        for dia in range(1, num_dias + 1):
            fecha_dia = datetime.date(fecha.year, fecha.month, dia)
            total_dia = self.calcular_total_dia(fecha_dia, metodo)
            total_general += total_dia
            
            fecha_str = fecha_dia.strftime("%d/%m/%Y")
            importe_str = f'{total_dia:.2f}'
            puntos = 30 - len(fecha_str) - len(importe_str) - 2
            lineas.append(f'{fecha_str}:{"." * puntos}{importe_str}€')
        
        lineas.append('-' * 30)
        
        base = total_general / (1 + iva / 100)
        lineas.append(f'Base imponible: {base:.2f}€')
        
        importe_iva = total_general - base
        lineas.append(f'{iva}% de IVA: {importe_iva:.2f}€')
        
        lineas.append(f'Total: {total_general:.2f}€')
        lineas.append('-' * 30)
        lineas.append('.')
        
        return '\n'.join(lineas)
    
    def obtener_recibos_camarero(self, nombre_camarero: str,
                                fecha: datetime.date) -> List[Receipt]:
        """
        Obtiene los recibos de un camarero en un mes.
        
        Args:
            nombre_camarero: Nombre del camarero
            fecha: Fecha del mes
            
        Returns:
            List[Receipt]: Lista de recibos del camarero
        """
        recibos_mes = self.receipt_manager.obtener_recibos_mes(fecha.month)
        return [r for r in recibos_mes if r.camarero == nombre_camarero]
    
    def obtener_camareros_activos(self, fecha: datetime.date) -> List[str]:
        """
        Obtiene la lista de camareros que tienen recibos en un mes.
        
        Args:
            fecha: Fecha del mes
            
        Returns:
            List[str]: Lista de nombres de camareros
        """
        recibos_mes = self.receipt_manager.obtener_recibos_mes(fecha.month)
        camareros = set()
        
        for recibo in recibos_mes:
            if recibo.camarero:
                camareros.add(recibo.camarero)
        
        return sorted(list(camareros))


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'CalendarController'
]