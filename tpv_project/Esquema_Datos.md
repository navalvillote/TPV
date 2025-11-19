Por supuesto, te voy a explicar detalladamente todo el esquema de datos de la aplicación TPV.

## Esquema Completo de Datos de la Aplicación TPV

---

## 1. ESTRUCTURA DE ARCHIVOS

La aplicación genera y gestiona los siguientes archivos:

```
tpv_project/
├── data/
│   ├── data.tpv              # Datos generales (productos, clientes, config)
│   ├── anual.2024.tpv        # Recibos del año 2024
│   ├── anual.2025.tpv        # Recibos del año 2025
│   └── anual.XXXX.tpv        # Recibos de cada año
├── image.tpv                 # Imágenes encriptadas
└── icono.ico                 # Icono de la aplicación
```

---

## 2. ARCHIVO: `data.tpv` (Datos Generales)

### Contenido
Este archivo contiene **TODOS** los datos principales de la aplicación:

```python
datos = [
    productos,           # [0] Lista de productos
    recibos_pendientes,  # [1] Tickets sin pagar
    clientes,            # [2] Lista de clientes
    camareros,           # [3] Lista de camareros
    iva,                 # [4] Porcentaje de IVA
    password,            # [5] Contraseña de acceso
    impresoras           # [6] [impresora_principal, impresora_comanda]
]
```

### Estructura Detallada

#### [0] **Productos** - Lista de diccionarios
```python
productos = [
    {
        'nombre': 'Caña',
        'precio': 1.3,
        'familia': 'Bebida'
    },
    {
        'nombre': 'Patatas bravas',
        'precio': 6.0,
        'familia': 'Comida'
    },
    {
        'nombre': 'Mechero',
        'precio': 1.5,
        'familia': 'Otros'
    }
]
```

**Familias permitidas**: 
- `'Bebida'`
- `'Comida'`
- `'Otros'`

#### [1] **Recibos Pendientes** - Lista de diccionarios
```python
recibos_pendientes = [
    {
        'pedido': [
            [2, 'Caña', 1.3, 'Bebida'],      # [cantidad, nombre, precio, familia]
            [1, 'Patatas bravas', 6.0, 'Comida']
        ],
        'nombre': 'Juan Pérez',               # Nombre del cliente
        'fecha': '18/11/2025 - 14:30:25',    # Formato: DD/MM/YYYY - HH:MM:SS
        'estado': 'pendiente',                # 'pendiente', 'efectivo', 'tarjeta', 'Nuevo'
        'impreso': False,                     # Si se imprimió o no
        'camarero': 'María'                   # Nombre del camarero que lo atendió
    }
]
```

#### [2] **Clientes** - Lista de strings
```python
clientes = [
    'Juan Pérez',
    'María García',
    'Pedro López'
]
```

#### [3] **Camareros** - Lista de strings
```python
camareros = [
    'María',
    'Carlos',
    'Ana'
]
```

#### [4] **IVA** - Float
```python
iva = 21.0  # Porcentaje
```

#### [5] **Password** - String
```python
password = ''  # Vacío por defecto, se puede configurar
```

#### [6] **Impresoras** - Lista de strings
```python
impresoras = [
    'HP LaserJet Pro',  # [0] Impresora principal (tickets)
    'Epson TM-T20'      # [1] Impresora de comanda (cocina)
]
```

---

## 3. ARCHIVOS: `anual.XXXX.tpv` (Recibos Anuales)

### Contenido
Contiene **todos los recibos pagados** (efectivo o tarjeta) organizados por mes.

```python
recibos_anuales = [
    recibos_enero,    # [0]  - Lista de recibos de enero
    recibos_febrero,  # [1]  - Lista de recibos de febrero
    recibos_marzo,    # [2]  - Lista de recibos de marzo
    recibos_abril,    # [3]  - Lista de recibos de abril
    recibos_mayo,     # [4]  - Lista de recibos de mayo
    recibos_junio,    # [5]  - Lista de recibos de junio
    recibos_julio,    # [6]  - Lista de recibos de julio
    recibos_agosto,   # [7]  - Lista de recibos de agosto
    recibos_septiembre, # [8] - Lista de recibos de septiembre
    recibos_octubre,  # [9]  - Lista de recibos de octubre
    recibos_noviembre,# [10] - Lista de recibos de noviembre
    recibos_diciembre # [11] - Lista de recibos de diciembre
]
```

