"""
Gestor de persistencia de datos (VERSIÓN SQLite ENCRIPTADA).

Este módulo mantiene compatibilidad total con el código existente
pero usa SQLite encriptada internamente.
"""

import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path

from data.database_encrypted import get_database_manager
from models.product import Product, ProductManager
from models.receipt import Receipt, ReceiptManager, LineaRecibo
from models.customer import CustomerManager, WaiterManager
from config.settings import TicketConfig


class DataManagerSQLite:
    """Gestiona la persistencia usando SQLite ENCRIPTADA."""
    
    def __init__(self):
        """Inicializa el gestor de datos."""
        self.db = get_database_manager()
        
        # Gestores (mantienen compatibilidad con el código existente)
        self.products = ProductManagerSQLite(self.db)
        self.customers = CustomerManagerSQLite(self.db)
        self.waiters = WaiterManagerSQLite(self.db)
        
        # Recibos pendientes (cargados en memoria para compatibilidad)
        self.receipts_pending = []
        
        # Configuración
        self.iva = self.db.obtener_configuracion('iva', TicketConfig.DEFAULT_IVA)
        self.password = self.db.obtener_configuracion('password', '')
        self.printers = self.db.obtener_configuracion('impresoras', ['', ''])
    
    def cargar_datos_generales(self) -> bool:
        """
        Carga los datos generales desde la base de datos encriptada.
        
        Returns:
            bool: True si se cargaron datos
        """
        try:
            # Cargar recibos pendientes
            recibos_db = self.db.obtener_recibos(estado='pendiente')
            self.receipts_pending = []
            
            for recibo_db in recibos_db:
                # Convertir de formato DB a Receipt
                pedido = []
                for linea in recibo_db['lineas']:
                    pedido.append(LineaRecibo(
                        cantidad=linea['cantidad'],
                        nombre=linea['producto_nombre'],
                        precio=linea['precio_unitario'],
                        familia=linea['familia']
                    ))
                
                recibo = Receipt(
                    pedido=pedido,
                    nombre=recibo_db.get('cliente_nombre', 'Cliente'),
                    fecha=recibo_db['fecha'],
                    estado=recibo_db['estado'],
                    impreso=recibo_db['impreso'],
                    camarero=recibo_db.get('camarero_nombre', '')
                )
                
                # Guardar ID de base de datos
                recibo.db_id = recibo_db['id']
                
                self.receipts_pending.append(recibo)
            
            return True
            
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            return False
    
    def guardar_datos_generales(self) -> None:
        """Guarda los datos generales en la base de datos encriptada."""
        try:
            # Guardar configuración
            self.db.guardar_configuracion('iva', self.iva)
            self.db.guardar_configuracion('password', self.password)
            self.db.guardar_configuracion('impresoras', self.printers)
            
            # Crear backup cada 6 horas
            hora_actual = datetime.now().hour
            if hora_actual % 6 == 0:
                self.db.crear_backup()
            
        except Exception as e:
            raise Exception(f"Error al guardar datos generales: {str(e)}")
    
    def agregar_recibo_pendiente(self, recibo: Receipt) -> None:
        """Agrega un recibo a la lista de pendientes Y a la BD encriptada."""
        # Agregar a memoria
        self.receipts_pending.append(recibo)
        
        # Guardar en base de datos encriptada
        recibo_data = {
            'fecha': recibo.fecha,
            'cliente_nombre': recibo.nombre,
            'camarero_nombre': recibo.camarero,
            'estado': recibo.estado,
            'subtotal': recibo.calcular_subtotal(),
            'iva_porcentaje': self.iva,
            'total': recibo.calcular_total(),
            'impreso': recibo.impreso
        }
        
        lineas = []
        for linea in recibo.pedido:
            lineas.append({
                'producto_nombre': linea.nombre,
                'cantidad': linea.cantidad,
                'precio_unitario': linea.precio,
                'familia': linea.familia,
                'subtotal': linea.calcular_total()
            })
        
        recibo_id = self.db.guardar_recibo(recibo_data, lineas)
        recibo.db_id = recibo_id
    
    def eliminar_recibo_pendiente(self, fecha: str) -> bool:
        """Elimina un recibo pendiente por su fecha."""
        for i, recibo in enumerate(self.receipts_pending):
            if recibo.fecha == fecha:
                # Eliminar de base de datos
                if hasattr(recibo, 'db_id'):
                    self
                if hasattr(recibo, 'db_id'):
                    self.db.eliminar_recibo(recibo.db_id, usuario='sistema')
                
                # Eliminar de memoria
                del self.receipts_pending[i]
                return True
        return False
    def guardar_recibos_anuales(self, recibos_manager: ReceiptManager,
                                anio: int = None) -> None:
        """
        Guarda los recibos anuales en la base de datos encriptada.
        Los recibos ya se guardan en tiempo real, este método es para compatibilidad.
        """
        # No hacer nada, los recibos ya están guardados en tiempo real
        pass
    
    def cargar_recibos_anuales(self, anio: int = None) -> ReceiptManager:
        """Carga los recibos anuales desde la base de datos encriptada."""
        if anio is None:
            anio = datetime.now().year
        
        manager = ReceiptManager()
        
        try:
            # Obtener recibos del año (pagados)
            fecha_inicio = f'01/01/{anio}'
            fecha_fin = f'31/12/{anio}'
            
            recibos_db = self.db.obtener_recibos(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin
            )
            
            # Filtrar solo pagados
            recibos_pagados = [r for r in recibos_db if r['estado'] in ['efectivo', 'tarjeta']]
            
            # Agrupar por mes y convertir a Receipt
            for recibo_db in recibos_pagados:
                # Extraer mes de la fecha
                fecha_str = recibo_db['fecha']
                mes = int(fecha_str.split('/')[1])
                
                # Convertir a Receipt
                pedido = []
                for linea in recibo_db['lineas']:
                    pedido.append(LineaRecibo(
                        cantidad=linea['cantidad'],
                        nombre=linea['producto_nombre'],
                        precio=linea['precio_unitario'],
                        familia=linea['familia']
                    ))
                
                recibo = Receipt(
                    pedido=pedido,
                    nombre=recibo_db.get('cliente_nombre', f"Pagado {recibo_db['estado']}"),
                    fecha=recibo_db['fecha'],
                    estado=recibo_db['estado'],
                    impreso=recibo_db['impreso'],
                    camarero=recibo_db.get('camarero_nombre', '')
                )
                
                manager.agregar_recibo(recibo, mes)
            
            return manager
            
        except Exception as e:
            print(f"Error al cargar recibos anuales: {e}")
            return manager
    
    def obtener_recibo_pendiente(self, fecha: str) -> Optional[Receipt]:
        """Obtiene un recibo pendiente por su fecha."""
        for recibo in self.receipts_pending:
            if recibo.fecha == fecha:
                return recibo
        return None
    
    def obtener_recibos_pendientes_cliente(self, nombre_cliente: str) -> List[Receipt]:
        """Obtiene todos los recibos pendientes de un cliente."""
        return [
            r for r in self.receipts_pending 
            if r.nombre == nombre_cliente
        ]
    
    def cliente_tiene_pendientes(self, nombre_cliente: str) -> bool:
        """Verifica si un cliente tiene recibos pendientes."""
        return any(r.nombre == nombre_cliente for r in self.receipts_pending)
    
    def unir_recibos_pendientes(self, nombre_cliente: str) -> Optional[Receipt]:
        """Une todos los recibos pendientes de un cliente en uno solo."""
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
        
        # Eliminar recibos antiguos de BD
        for recibo in recibos_cliente:
            if hasattr(recibo, 'db_id'):
                self.db.eliminar_recibo(recibo.db_id, usuario='sistema')
        
        # Eliminar de memoria
        self.receipts_pending = [
            r for r in self.receipts_pending 
            if r.nombre != nombre_cliente
        ]
        
        # Agregar recibo unido
        self.agregar_recibo_pendiente(recibo_unido)
        
        return recibo_unido
    
    def crear_datos_ejemplo(self) -> None:
        """Crea datos de ejemplo para pruebas."""
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
# GESTORES ESPECIALIZADOS (Wrappers sobre SQLite)
# ============================================================================

