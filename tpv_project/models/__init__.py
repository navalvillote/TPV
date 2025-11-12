# ============================================================================
# models/__init__.py
# ============================================================================
"""
Paquete de modelos de datos.
"""

from .product import Product, ProductManager, crear_producto_varios
from .receipt import LineaRecibo, Receipt, ReceiptManager
from .customer import CustomerManager, WaiterManager

__all__ = [
    'Product',
    'ProductManager',
    'crear_producto_varios',
    'LineaRecibo',
    'Receipt',
    'ReceiptManager',
    'CustomerManager',
    'WaiterManager'
]