### Estructura de cada mes
```python
recibos_enero = [
    {
        'pedido': [
            [3, 'Caña', 1.3, 'Bebida'],
            [2, 'Café solo', 1.2, 'Bebida']
        ],
        'nombre': 'Pagado efectivo',          # 'Pagado efectivo' o 'Pagado tarjeta'
        'fecha': '05/01/2025 - 12:15:30',
        'estado': 'efectivo',                 # 'efectivo' o 'tarjeta'
        'impreso': True,
        'camarero': 'María'
    },
    {
        'pedido': [
            [1, 'Hamburguesas', 7.0, 'Comida']
        ],
        'nombre': 'Pagado tarjeta',
        'fecha': '05/01/2025 - 13:45:10',
        'estado': 'tarjeta',
        'impreso': True,
        'camarero': 'Carlos'
    }
]
```

---

## 4. ARCHIVO: `image.tpv` (Imágenes)

### Contenido
Contiene **todas las imágenes** de la interfaz encriptadas en formato binario.

```python
imagenes = [
    ['logo', bytes_imagen_logo],
    ['tecla', bytes_imagen_tecla],
    ['tecla_p', bytes_imagen_tecla_presionada],
    ['pantalla', bytes_imagen_pantalla],
    ['tecla_marco', bytes_imagen_marco],
    ['tecla_doble', bytes_imagen_doble],
    # ... más imágenes
]
```

### Convención de nombres
- Imagen normal: `'tecla'`
- Imagen invertida: `'tecla_p'` (sufijo `_p` = presionada)

---

## 5. SISTEMA DE ENCRIPTACIÓN

### Método: Fernet (Criptografía Simétrica)

```python
from cryptography.fernet import Fernet

# Clave de encriptación (definida en config/settings.py)
ENCRYPTION_KEY = b'5-uvWBhTHRAk7Eq8wlzdnXZlLCZFj8rE44rUN49wztg='
```

### Proceso de Encriptación

```
Datos Python → JSON/Pickle → Encriptar → Escribir archivo .tpv
```

### Proceso de Desencriptación

```
Leer archivo .tpv → Desencriptar → JSON/Pickle → Datos Python
```

---

## 6. FLUJO DE CARGA DE DATOS (INICIO DE APLICACIÓN)

### Paso 1: Inicialización (`main.py`)
```python
def main():
    # 1. Cargar imágenes
    image_manager = get_image_manager()
    image_manager.cargar_imagenes_desde_archivo()  # Lee image.tpv
    
    # 2. Cargar datos generales
    data_manager = get_data_manager()
    data_manager.cargar_datos_generales()  # Lee data.tpv
    
    # 3. Cargar recibos del año actual
    receipt_manager = data_manager.cargar_recibos_anuales()  # Lee anual.2025.tpv
```

### Paso 2: Carga de `data.tpv` (`data/data_manager.py`)
```python
def cargar_datos_generales(self) -> bool:
    # 1. Verificar si existe el archivo
    if not os.path.exists(DATA_FILE):
        # Si no existe, crear con datos vacíos
        self.guardar_datos_generales()
        return False
    
    # 2. Desencriptar y cargar
    datos = self._encryption.cargar_archivo_encriptado(
        str(DATA_FILE),
        usar_json=True  # Usa JSON para datos estructurados
    )
    
    # 3. Parsear datos
    if datos and len(datos) >= 7:
        self.products.cargar_productos(datos[0])           # Productos
        self.receipts_pending = [                          # Recibos pendientes
            Receipt.from_dict(r) for r in datos[1]
        ]
        self.customers.cargar_clientes(datos[2])           # Clientes
        self.waiters.cargar_camareros(datos[3])            # Camareros
        self.iva = datos[4]                                # IVA
        self.password = datos[5]                           # Password
        self.printers = datos[6]                           # Impresoras
        
        return True
    
    return False
```

### Paso 3: Carga de `anual.XXXX.tpv` (`data/data_manager.py`)
```python
def cargar_recibos_anuales(self, anio: int = None) -> ReceiptManager:
    if anio is None:
        anio = datetime.now().year  # Año actual (ej: 2025)
    
    archivo = DATA_DIR / f'anual.{anio}.tpv'
    manager = ReceiptManager()
    
    if os.path.exists(archivo):
        # Desencriptar archivo
        datos = self._encryption.cargar_archivo_encriptado(
            str(archivo),
            usar_json=True
        )
        # Cargar recibos por mes
        manager.cargar_recibos_anuales(datos)  # datos = [mes1, mes2, ..., mes12]
    
    return manager
```

