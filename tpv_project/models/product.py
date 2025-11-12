"""
Modelo de datos para Productos.

Este módulo define la estructura y operaciones relacionadas con productos.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from config.settings import ProductConfig
from utils.validators import (
    validar_precio, 
    validar_nombre_producto, 
    validar_familia
)


@dataclass
class Product:
    """Representa un producto del TPV."""
    
    nombre: str
    precio: float
    familia: str
    
    def __post_init__(self):
        """Valida los datos del producto tras la inicialización."""
        if not validar_nombre_producto(self.nombre):
            raise ValueError(f"Nombre de producto inválido: {self.nombre}")
        
        if not validar_precio(str(self.precio)):
            raise ValueError(f"Precio inválido: {self.precio}")
        
        if not validar_familia(self.familia, ProductConfig.FAMILIAS):
            raise ValueError(f"Familia inválida: {self.familia}")
    
    def to_dict(self) -> Dict:
        """
        Convierte el producto a diccionario.
        
        Returns:
            Dict: Diccionario con los datos del producto
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Product':
        """
        Crea un producto desde un diccionario.
        
        Args:
            data: Diccionario con los datos del producto
            
        Returns:
            Product: Instancia de producto
        """
        return cls(
            nombre=data['nombre'],
            precio=float(data['precio']),
            familia=data['familia']
        )
    
    def __str__(self) -> str:
        """Representación en string del producto."""
        return f"{self.nombre} - {self.precio:.2f}€ ({self.familia})"
    
    def __repr__(self) -> str:
        """Representación para debug."""
        return (f"Product(nombre='{self.nombre}', "
                f"precio={self.precio}, familia='{self.familia}')")


class ProductManager:
    """Gestiona la colección de productos."""
    
    def __init__(self):
        """Inicializa el gestor de productos."""
        self._productos: List[Product] = []
    
    def agregar_producto(self, producto: Product) -> None:
        """
        Agrega un nuevo producto.
        
        Args:
            producto: Producto a agregar
            
        Raises:
            ValueError: Si el producto ya existe
        """
        if self.existe_producto(producto.nombre):
            raise ValueError(f"El producto '{producto.nombre}' ya existe")
        
        self._productos.append(producto)
    
    def actualizar_producto(self, nombre: str, precio: Optional[float] = None,
                          familia: Optional[str] = None) -> None:
        """
        Actualiza un producto existente.
        
        Args:
            nombre: Nombre del producto a actualizar
            precio: Nuevo precio (opcional)
            familia: Nueva familia (opcional)
            
        Raises:
            ValueError: Si el producto no existe o los datos son inválidos
        """
        producto = self.obtener_producto(nombre)
        if producto is None:
            raise ValueError(f"Producto '{nombre}' no encontrado")
        
        if precio is not None:
            if not validar_precio(str(precio)):
                raise ValueError(f"Precio inválido: {precio}")
            producto.precio = precio
        
        if familia is not None:
            if not validar_familia(familia, ProductConfig.FAMILIAS):
                raise ValueError(f"Familia inválida: {familia}")
            producto.familia = familia
    
    def eliminar_producto(self, nombre: str) -> bool:
        """
        Elimina un producto.
        
        Args:
            nombre: Nombre del producto a eliminar
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        for i, producto in enumerate(self._productos):
            if producto.nombre == nombre:
                del self._productos[i]
                return True
        return False
    
    def obtener_producto(self, nombre: str) -> Optional[Product]:
        """
        Obtiene un producto por su nombre.
        
        Args:
            nombre: Nombre del producto
            
        Returns:
            Optional[Product]: Producto si existe, None en caso contrario
        """
        for producto in self._productos:
            if producto.nombre == nombre:
                return producto
        return None
    
    def existe_producto(self, nombre: str) -> bool:
        """
        Verifica si existe un producto con el nombre dado.
        
        Args:
            nombre: Nombre del producto
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return self.obtener_producto(nombre) is not None
    
    def obtener_productos_por_familia(self, familia: str) -> List[Product]:
        """
        Obtiene todos los productos de una familia.
        
        Args:
            familia: Familia de productos
            
        Returns:
            List[Product]: Lista de productos de la familia
        """
        return [p for p in self._productos if p.familia == familia]
    
    def obtener_todos(self) -> List[Product]:
        """
        Obtiene todos los productos.
        
        Returns:
            List[Product]: Lista de todos los productos
        """
        return self._productos.copy()
    
    def cargar_productos(self, productos_data: List[Dict]) -> None:
        """
        Carga productos desde una lista de diccionarios.
        
        Args:
            productos_data: Lista de diccionarios con datos de productos
        """
        self._productos.clear()
        for data in productos_data:
            try:
                producto = Product.from_dict(data)
                self._productos.append(producto)
            except Exception as e:
                print(f"Error al cargar producto: {e}")
    
    def exportar_productos(self) -> List[Dict]:
        """
        Exporta todos los productos como lista de diccionarios.
        
        Returns:
            List[Dict]: Lista de diccionarios con datos de productos
        """
        return [p.to_dict() for p in self._productos]
    
    def obtener_numero_productos(self) -> int:
        """
        Obtiene el número total de productos.
        
        Returns:
            int: Número de productos
        """
        return len(self._productos)
    
    def limpiar(self) -> None:
        """Elimina todos los productos."""
        self._productos.clear()


# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

def crear_producto_varios(precio: float) -> Product:
    """
    Crea un producto del tipo "Varios" con un precio específico.
    
    Args:
        precio: Precio del producto
        
    Returns:
        Product: Producto de tipo varios
    """
    return Product(
        nombre='Varios',
        precio=precio,
        familia=ProductConfig.FAMILIA_VARIOS
    )


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'Product',
    'ProductManager',
    'crear_producto_varios'
]