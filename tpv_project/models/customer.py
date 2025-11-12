"""
Modelos de datos para Clientes y Camareros.

Este archivo contiene ambos modelos por su simplicidad.
"""

from typing import List
from utils.validators import validar_nombre_cliente


# ============================================================================
# MODELO DE CLIENTE
# ============================================================================

class CustomerManager:
    """Gestiona la lista de clientes."""
    
    def __init__(self):
        """Inicializa el gestor de clientes."""
        self._clientes: List[str] = []
    
    def agregar_cliente(self, nombre: str) -> None:
        """
        Agrega un nuevo cliente.
        
        Args:
            nombre: Nombre del cliente
            
        Raises:
            ValueError: Si el nombre es inválido o el cliente ya existe
        """
        if not validar_nombre_cliente(nombre):
            raise ValueError(f"Nombre de cliente inválido: {nombre}")
        
        if self.existe_cliente(nombre):
            raise ValueError(f"El cliente '{nombre}' ya existe")
        
        self._clientes.append(nombre)
    
    def eliminar_cliente(self, nombre: str) -> bool:
        """
        Elimina un cliente.
        
        Args:
            nombre: Nombre del cliente
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if nombre in self._clientes:
            self._clientes.remove(nombre)
            return True
        return False
    
    def existe_cliente(self, nombre: str) -> bool:
        """
        Verifica si existe un cliente.
        
        Args:
            nombre: Nombre del cliente
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return nombre in self._clientes
    
    def obtener_todos(self) -> List[str]:
        """
        Obtiene todos los clientes.
        
        Returns:
            List[str]: Lista de nombres de clientes
        """
        return self._clientes.copy()
    
    def cargar_clientes(self, clientes: List[str]) -> None:
        """
        Carga clientes desde una lista.
        
        Args:
            clientes: Lista de nombres de clientes
        """
        self._clientes = clientes.copy()
    
    def exportar_clientes(self) -> List[str]:
        """
        Exporta la lista de clientes.
        
        Returns:
            List[str]: Lista de nombres de clientes
        """
        return self._clientes.copy()
    
    def obtener_numero_clientes(self) -> int:
        """
        Obtiene el número total de clientes.
        
        Returns:
            int: Número de clientes
        """
        return len(self._clientes)
    
    def limpiar(self) -> None:
        """Elimina todos los clientes."""
        self._clientes.clear()


# ============================================================================
# MODELO DE CAMARERO
# ============================================================================

class WaiterManager:
    """Gestiona la lista de camareros."""
    
    def __init__(self):
        """Inicializa el gestor de camareros."""
        self._camareros: List[str] = []
    
    def agregar_camarero(self, nombre: str) -> None:
        """
        Agrega un nuevo camarero.
        
        Args:
            nombre: Nombre del camarero
            
        Raises:
            ValueError: Si el nombre es inválido o el camarero ya existe
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("Nombre de camarero inválido")
        
        if self.existe_camarero(nombre):
            raise ValueError(f"El camarero '{nombre}' ya existe")
        
        self._camareros.append(nombre)
    
    def eliminar_camarero(self, nombre: str) -> bool:
        """
        Elimina un camarero.
        
        Args:
            nombre: Nombre del camarero
            
        Returns:
            bool: True si se eliminó, False si no existía
        """
        if nombre in self._camareros:
            self._camareros.remove(nombre)
            return True
        return False
    
    def existe_camarero(self, nombre: str) -> bool:
        """
        Verifica si existe un camarero.
        
        Args:
            nombre: Nombre del camarero
            
        Returns:
            bool: True si existe, False en caso contrario
        """
        return nombre in self._camareros
    
    def obtener_todos(self) -> List[str]:
        """
        Obtiene todos los camareros.
        
        Returns:
            List[str]: Lista de nombres de camareros
        """
        return self._camareros.copy()
    
    def cargar_camareros(self, camareros: List[str]) -> None:
        """
        Carga camareros desde una lista.
        
        Args:
            camareros: Lista de nombres de camareros
        """
        self._camareros = camareros.copy()
    
    def exportar_camareros(self) -> List[str]:
        """
        Exporta la lista de camareros.
        
        Returns:
            List[str]: Lista de nombres de camareros
        """
        return self._camareros.copy()
    
    def obtener_numero_camareros(self) -> int:
        """
        Obtiene el número total de camareros.
        
        Returns:
            int: Número de camareros
        """
        return len(self._camareros)
    
    def limpiar(self) -> None:
        """Elimina todos los camareros."""
        self._camareros.clear()


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'CustomerManager',
    'WaiterManager'
]