### Paso 4: Carga de `image.tpv` (`core/image_manager.py`)
```python
def cargar_imagenes_desde_archivo(self, ruta_archivo: str = None) -> None:
    ruta = ruta_archivo or str(IMAGES_FILE)
    
    # Cargar y desencriptar
    datos_lista = self._encryption.cargar_archivo_encriptado(
        ruta, 
        usar_json=False  # Usa pickle para datos binarios
    )
    
    # Procesar cada imagen
    self._imagenes.clear()
    for nombre, imagen_binaria in datos_lista:
        imagen = Image.open(io.BytesIO(imagen_binaria))  # PIL Image
        imagen.filename = nombre
        self._imagenes[nombre] = imagen
```

---

## 7. FLUJO DE GUARDADO DE DATOS

### Momento 1: Guardar Producto Nuevo/Modificado
```python
# Usuario guarda producto desde KeyboardView
def _guardar_producto(nombre, precio, familia):
    # 1. Crear/actualizar producto
    producto = Product(nombre, precio, familia)
    data_manager.products.agregar_producto(producto)
    
    # 2. Guardar TODO el archivo data.tpv
    data_manager.guardar_datos_generales()
```

### Momento 2: Pagar Ticket (Efectivo/Tarjeta)
```python
# Usuario paga un ticket
def _pagar_efectivo():
    # 1. Si es ticket pendiente, eliminar de pendientes
    if recibo_actual.estado == 'pendiente':
        data_manager.eliminar_recibo_pendiente(recibo_actual.fecha)
    
    # 2. Marcar como pagado
    receipt_controller.finalizar_recibo_efectivo(camarero_actual)
    
    # 3. Agregar al gestor de recibos anuales
    mes = datetime.now().month
    receipt_manager.agregar_recibo(recibo, mes)
    
    # 4. Guardar recibos anuales
    data_manager.guardar_recibos_anuales(receipt_manager)  # Guarda anual.2025.tpv
    
    # 5. Guardar datos generales (actualiza pendientes)
    data_manager.guardar_datos_generales()  # Guarda data.tpv
```

### Momento 3: Guardar Ticket Pendiente
```python
# Usuario guarda ticket como pendiente
def _guardar_ticket_pendiente(nombre_cliente):
    # 1. Marcar recibo como pendiente
    recibo.marcar_como_pendiente(nombre_cliente, camarero_actual)
    
    # 2. Agregar a lista de pendientes
    data_manager.agregar_recibo_pendiente(recibo)
    
    # 3. Agregar cliente si no existe
    if not data_manager.customers.existe_cliente(nombre_cliente):
        data_manager.customers.agregar_cliente(nombre_cliente)
    
    # 4. Guardar datos generales
    data_manager.guardar_datos_generales()  # Guarda data.tpv
```

### Momento 4: Unir Tickets de Cliente
```python
# Usuario une tickets de un cliente
def _unir_tickets_callback(nombre_cliente):
    # 1. Unir todos los tickets
    recibo_unido = data_manager.unir_recibos_pendientes(nombre_cliente)
    # Internamente:
    # - Elimina todos los tickets sueltos del cliente
    # - Crea un nuevo ticket con todas las líneas fusionadas
    
    # 2. Guardar cambios
    data_manager.guardar_datos_generales()  # Guarda data.tpv
```

### Momento 5: Salir de la Aplicación
```python
# Usuario cierra la aplicación
def _salir():
    # Guardar todos los datos pendientes
    data_manager.guardar_datos_generales()
    data_manager.guardar_recibos_anuales(receipt_manager)
```

---

## 8. MÉTODOS DE GUARDADO

### `guardar_datos_generales()` en `data/data_manager.py`
```python
def guardar_datos_generales(self) -> None:
    # 1. Preparar datos
    datos = [
        self.products.exportar_productos(),              # [0]
        [r.to_dict() for r in self.receipts_pending],   # [1]
        self.customers.exportar_clientes(),              # [2]
        self.waiters.exportar_camareros(),               # [3]
        self.iva,                                        # [4]
        self.password,                                   # [5]
        self.printers                                    # [6]
    ]
    
    # 2. Encriptar y guardar
    self._encryption.guardar_archivo_encriptado(
        str(DATA_FILE),
        datos,
        usar_json=True
    )
```

### `guardar_recibos_anuales()` en `data/data_manager.py`
```python
def guardar_recibos_anuales(self, recibos_manager: ReceiptManager, anio: int = None) -> None:
    if anio is None:
        anio = datetime.now().year
    
    archivo = DATA_DIR / f'anual.{anio}.tpv'
    
    # 1. Exportar recibos por mes
    datos = recibos_manager.exportar_recibos_anuales()
    # datos = [[recibos_enero], [recibos_febrero], ..., [recibos_diciembre]]
    
    # 2. Encriptar y guardar
    self._encryption.guardar_archivo_encriptado(
        str(archivo),
        datos,
        usar_json=True
    )
```

