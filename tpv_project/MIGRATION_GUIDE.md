# Guía de Migración desde Mi_TPV.py

Este documento explica cómo migrar desde el código original (`Mi_TPV.py`) a la nueva estructura refactorizada.

## 📋 Resumen de Cambios

### Estructura del Proyecto

**Antes** (Mi_TPV.py):
- Todo el código en un solo archivo (~2500 líneas)
- Variables globales
- Funciones sueltas
- Sin separación clara de responsabilidades

**Ahora**:
- Código organizado en módulos por funcionalidad
- Arquitectura MVC (Model-View-Controller)
- Clases bien definidas
- Separación de responsabilidades

### Mapeo de Componentes

| Código Original | Nueva Ubicación | Descripción |
|----------------|-----------------|-------------|
| `class Ventanas` | `views/main_view.py` → `MainWindow` | Ventana principal |
| `class Paneles` | `views/components/base_widgets.py` → `BasePanel` | Paneles base |
| `class Marcos` | `views/components/base_widgets.py` → `MarcoConImagen` | Marcos con imagen |
| `class Botones` | `views/components/base_widgets.py` → `ImageLabel` | Botones con imagen |
| `class Tickets` | `views/components/ticket_display.py` → `TicketDisplay` | Display de tickets |
| Funciones de formato | `utils/formatters.py` | Formateo de texto/números |
| Funciones de validación | `utils/validators.py` | Validaciones |
| Gestión de productos | `models/product.py` | Modelo de productos |
| Gestión de recibos | `models/receipt.py` | Modelo de recibos |
| Gestión de clientes | `models/customer.py` | Modelo de clientes |
| Gestión de camareros | `models/customer.py` → `WaiterManager` | Modelo de camareros |
| Encriptación | `core/encryption.py` | Sistema de encriptación |
| Imágenes | `core/image_manager.py` | Gestión de imágenes |
| Impresión | `controllers/printer_controller.py` | Controlador de impresión |
| Calendario | `controllers/calendar_controller.py` | Controlador de calendario |
| Persistencia | `data/data_manager.py` | Gestión de datos |

## 🔄 Migración de Datos

### Compatibilidad

La nueva estructura es **100% compatible** con los archivos de datos existentes:
- `data.tpv` → Se puede leer directamente
- `anual.YYYY.tpv` → Se puede leer directamente
- `image.tpv` → Se puede leer directamente

### Pasos para Migrar Datos

1. **Hacer backup** de los datos actuales:
   ```bash
   mkdir backup
   cp data.tpv backup/
   cp anual.*.tpv backup/
   cp image.tpv backup/
   ```

2. **Copiar archivos** a la nueva estructura:
   ```bash
   # Crear directorio data
   mkdir data
   
   # Copiar datos
   cp data.tpv data/
   cp anual.*.tpv data/
   
   # Copiar imágenes (ya está en raíz)
   # image.tpv debe estar en la raíz del proyecto
   ```

3. **Verificar** que los archivos se cargan correctamente:
   ```bash
   python main.py
   ```

### Formato de Datos

Los datos siguen el mismo formato encriptado, por lo que no se requiere conversión.

## 🔧 Cambios en la API Interna

### Variables Globales Eliminadas

Las variables globales se han movido a clases gestoras:

```python
# ANTES (Mi_TPV.py)
lista_productos = []
lista_recibos_mensuales = []
lista_clientes = []
diccionario_recibo = {'pedido': []}
impuesto_iva = 21

# AHORA
data_manager = get_data_manager()
data_manager.products  # ProductManager
data_manager.customers  # CustomerManager
data_manager.iva  # float
receipt_controller.obtener_recibo_actual()  # Receipt
```

### Funciones Principales

#### Gestión de Productos

```python
# ANTES
def guardar_producto():
    # Lógica mezclada con UI
    lista_productos.append(prdt)
    guardar_datos()

# AHORA
# En el controlador o gestor
data_manager.products.agregar_producto(producto)
data_manager.guardar_datos_generales()
```

#### Gestión de Recibos

```python
# ANTES
def completar_pedido(consumicion):
    # Lógica compleja mezclada
    diccionario_recibo['pedido'].append(lista)

# AHORA
receipt_controller.agregar_producto(nombre_producto, cantidad)
```

#### Finalizar Venta

```python
# ANTES
# Código directo en el evento
diccionario_recibo['nombre'] = f'Pagado {metodo}'
lista_recibos_mensuales.append(diccionario_recibo)

# AHORA
receipt_controller.finalizar_recibo_efectivo(camarero)
# o
receipt_controller.finalizar_recibo_tarjeta(camarero)
```

## 🎨 Cambios en la Interfaz

### Creación de Widgets

