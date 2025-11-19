"""
Gestor de persistencia de datos.

Este módulo maneja la carga y guardado de todos los datos de la aplicación.
"""

import os
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path

from core.encryption import get_encryption_manager
from models.product import ProductManager
from models.receipt import ReceiptManager, Receipt
from models.customer import CustomerManager, WaiterManager
from config.settings import DATA_FILE, DATA_DIR, TicketConfig


class DataManager:
    """Gestiona la persistencia de todos los datos de la aplicación."""
    
    def __init__(self):
        """Inicializa el gestor de datos."""
        self._encryption = get_encryption_manager()
        
        # Gestores de datos
        self.products = ProductManager()
        self.receipts_pending = []  # Recibos impagados
        self.customers = CustomerManager()
        self.waiters = WaiterManager()
        
        # Configuración
        self.iva = TicketConfig.DEFAULT_IVA
        self.password = ''
        self.printers = ['', '']  # [principal, comanda]
    
    def guardar_datos_generales(self) -> None:
        """
        Guarda los datos generales en data.tpv.
        
        Incluye: productos, recibos impagados, clientes, camareros,
                IVA, password, impresoras.
                
        Raises:
            Exception: Si hay error al guardar
        """
        try:
            datos = [
                self.products.exportar_productos(),
                [r.to_dict() for r in self.receipts_pending],
                self.customers.exportar_clientes(),
                self.waiters.exportar_camareros(),
                self.iva,
                self.password,
                self.printers
            ]
            
            self._encryption.guardar_archivo_encriptado(
                str(DATA_FILE),
                datos,
                usar_json=True
            )
            
        except Exception as e:
            raise Exception(f"Error al guardar datos generales: {str(e)}")
    
    def cargar_datos_generales(self) -> bool:
        """
        Carga los datos generales desde data.tpv.
        
        Si el archivo no existe, se crea con datos vacíos.
        
        Returns:
            bool: True si se cargaron datos, False si se creó archivo nuevo
            
        Raises:
            Exception: Si hay error al cargar
        """
        try:
            if not os.path.exists(DATA_FILE):
                # Crear archivo con datos por defecto
                self.guardar_datos_generales()
                return False
            
            datos = self._encryption.cargar_archivo_encriptado(
                str(DATA_FILE),
                usar_json=True
            )
            
            if datos and len(datos) >= 7:
                # Cargar productos
                self.products.cargar_productos(datos[0])
                
                # Cargar recibos impagados
                self.receipts_pending = [
                    Receipt.from_dict(r) for r in datos[1]
                ]
                
                # Cargar clientes
                self.customers.cargar_clientes(datos[2])
                
                # Cargar camareros
                self.waiters.cargar_camareros(datos[3])
                
                # Cargar configuración
                self.iva = datos[4]
                self.password = datos[5]
                self.printers = datos[6]
                
                return True
            
            return False
            
        except Exception as e:
            raise Exception(f"Error al cargar datos generales: {str(e)}")
    
    def guardar_recibos_anuales(self, recibos_manager: ReceiptManager,
                                anio: int = None) -> None:
        """
        Guarda los recibos anuales en anual.{año}.tpv.
        
        Args:
            recibos_manager: Gestor de recibos con los datos del año
            anio: Año a guardar. Si es None, usa el año actual
            
        Raises:
            Exception: Si hay error al guardar
        """
        if anio is None:
            anio = datetime.now().year
        
        archivo = DATA_DIR / f'anual.{anio}.tpv'
        
        try:
            datos = recibos_manager.exportar_recibos_anuales()
            
            self._encryption.guardar_archivo_encriptado(
                str(archivo),
                datos,
                usar_json=True
            )
            
        except Exception as e:
            raise Exception(f"Error al guardar recibos anuales: {str(e)}")
    
    def cargar_recibos_anuales(self, anio: int = None) -> ReceiptManager:
        """
        Carga los recibos anuales desde anual.{año}.tpv.
        
        Args:
            anio: Año a cargar. Si es None, usa el año actual
            
        Returns:
            ReceiptManager: Gestor con los recibos del año
            
        Raises:
            Exception: Si hay error al cargar
        """
        if anio is None:
            anio = datetime.now().year
        
        archivo = DATA_DIR / f'anual.{anio}.tpv'
        
        manager = ReceiptManager()
        
        try:
            if os.path.exists(archivo):
                datos = self._encryption.cargar_archivo_encriptado(
                    str(archivo),
                    usar_json=True
                )
                manager.cargar_recibos_anuales(datos)
            
            return manager
            
        except Exception as e:
            raise Exception(f"Error al cargar recibos anuales: {str(e)}")
    
    def agregar_recibo_pendiente(self, recibo: Receipt) -> None:
        """
        Agrega un recibo a la lista de pendientes.
        
        Args:
            recibo: Recibo a agregar
        """
        self.receipts_pending.append(recibo)
    
    def eliminar_recibo_pendiente(self, fecha: str) -> bool:
        """
        Elimina un recibo pendiente por su fecha.
        
        Args:
            fecha: Fecha del recibo
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        for i, recibo in enumerate(self.receipts_pending):
            if recibo.fecha == fecha:
                del self.receipts_pending[i]
                return True
        return False
    
    def obtener_recibo_pendiente(self, fecha: str) -> Receipt:
        """
        Obtiene un recibo pendiente por su fecha.
        
        Args:
            fecha: Fecha del recibo
            
        Returns:
            Receipt: Recibo si existe, None en caso contrario
        """
        for recibo in self.receipts_pending:
            if recibo.fecha == fecha:
                return recibo
        return None
    
    def obtener_recibos_pendientes_cliente(self, nombre_cliente: str) -> List[Receipt]:
        """
        Obtiene todos los recibos pendientes de un cliente.
        
        Args:
            nombre_cliente: Nombre del cliente
            
        Returns:
            List[Receipt]: Lista de recibos pendientes
        """
        return [
            r for r in self.receipts_pending 
            if r.nombre == nombre_cliente
        ]
    
    def cliente_tiene_pendientes(self, nombre_cliente: str) -> bool:
        """
        Verifica si un cliente tiene recibos pendientes.
        
        Args:
            nombre_cliente: Nombre del cliente
            
        Returns:
            bool: True si tiene pendientes, False en caso contrario
        """
        return any(r.nombre == nombre_cliente for r in self.receipts_pending)
    
    def unir_recibos_pendientes(self, nombre_cliente: str) -> Receipt:
        """
        Une todos los recibos pendientes de un cliente en uno solo.
        
        IMPORTANTE: Este método ELIMINA los recibos sueltos del cliente
        y crea un nuevo recibo unificado que contiene todas las líneas.
        
        Args:
            nombre_cliente: Nombre del cliente
            
        Returns:
            Receipt: Recibo unificado, o None si no hay recibos
        """
        recibos_cliente = self.obtener_recibos_pendientes_cliente(nombre_cliente)
        
        if not recibos_cliente:
            return None
        
        # Crear nuevo recibo con todas las líneas
        recibo_unido = Receipt(
            nombre=nombre_cliente,
            fecha=recibos_cliente[0].fecha,
            estado=TicketConfig.ESTADO_PENDIENTE,
            camarero=recibos_cliente[0].camarero
        )
        
        # Unir todas las líneas
        for recibo in recibos_cliente:
            for linea in recibo.pedido:
                recibo_unido.agregar_linea(linea)
        
        # CORRECCIÓN: Eliminar recibos antiguos sueltos
        self.receipts_pending = [
            r for r in self.receipts_pending 
            if r.nombre != nombre_cliente
        ]
        
        # Agregar recibo unido
        self.receipts_pending.append(recibo_unido)
        
        return recibo_unido
    
    def crear_datos_ejemplo(self) -> None:
        """
        Crea datos de ejemplo para pruebas.
        
        Incluye productos de ejemplo en las tres familias.
        """
        from models.product import Product
        
        # Bebidas
        bebidas_ejemplo = [
            ("Caña", 1.3),
            ("Jarra de Cerveza", 3.5),
            ("Tinto de verano", 1.8),
            ("Copa de vino", 1.3),
            ("Vermut", 2.5),
            ("Refresco", 1.8),
            ("Café solo", 1.2),
            ("Café con leche", 1.5)
        ]
        
        # Comidas
        comidas_ejemplo = [
            ("Patatas bravas", 6.0),
            ("Croquetas caseras", 7.0),
            ("Jamón ibérico", 10.0),
            ("Tortilla de patatas", 6.0),
            ("Bocadillos", 4.0),
            ("Hamburguesas", 7.0)
        ]
        
        # Otros
        otros_ejemplo = [
            ("Mechero", 1.5),
            ("Navaja", 10.0)
        ]
        
        # Agregar productos
        for nombre, precio in bebidas_ejemplo:
            producto = Product(nombre, precio, "Bebida")
            try:
                self.products.agregar_producto(producto)
            except:
                pass
        
        for nombre, precio in comidas_ejemplo:
            producto = Product(nombre, precio, "Comida")
            try:
                self.products.agregar_producto(producto)
            except:
                pass
        
        for nombre, precio in otros_ejemplo:
            producto = Product(nombre, precio, "Otros")
            try:
                self.products.agregar_producto(producto)
            except:
                pass


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

_data_manager = None


def get_data_manager() -> DataManager:
    """
    Obtiene la instancia global del gestor de datos.
    
    Returns:
        DataManager: Gestor de datos
    """
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'DataManager',
    'get_data_manager'
]