class ProductManagerSQLite:
    """Gestor de productos usando SQLite encriptada."""
    
    def __init__(self, db):
        self.db = db
    
    def agregar_producto(self, producto: Product) -> None:
        """Agrega o actualiza un producto."""
        self.db.guardar_producto(
            producto.nombre,
            producto.precio,
            producto.familia
        )
    
    def actualizar_producto(self, nombre: str, precio: Optional[float] = None,
                          familia: Optional[str] = None) -> None:
        """Actualiza un producto."""
        productos = self.db.obtener_productos()
        for p in productos:
            if p['nombre'] == nombre:
                nuevo_precio = precio if precio is not None else p['precio']
                nueva_familia = familia if familia is not None else p['familia']
                self.db.guardar_producto(nombre, nuevo_precio, nueva_familia)
                return
        
        raise ValueError(f"Producto '{nombre}' no encontrado")
    
    def eliminar_producto(self, nombre: str) -> bool:
        """Elimina un producto (soft delete)."""
        return self.db.eliminar_producto(nombre)
    
    def obtener_producto(self, nombre: str) -> Optional[Product]:
        """Obtiene un producto por su nombre."""
        productos = self.db.obtener_productos()
        for p in productos:
            if p['nombre'] == nombre:
                return Product(
                    nombre=p['nombre'],
                    precio=p['precio'],
                    familia=p['familia']
                )
        return None
    
    def existe_producto(self, nombre: str) -> bool:
        """Verifica si existe un producto."""
        return self.obtener_producto(nombre) is not None
    
    def obtener_productos_por_familia(self, familia: str) -> List[Product]:
        """Obtiene productos de una familia."""
        productos_db = self.db.obtener_productos(familia=familia)
        return [
            Product(p['nombre'], p['precio'], p['familia'])
            for p in productos_db
        ]
    
    def obtener_todos(self) -> List[Product]:
        """Obtiene todos los productos activos."""
        productos_db = self.db.obtener_productos()
        return [
            Product(p['nombre'], p['precio'], p['familia'])
            for p in productos_db
        ]
    
    def obtener_numero_productos(self) -> int:
        """Obtiene el número total de productos."""
        return len(self.db.obtener_productos())
    
    def exportar_productos(self) -> List[Dict]:
        """Exporta productos (para compatibilidad)."""
        return self.db.obtener_productos()
    
    def cargar_productos(self, productos_data: List[Dict]) -> None:
        """Carga productos (para compatibilidad)."""
        for data in productos_data:
            try:
                self.db.guardar_producto(
                    data['nombre'],
                    data['precio'],
                    data['familia']
                )
            except Exception as e:
                print(f"Error al cargar producto: {e}")
    
    def limpiar(self) -> None:
        """Limpia todos los productos (marca como inactivos)."""
        productos = self.db.obtener_productos()
        for p in productos:
            self.db.eliminar_producto(p['nombre'])