```python
# ANTES (Mi_TPV.py)
pantalla = numericos.crear_marco(' ', 'Pantalla', 'pantalla', 26, fondo)
pantalla.colocar_objeto(0, 0)

# AHORA
from views.components.ticket_display import PantallaNumerico
pantalla = PantallaNumerico(parent, color_fondo)
pantalla.colocar(0, 0)
```

### Manejo de Eventos

```python
# ANTES
def on_click_tecla(event):
    event.widget.invertir_colores()
    crear_importe(event.widget.title)

# AHORA
# Los componentes tienen callbacks configurables
teclado.vincular_callback(self._on_tecla_numerica)

def _on_tecla_numerica(self, tecla: str):
    # Lógica separada de la UI
    self.receipt_controller.procesar_tecla(tecla)
```

## 🔍 Mejoras de Código

### Type Hints

```python
# ANTES
def formatear_numero(tecla, numero):
    # ...

# AHORA
def formatear_numero_moneda(tecla: str, numero: str) -> str:
    """
    Formatea un número como moneda.
    
    Args:
        tecla: Tecla pulsada
        numero: Número actual
        
    Returns:
        str: Número formateado
    """
    # ...
```

### Manejo de Errores

```python
# ANTES
def cargar_datos():
    listas = cargar_datos_encriptados()
    lista_productos = listas[0]

# AHORA
def cargar_datos_generales(self) -> bool:
    """Carga datos con manejo de errores."""
    try:
        if not os.path.exists(DATA_FILE):
            self.guardar_datos_generales()
            return False
        
        datos = self._encryption.cargar_archivo_encriptado(...)
        # Procesamiento...
        return True
        
    except Exception as e:
        raise Exception(f"Error al cargar datos: {str(e)}")
```

## 📝 Funcionalidades Pendientes

Algunas funcionalidades del código original aún no están completamente implementadas en la refactorización:

### Completamente Implementado ✅
- Gestión de productos
- Gestión de recibos
- Encriptación de datos
- Gestión de imágenes
- Impresión básica
- Calendario y reportes
- Teclado numérico

### Parcialmente Implementado ⚠️
- Teclado virtual completo (estructura creada, falta integración completa)
- Panel de tickets pendientes (modelo completo, vista simplificada)
- Gestión de camareros (modelo completo, UI simplificada)
- Panel de calendario (controlador completo, vista pendiente)

### Por Implementar 🔜
- Vista completa del calendario
- Vista del teclado virtual
- Modo gestión de productos en UI
- Modo gestión de camareros en UI
- Sistema de password completo
- Generador automático de tickets de prueba

## 🚀 Próximos Pasos

1. **Completar vistas pendientes**:
   - `views/calendar_view.py`
   - `views/keyboard_view.py`

2. **Integrar componentes**:
   - Conectar teclado virtual con modos
   - Completar panel de pendientes
   - Implementar cambio de camareros

3. **Testing**:
   - Crear tests unitarios
   - Probar todas las funcionalidades
   - Validar migración de datos

4. **Optimización**:
   - Mejorar rendimiento
   - Reducir uso de memoria
   - Optimizar carga de imágenes

## 💡 Consejos para Desarrolladores

### Extender Funcionalidad

Para añadir nueva funcionalidad:

1. **Modelo** (si es necesario):
   ```python
   # models/nuevo_modelo.py
   class NuevoModelo:
       def __init__(self):
           pass
   ```

2. **Controlador**:
   ```python
   # controllers/nuevo_controller.py
   class NuevoController:
       def __init__(self, data_manager):
           self.data_manager = data_manager
   ```

3. **Vista/Componente**:
   ```python
   # views/components/nuevo_componente.py
   class NuevoComponente(BasePanel):
       def __init__(self, parent):
           super().__init__(parent, ...)
   ```

4. **Integrar** en `main.py` o la vista correspondiente

### Debugging

La nueva estructura facilita el debugging:

```python
# Activar logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Los errores son más específicos
try:
    data_manager.cargar_datos_generales()
except Exception as e:
    print(f"Error específico: {e}")
    import traceback
    traceback.print_exc()
```

## 📞 Soporte

Para dudas sobre la migración:
1. Revisar esta guía
2. Consultar el código con comentarios
3. Revisar ejemplos en `main.py`
4. Contactar al desarrollador

## ✅ Checklist de Migración

- [ ] Backup de datos actuales
- [ ] Instalación de dependencias
- [ ] Creación de `image.tpv`
- [ ] Copia de archivos de datos
- [ ] Verificación de carga de datos
- [ ] Prueba de funcionalidad básica
- [ ] Verificación de impresión
- [ ] Prueba de productos
- [ ] Prueba de recibos
- [ ] Revisión de reportes
- [ ] Backup de la nueva instalación

---

**Última actualización**: Noviembre 2024