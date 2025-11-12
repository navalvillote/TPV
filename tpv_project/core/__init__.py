# ============================================================================
# core/__init__.py
# ============================================================================
"""
Paquete core con funcionalidades fundamentales.
"""

from .encryption import EncryptionManager, get_encryption_manager
from .image_manager import ImageManager, get_image_manager

__all__ = [
    'EncryptionManager',
    'get_encryption_manager',
    'ImageManager',
    'get_image_manager'
]