---

## 9. CONVERSIÓN DE OBJETOS

### De Objeto a Diccionario (`to_dict`)
```python
# Clase Receipt
def to_dict(self) -> Dict:
    return {
        'pedido': [linea.to_list() for linea in self.pedido],
        'nombre': self.nombre,
        'fecha': self.fecha,
        'estado': self.estado,
        'impreso': self.impreso,
        'camarero': self.camarero
    }

# Clase LineaRecibo
def to_list(self) -> List:
    return [self.cantidad, self.nombre, self.precio, self.familia]

# Clase Product
def to_dict(self) -> Dict:
    return {
        'nombre': self.nombre,
        'precio': self.precio,
        'familia': self.familia
    }
```

### De Diccionario a Objeto (`from_dict`)
```python
# Clase Receipt
@classmethod
def from_dict(cls, data: Dict) -> 'Receipt':
    pedido = [LineaRecibo.from_list(linea) for linea in data['pedido']]
    
    return cls(
        pedido=pedido,
        nombre=data['nombre'],
        fecha=data['fecha'],
        estado=data['estado'],
        impreso=data['impreso'],
        camarero=data.get('camarero', '')
    )

# Clase LineaRecibo
@classmethod
def from_list(cls, data: List) -> 'LineaRecibo':
    return cls(
        cantidad=data[0],
        nombre=data[1],
        precio=float(data[2]),
        familia=data[3]
    )

# Clase Product
@classmethod
def from_dict(cls, data: Dict) -> 'Product':
    return cls(
        nombre=data['nombre'],
        precio=float(data['precio']),
        familia=data['familia']
    )
```

---

## 10. DIAGRAMA DE FLUJO COMPLETO

```
INICIO DE APLICACIÓN
├── Cargar image.tpv
│   └── ImageManager.cargar_imagenes_desde_archivo()
│       └── Desencriptar → Cargar en memoria como PIL.Image
│
├── Cargar data.tpv
│   └── DataManager.cargar_datos_generales()
│       ├── Desencriptar
│       ├── Parsear JSON
│       └── Crear objetos:
│           ├── Product (productos)
│           ├── Receipt (tickets pendientes)
│           ├── str (clientes)
│           ├── str (camareros)
│           ├── float (IVA)
│           ├── str (password)
│           └── List[str] (impresoras)
│
└── Cargar anual.2025.tpv
    └── DataManager.cargar_recibos_anuales(2025)
        ├── Desencriptar
        ├── Parsear JSON
        └── Crear objetos Receipt organizados por mes

OPERACIÓN DE USUARIO
├── Crear/Modificar Producto
│   └── guardar_datos_generales() → Actualiza data.tpv
│
├── Guardar Ticket Pendiente
│   └── guardar_datos_generales() → Actualiza data.tpv
│
├── Pagar Ticket
│   ├── guardar_recibos_anuales() → Actualiza anual.2025.tpv
│   └── guardar_datos_generales() → Actualiza data.tpv
│
├── Unir Tickets
│   └── guardar_datos_generales() → Actualiza data.tpv
│
└── Agregar/Eliminar Cliente/Camarero
    └── guardar_datos_generales() → Actualiza data.tpv

CIERRE DE APLICACIÓN
├── guardar_datos_generales() → Guarda data.tpv
└── guardar_recibos_anuales() → Guarda anual.2025.tpv
```

---

## 11. RESUMEN DE PERSISTENCIA

| Dato | Archivo | Formato | Cuándo se Guarda |
|------|---------|---------|------------------|
| Productos | `data.tpv` | JSON encriptado | Al crear/modificar/eliminar producto |
| Clientes | `data.tpv` | JSON encriptado | Al agregar/eliminar cliente |
| Camareros | `data.tpv` | JSON encriptado | Al agregar/eliminar camarero |
| Tickets Pendientes | `data.tpv` | JSON encriptado | Al guardar/unir/pagar ticket |
| IVA | `data.tpv` | JSON encriptado | Al cambiar configuración |
| Password | `data.tpv` | JSON encriptado | Al cambiar configuración |
| Impresoras | `data.tpv` | JSON encriptado | Al cambiar configuración |
| Tickets Pagados | `anual.XXXX.tpv` | JSON encriptado | Al pagar ticket (efectivo/tarjeta) |
| Imágenes UI | `image.tpv` | Pickle encriptado | Solo al ejecutar `create_images.py` |

---

¿Necesitas que profundice en alguna parte específica del esquema de datos?