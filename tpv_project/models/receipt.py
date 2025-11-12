"""
Modelo de datos para Recibos/Tickets.

Este módulo define la estructura y operaciones relacionadas con recibos.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime
from config.settings import TicketConfig
from utils.formatters import (
    formatear_linea_ticket,
    calcular_base_imponible,
    calcular_iva
)


@dataclass
class LineaRecibo:
    """Representa una línea de un recibo."""
    
    cantidad: int
    nombre: str
    precio: float
    familia: str
    
    def calcular_total(self) -> float:
        """
        Calcula el total de esta línea.
        
        Returns:
            float: Total (cantidad * precio)
        """
        return self.cantidad * self.precio
    
    def to_list(self) -> List:
        """
        Convierte la línea a lista (formato original).
        
        Returns:
            List: [cantidad, nombre, precio, familia]
        """
        return [self.cantidad, self.nombre, self.precio, self.familia]
    
    @classmethod
    def from_list(cls, data: List) -> 'LineaRecibo':
        """
        Crea una línea desde una lista.
        
        Args:
            data: Lista con [cantidad, nombre, precio, familia]
            
        Returns:
            LineaRecibo: Instancia de línea de recibo
        """
        return cls(
            cantidad=data[0],
            nombre=data[1],
            precio=float(data[2]),
            familia=data[3]
        )


@dataclass
class Receipt:
    """Representa un recibo/ticket."""
    
    pedido: List[LineaRecibo] = field(default_factory=list)
    nombre: str = TicketConfig.HEADER
    fecha: str = ""
    estado: str = TicketConfig.ESTADO_NUEVO
    impreso: bool = False
    camarero: str = ""
    
    def __post_init__(self):
        """Inicializa la fecha si está vacía."""
        if not self.fecha:
            self.fecha = datetime.now().strftime(TicketConfig.DATETIME_FORMAT)
    
    def agregar_linea(self, linea: LineaRecibo) -> None:
        """
        Agrega una línea al pedido.
        
        Args:
            linea: Línea a agregar
        """
        # Buscar si ya existe el producto
        for linea_existente in self.pedido:
            if linea_existente.nombre == linea.nombre:
                linea_existente.cantidad += linea.cantidad
                return
        
        # Si no existe, agregar nueva línea
        self.pedido.append(linea)
    
    def quitar_linea(self, nombre: str, cantidad: int = 1) -> bool:
        """
        Quita unidades de una línea del pedido.
        
        Args:
            nombre: Nombre del producto
            cantidad: Cantidad a quitar
            
        Returns:
            bool: True si se quitó, False si no existía
        """
        for i, linea in enumerate(self.pedido):
            if linea.nombre == nombre:
                linea.cantidad -= cantidad
                if linea.cantidad <= 0:
                    del self.pedido[i]
                return True
        return False
    
    def calcular_subtotal(self) -> float:
        """
        Calcula el subtotal del recibo (sin IVA).
        
        Returns:
            float: Subtotal
        """
        return sum(linea.calcular_total() for linea in self.pedido)
    
    def calcular_total(self) -> float:
        """
        Calcula el total del recibo (con IVA).
        
        Returns:
            float: Total
        """
        return self.calcular_subtotal()
    
    def calcular_base_imponible(self, iva: float) -> float:
        """
        Calcula la base imponible del recibo.
        
        Args:
            iva: Porcentaje de IVA
            
        Returns:
            float: Base imponible
        """
        total = self.calcular_total()
        return calcular_base_imponible(total, iva)
    
    def calcular_importe_iva(self, iva: float) -> float:
        """
        Calcula el importe del IVA del recibo.
        
        Args:
            iva: Porcentaje de IVA
            
        Returns:
            float: Importe del IVA
        """
        total = self.calcular_total()
        return calcular_iva(total, iva)
    
    def esta_vacio(self) -> bool:
        """
        Verifica si el recibo está vacío.
        
        Returns:
            bool: True si no tiene líneas, False en caso contrario
        """
        return len(self.pedido) == 0
    
    def limpiar(self) -> None:
        """Limpia todas las líneas del pedido."""
        self.pedido.clear()
    
    def marcar_como_pagado(self, metodo_pago: str, camarero: str = "") -> None:
        """
        Marca el recibo como pagado.
        
        Args:
            metodo_pago: Método de pago ('efectivo' o 'tarjeta')
            camarero: Nombre del camarero
        """
        self.nombre = f'Pagado {metodo_pago}'
        self.estado = metodo_pago
        self.fecha = datetime.now().strftime(TicketConfig.DATETIME_FORMAT)
        if camarero:
            self.camarero = camarero
    
    def marcar_como_pendiente(self, nombre_cliente: str, camarero: str = "") -> None:
        """
        Marca el recibo como pendiente de pago.
        
        Args:
            nombre_cliente: Nombre del cliente
            camarero: Nombre del camarero
        """
        self.nombre = nombre_cliente
        self.estado = TicketConfig.ESTADO_PENDIENTE
        self.fecha = datetime.now().strftime(TicketConfig.DATETIME_FORMAT)
        self.impreso = False
        if camarero:
            self.camarero = camarero
    
    def to_dict(self) -> Dict:
        """
        Convierte el recibo a diccionario.
        
        Returns:
            Dict: Diccionario con los datos del recibo
        """
        return {
            'pedido': [linea.to_list() for linea in self.pedido],
            'nombre': self.nombre,
            'fecha': self.fecha,
            'estado': self.estado,
            'impreso': self.impreso,
            'camarero': self.camarero
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Receipt':
        """
        Crea un recibo desde un diccionario.
        
        Args:
            data: Diccionario con los datos del recibo
            
        Returns:
            Receipt: Instancia de recibo
        """
        pedido = [LineaRecibo.from_list(linea) for linea in data['pedido']]
        
        return cls(
            pedido=pedido,
            nombre=data['nombre'],
            fecha=data['fecha'],
            estado=data['estado'],
            impreso=data['impreso'],
            camarero=data.get('camarero', '')
        )
    
    def generar_texto_ticket(self, iva: float) -> str:
        """
        Genera el texto completo del ticket para imprimir.
        
        Args:
            iva: Porcentaje de IVA
            
        Returns:
            str: Texto del ticket formateado
        """
        lineas = []
        
        # Cabecera
        lineas.append('')
        lineas.append(TicketConfig.TICKET_SEPARATOR)
        lineas.append(self.nombre)
        lineas.append(self.fecha)
        lineas.append(TicketConfig.TICKET_SEPARATOR)
        
        # Líneas del pedido
        if self.pedido:
            for linea in self.pedido:
                lineas.append(formatear_linea_ticket(
                    linea.cantidad,
                    linea.nombre,
                    linea.precio
                ))
            
            # Totales
            lineas.append(TicketConfig.TICKET_SEPARATOR)
            
            base = self.calcular_base_imponible(iva)
            lineas.append(f'Base imponible: {base:.2f}€')
            
            importe_iva = self.calcular_importe_iva(iva)
            lineas.append(f'{iva}% de IVA: {importe_iva:.2f}€')
            
            total = self.calcular_total()
            lineas.append(f'Total a pagar: {total:.2f}€')
        
        # Pie
        lineas.append(TicketConfig.TICKET_SEPARATOR)
        lineas.append('Gracias por su Visita!!!')
        lineas.append('.')
        
        return '\n'.join(lineas)


class ReceiptManager:
    """Gestiona la colección de recibos."""
    
    def __init__(self):
        """Inicializa el gestor de recibos."""
        # Lista por meses [enero, febrero, ..., diciembre]
        self._recibos_anuales: List[List[Receipt]] = [[] for _ in range(12)]
    
    def agregar_recibo(self, recibo: Receipt, mes: Optional[int] = None) -> None:
        """
        Agrega un recibo.
        
        Args:
            recibo: Recibo a agregar
            mes: Mes (1-12). Si es None, se extrae de la fecha del recibo
        """
        if mes is None:
            # Extraer mes de la fecha del recibo
            fecha_str = recibo.fecha.split(' - ')[0]
            mes = int(fecha_str.split('/')[1])
        
        if 1 <= mes <= 12:
            self._recibos_anuales[mes - 1].append(recibo)
    
    def obtener_recibos_mes(self, mes: int) -> List[Receipt]:
        """
        Obtiene todos los recibos de un mes.
        
        Args:
            mes: Mes (1-12)
            
        Returns:
            List[Receipt]: Lista de recibos del mes
        """
        if 1 <= mes <= 12:
            return self._recibos_anuales[mes - 1].copy()
        return []
    
    def obtener_todos_recibos(self) -> List[Receipt]:
        """
        Obtiene todos los recibos de todos los meses.
        
        Returns:
            List[Receipt]: Lista de todos los recibos
        """
        todos = []
        for mes_recibos in self._recibos_anuales:
            todos.extend(mes_recibos)
        return todos
    
    def cargar_recibos_anuales(self, datos: List[List[Dict]]) -> None:
        """
        Carga recibos anuales desde datos.
        
        Args:
            datos: Lista de 12 listas (una por mes) con diccionarios de recibos
        """
        self._recibos_anuales = [[] for _ in range(12)]
        
        for mes_idx, mes_datos in enumerate(datos):
            for recibo_data in mes_datos:
                try:
                    recibo = Receipt.from_dict(recibo_data)
                    self._recibos_anuales[mes_idx].append(recibo)
                except Exception as e:
                    print(f"Error al cargar recibo: {e}")
    
    def exportar_recibos_anuales(self) -> List[List[Dict]]:
        """
        Exporta todos los recibos como lista de listas de diccionarios.
        
        Returns:
            List[List[Dict]]: Datos de recibos por mes
        """
        return [
            [r.to_dict() for r in mes_recibos]
            for mes_recibos in self._recibos_anuales
        ]
    
    def limpiar(self) -> None:
        """Elimina todos los recibos."""
        self._recibos_anuales = [[] for _ in range(12)]


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'LineaRecibo',
    'Receipt',
    'ReceiptManager'
]