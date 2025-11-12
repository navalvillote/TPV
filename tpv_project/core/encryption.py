"""
Sistema de encriptación para datos sensibles de la aplicación TPV.

Este módulo maneja la encriptación y desencriptación de datos
utilizando Fernet (criptografía simétrica).
"""

import pickle
import json
from typing import Any, Union
from cryptography.fernet import Fernet
from config.settings import EncryptionConfig


class EncryptionManager:
    """Gestiona la encriptación y desencriptación de datos."""
    
    def __init__(self, encryption_key: bytes = None):
        """
        Inicializa el gestor de encriptación.
        
        Args:
            encryption_key: Clave de encriptación. Si es None, usa la clave
                          de configuración.
        """
        self.key = encryption_key or EncryptionConfig.ENCRYPTION_KEY
        self.fernet = Fernet(self.key)
    
    def encriptar_objeto(self, objeto: Any) -> bytes:
        """
        Encripta un objeto Python utilizando pickle y Fernet.
        
        Args:
            objeto: Objeto Python a encriptar
            
        Returns:
            bytes: Datos encriptados
            
        Raises:
            Exception: Si hay error en la encriptación
        """
        try:
            # Serializar el objeto con pickle
            datos_serializados = pickle.dumps(objeto)
            # Encriptar los datos
            datos_encriptados = self.fernet.encrypt(datos_serializados)
            return datos_encriptados
        except Exception as e:
            raise Exception(f"Error al encriptar objeto: {str(e)}")
    
    def desencriptar_objeto(self, datos_encriptados: bytes) -> Any:
        """
        Desencripta datos y devuelve el objeto Python original.
        
        Args:
            datos_encriptados: Datos encriptados
            
        Returns:
            Any: Objeto Python desencriptado
            
        Raises:
            Exception: Si hay error en la desencriptación
        """
        try:
            # Desencriptar los datos
            datos_serializados = self.fernet.decrypt(datos_encriptados)
            # Deserializar el objeto
            objeto = pickle.loads(datos_serializados)
            return objeto
        except Exception as e:
            raise Exception(f"Error al desencriptar objeto: {str(e)}")
    
    def encriptar_json(self, datos: Union[dict, list]) -> bytes:
        """
        Encripta datos en formato JSON.
        
        Args:
            datos: Diccionario o lista a encriptar
            
        Returns:
            bytes: Datos encriptados
            
        Raises:
            Exception: Si hay error en la encriptación
        """
        try:
            # Convertir a JSON y codificar
            datos_json = json.dumps(datos).encode('utf-8')
            # Encriptar los datos
            datos_encriptados = self.fernet.encrypt(datos_json)
            return datos_encriptados
        except Exception as e:
            raise Exception(f"Error al encriptar JSON: {str(e)}")
    
    def desencriptar_json(self, datos_encriptados: bytes) -> Union[dict, list]:
        """
        Desencripta datos en formato JSON.
        
        Args:
            datos_encriptados: Datos encriptados
            
        Returns:
            Union[dict, list]: Datos desencriptados
            
        Raises:
            Exception: Si hay error en la desencriptación
        """
        try:
            # Desencriptar los datos
            datos_json = self.fernet.decrypt(datos_encriptados).decode('utf-8')
            # Convertir de JSON a objeto Python
            datos = json.loads(datos_json)
            return datos
        except Exception as e:
            raise Exception(f"Error al desencriptar JSON: {str(e)}")
    
    def guardar_archivo_encriptado(self, ruta: str, datos: Any, 
                                   usar_json: bool = True) -> None:
        """
        Guarda datos encriptados en un archivo.
        
        Args:
            ruta: Ruta del archivo
            datos: Datos a guardar
            usar_json: Si True, usa JSON; si False, usa pickle
            
        Raises:
            Exception: Si hay error al guardar
        """
        try:
            if usar_json:
                datos_encriptados = self.encriptar_json(datos)
            else:
                datos_encriptados = self.encriptar_objeto(datos)
            
            with open(ruta, 'wb') as archivo:
                archivo.write(datos_encriptados)
        except Exception as e:
            raise Exception(f"Error al guardar archivo encriptado: {str(e)}")
    
    def cargar_archivo_encriptado(self, ruta: str, 
                                  usar_json: bool = True) -> Any:
        """
        Carga datos encriptados desde un archivo.
        
        Args:
            ruta: Ruta del archivo
            usar_json: Si True, usa JSON; si False, usa pickle
            
        Returns:
            Any: Datos desencriptados
            
        Raises:
            Exception: Si hay error al cargar
        """
        try:
            with open(ruta, 'rb') as archivo:
                datos_encriptados = archivo.read()
            
            if usar_json:
                return self.desencriptar_json(datos_encriptados)
            else:
                return self.desencriptar_objeto(datos_encriptados)
        except Exception as e:
            raise Exception(f"Error al cargar archivo encriptado: {str(e)}")
    
    @staticmethod
    def generar_nueva_clave() -> bytes:
        """
        Genera una nueva clave de encriptación.
        
        Returns:
            bytes: Nueva clave de encriptación
            
        Note:
            Esta clave debe guardarse de forma segura. Si se pierde,
            no se podrán recuperar los datos encriptados.
        """
        return Fernet.generate_key()


# ============================================================================
# FUNCIONES DE CONVENIENCIA
# ============================================================================

# Instancia global del gestor de encriptación
_encryption_manager = None


def get_encryption_manager() -> EncryptionManager:
    """
    Obtiene la instancia global del gestor de encriptación.
    
    Returns:
        EncryptionManager: Gestor de encriptación
    """
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()
    return _encryption_manager


def encriptar(objeto: Any) -> bytes:
    """
    Función de conveniencia para encriptar un objeto.
    
    Args:
        objeto: Objeto a encriptar
        
    Returns:
        bytes: Datos encriptados
    """
    return get_encryption_manager().encriptar_objeto(objeto)


def desencriptar(datos_encriptados: bytes) -> Any:
    """
    Función de conveniencia para desencriptar datos.
    
    Args:
        datos_encriptados: Datos encriptados
        
    Returns:
        Any: Objeto desencriptado
    """
    return get_encryption_manager().desencriptar_objeto(datos_encriptados)


# ============================================================================
# EXPORTACIÓN
# ============================================================================

__all__ = [
    'EncryptionManager',
    'get_encryption_manager',
    'encriptar',
    'desencriptar'
]