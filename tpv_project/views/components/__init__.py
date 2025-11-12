# ============================================================================
# views/components/__init__.py
# ============================================================================
"""
Paquete de componentes de interfaz.
"""

from .base_widgets import (
    BasePanel,
    BaseLabel,
    ImageLabel,
    MarcoConImagen,
    ListaConScroll
)

from .keyboard import (
    TecladoVirtual,
    TecladoNumerico,
    GestorEntradaTexto
)

from .ticket_display import (
    TicketDisplay,
    PantallaNumerico,
    EtiquetaInfo
)

__all__ = [
    'BasePanel',
    'BaseLabel',
    'ImageLabel',
    'MarcoConImagen',
    'ListaConScroll',
    'TecladoVirtual',
    'TecladoNumerico',
    'GestorEntradaTexto',
    'TicketDisplay',
    'PantallaNumerico',
    'EtiquetaInfo'
]