class CustomerManagerSQLite:
    """Gestor de clientes usando SQLite encriptada."""
    
    def __init__(self, db):
        self.db = db
    
    def agregar_cliente(self, nombre: str) -> None:
        """Agrega un nuevo cliente."""
        self.db.guardar_cliente(nombre)
    
    def eliminar_cliente(self, nombre: str) -> bool:
        """Elimina un cliente (soft delete)."""
        return self.db.eliminar_cliente(nombre)
    
    def existe_cliente(self, nombre: str) -> bool:
        """Verifica si existe un cliente."""
        clientes = self.db.obtener_clientes()
        return nombre in clientes
    
    def obtener_todos(self) -> List[str]:
        """Obtiene todos los clientes activos."""
        return self.db.obtener_clientes()
    
    def obtener_numero_clientes(self) -> int:
        """Obtiene el número total de clientes."""
        return len(self.obtener_todos())
    
    def exportar_clientes(self) -> List[str]:
        """Exporta clientes (para compatibilidad)."""
        return self.obtener_todos()
    
    def cargar_clientes(self, clientes: List[str]) -> None:
        """Carga clientes (para compatibilidad)."""
        for cliente in clientes:
            try:
                if not self.existe_cliente(cliente):
                    self.agregar_cliente(cliente)
            except:
                pass
    
    def limpiar(self) -> None:
        """Limpia todos los clientes."""
        clientes = self.obtener_todos()
        for cliente in clientes:
            self.eliminar_cliente(cliente)


class WaiterManagerSQLite:
    """Gestor de camareros usando SQLite encriptada."""
    
    def __init__(self, db):
        self.db = db
    
    def agregar_camarero(self, nombre: str) -> None:
        """Agrega un nuevo camarero."""
        self.db.guardar_camarero(nombre)
    
    def eliminar_camarero(self, nombre: str) -> bool:
        """Elimina un camarero (soft delete)."""
        return self.db.eliminar_camarero(nombre)
    
    def existe_camarero(self, nombre: str) -> bool:
        """Verifica si existe un camarero."""
        camareros = self.db.obtener_camareros()
        return nombre in camareros
    
    def obtener_todos(self) -> List[str]:
        """Obtiene todos los camareros activos."""
        return self.db.obtener_camareros()
    
    def obtener_numero_camareros(self) -> int:
        """Obtiene el número total de camareros."""
        return len(self.obtener_todos())
    
    def exportar_camareros(self) -> List[str]:
        """Exporta camareros (para compatibilidad)."""
        return self.obtener_todos()
    
    def cargar_camareros(self, camareros: List[str]) -> None:
        """Carga camareros (para compatibilidad)."""
        for camarero in camareros:
            try:
                if not self.existe_camarero(camarero):
                    self.agregar_camarero(camarero)
            except:
                pass
    
    def limpiar(self) -> None:
        """Limpia todos los camareros."""
        camareros = self.obtener_todos()
        for camarero in camareros:
            self.eliminar_camarero(camarero)


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

_data_manager_sqlite = None


def get_data_manager_sqlite() -> DataManagerSQLite:
    """Obtiene la instancia global del gestor de datos SQLite."""
    global _data_manager_sqlite
    if _data_manager_sqlite is None:
        _data_manager_sqlite = DataManagerSQLite()
    return _data_manager_sqlite


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'DataManagerSQLite',
    'get_data_manager_sqlite'
]