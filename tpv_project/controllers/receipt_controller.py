"""
Controlador de recibos.

Este módulo maneja la lógica de negocio de los recibos/tickets.
"""

from typing import Optional, List
from datetime import datetime
from models.receipt import Receipt, LineaRecibo, ReceiptManager
from models.product import ProductManager, Product
from config.settings import TicketConfig
from data.data_manager import DataManager


class ReceiptController:
    """Controlador para gestión de recibos."""
    
    def __init__(self, data_manager: DataManager, 
                 receipt_manager: ReceiptManager):
        """
        Inicializa el controlador de recibos.
        
        Args:
            data_manager: Gestor de datos
            receipt_manager: Gestor de recibos anuales
        """
        self.data_manager = data_manager
        self.receipt_manager = receipt_manager
        self._recibo_actual: Receipt = self._crear_recibo_nuevo()
    
    def _crear_recibo_nuevo(self) -> Receipt:
        """
        Crea un nuevo recibo vacío.
        
        Returns:
            Receipt: Nuevo recibo
        """
        return Receipt(
            nombre=TicketConfig.HEADER,
            estado=TicketConfig.ESTADO_NUEVO
        )
    
    def obtener_recibo_actual(self) -> Receipt:
        """
        Obtiene el recibo actual en edición.
        
        Returns:
            Receipt: Recibo actual
        """
        return self._recibo_actual
    
    def establecer_recibo_actual(self, recibo: Receipt) -> None:
        """
        Establece el recibo actual.
        
        Args:
            recibo: Recibo a establecer como actual
        """
        self._recibo_actual = recibo
    
    def crear_nuevo_recibo(self, camarero: str = "") -> Receipt:
        """
        Crea un nuevo recibo y lo establece como actual.
        
        Args:
            camarero: Nombre del camarero
            
        Returns:
            Receipt: Nuevo recibo creado
        """
        self._recibo_actual = self._crear_recibo_nuevo()
        self._recibo_actual.camarero = camarero
        return self._recibo_actual
    
    def agregar_producto(self, nombre_producto: str, cantidad: int = 1) -> bool:
        """
        Agrega un producto al recibo actual.
        
        Args:
            nombre_producto: Nombre del producto
            cantidad: Cantidad a agregar (puede ser negativo para quitar)
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        # Buscar el producto
        producto = self.data_manager.products.obtener_producto(nombre_producto)
        
        if producto is None:
            print(f"Producto no encontrado: {nombre_producto}")
            return False
        
        # Crear línea de recibo
        linea = LineaRecibo(
            cantidad=cantidad,
            nombre=producto.nombre,
            precio=producto.precio,
            familia=producto.familia
        )
        
        if cantidad > 0:
            self._recibo_actual.agregar_linea(linea)
        else:
            self._recibo_actual.quitar_linea(producto.nombre, abs(cantidad))
        
        return True
    
    def agregar_producto_varios(self, precio: float, cantidad: int = 1) -> bool:
        """
        Agrega un producto "Varios" con precio personalizado.
        
        Args:
            precio: Precio del producto
            cantidad: Cantidad
            
        Returns:
            bool: True si se agregó correctamente
        """
        linea = LineaRecibo(
            cantidad=cantidad,
            nombre='Varios',
            precio=precio,
            familia='Varios'
        )
        
        if cantidad > 0:
            self._recibo_actual.agregar_linea(linea)
        else:
            self._recibo_actual.quitar_linea('Varios', abs(cantidad))
        
        return True
    
    def quitar_producto(self, nombre_producto: str, cantidad: int = 1) -> bool:
        """
        Quita un producto del recibo actual.
        
        Args:
            nombre_producto: Nombre del producto
            cantidad: Cantidad a quitar
            
        Returns:
            bool: True si se quitó correctamente
        """
        return self._recibo_actual.quitar_linea(nombre_producto, cantidad)
    
    def limpiar_recibo_actual(self) -> None:
        """Limpia el recibo actual."""
        self._recibo_actual.limpiar()
    
    def recibo_tiene_productos(self) -> bool:
        """
        Verifica si el recibo actual tiene productos.
        
        Returns:
            bool: True si tiene productos, False si está vacío
        """
        return not self._recibo_actual.esta_vacio()
    
    def finalizar_recibo_efectivo(self, camarero: str = "") -> Receipt:
        """
        Finaliza el recibo actual marcándolo como pagado en efectivo.
        
        Args:
            camarero: Nombre del camarero
            
        Returns:
            Receipt: Recibo finalizado
        """
        self._recibo_actual.marcar_como_pagado(
            TicketConfig.ESTADO_EFECTIVO, 
            camarero
        )
        
        # Agregar al gestor de recibos
        mes = datetime.now().month
        self.receipt_manager.agregar_recibo(self._recibo_actual, mes)
        
        # Guardar
        self.data_manager.guardar_recibos_anuales(self.receipt_manager)
        
        # Crear nuevo recibo
        recibo_finalizado = self._recibo_actual
        self.crear_nuevo_recibo(camarero)
        
        return recibo_finalizado
    
    def finalizar_recibo_tarjeta(self, camarero: str = "") -> Receipt:
        """
        Finaliza el recibo actual marcándolo como pagado con tarjeta.
        
        Args:
            camarero: Nombre del camarero
            
        Returns:
            Receipt: Recibo finalizado
        """
        self._recibo_actual.marcar_como_pagado(
            TicketConfig.ESTADO_TARJETA, 
            camarero
        )
        
        # Agregar al gestor de recibos
        mes = datetime.now().month
        self.receipt_manager.agregar_recibo(self._recibo_actual, mes)
        
        # Guardar
        self.data_manager.guardar_recibos_anuales(self.receipt_manager)
        
        # Crear nuevo recibo
        recibo_finalizado = self._recibo_actual
        self.crear_nuevo_recibo(camarero)
        
        return recibo_finalizado
    
    def guardar_recibo_pendiente(self, nombre_cliente: str, 
                                 camarero: str = "") -> Receipt:
        """
        Guarda el recibo actual como pendiente de pago.
        
        Args:
            nombre_cliente: Nombre del cliente
            camarero: Nombre del camarero
            
        Returns:
            Receipt: Recibo guardado
        """
        self._recibo_actual.marcar_como_pendiente(nombre_cliente, camarero)
        
        # Agregar a pendientes
        self.data_manager.agregar_recibo_pendiente(self._recibo_actual)
        
        # Agregar cliente si no existe
        if not self.data_manager.customers.existe_cliente(nombre_cliente):
            try:
                self.data_manager.customers.agregar_cliente(nombre_cliente)
            except:
                pass
        
        # Guardar
        self.data_manager.guardar_datos_generales()
        
        # Crear nuevo recibo
        recibo_guardado = self._recibo_actual
        self.crear_nuevo_recibo(camarero)
        
        return recibo_guardado
    
    def cargar_recibo_pendiente(self, fecha: str) -> Optional[Receipt]:
        """
        Carga un recibo pendiente por su fecha.
        
        Args:
            fecha: Fecha del recibo
            
        Returns:
            Optional[Receipt]: Recibo si existe, None en caso contrario
        """
        recibo = self.data_manager.obtener_recibo_pendiente(fecha)
        
        if recibo:
            self._recibo_actual = recibo
            return recibo
        
        return None
    
    def pagar_recibo_pendiente(self, fecha: str, metodo_pago: str,
                               camarero: str = "") -> bool:
        """
        Marca un recibo pendiente como pagado.
        
        Args:
            fecha: Fecha del recibo pendiente
            metodo_pago: Método de pago ('efectivo' o 'tarjeta')
            camarero: Nombre del camarero
            
        Returns:
            bool: True si se pagó correctamente
        """
        # Cargar el recibo
        if not self.cargar_recibo_pendiente(fecha):
            return False
        
        # Eliminar de pendientes
        self.data_manager.eliminar_recibo_pendiente(fecha)
        
        # Finalizar según método de pago
        if metodo_pago == TicketConfig.ESTADO_EFECTIVO:
            self.finalizar_recibo_efectivo(camarero)
        else:
            self.finalizar_recibo_tarjeta(camarero)
        
        return True
    
    def unir_recibos_pendientes_cliente(self, nombre_cliente: str) -> Optional[Receipt]:
        """
        Une todos los recibos pendientes de un cliente.
        
        Args:
            nombre_cliente: Nombre del cliente
            
        Returns:
            Optional[Receipt]: Recibo unificado o None si no hay recibos
        """
        recibo_unido = self.data_manager.unir_recibos_pendientes(nombre_cliente)
        
        if recibo_unido:
            self.data_manager.guardar_datos_generales()
            return recibo_unido
        
        return None
    
    def generar_texto_ticket(self) -> str:
        """
        Genera el texto del ticket actual para visualización.
        
        Returns:
            str: Texto del ticket formateado
        """
        return self._recibo_actual.generar_texto_ticket(
            self.data_manager.iva
        )
    
    def calcular_total_actual(self) -> float:
        """
        Calcula el total del recibo actual.
        
        Returns:
            float: Total del recibo
        """
        return self._recibo_actual.calcular_total()


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'ReceiptController'
]