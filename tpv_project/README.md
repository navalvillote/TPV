# TPV - Terminal Punto de Venta

Sistema de punto de venta (TPV) para bares y restaurantes desarrollado en Python con interfaz gráfica Tkinter.

## 🚀 Características

- **Gestión de productos**: Organización por familias (Bebidas, Comidas, Otros)
- **Tickets y recibos**: Sistema completo de generación y gestión de tickets
- **Múltiples formas de pago**: Efectivo y tarjeta
- **Tickets pendientes**: Gestión de cuentas pendientes por cliente
- **Gestión de camareros**: Control de tickets por empleado
- **Reportes y estadísticas**: Informes diarios, mensuales y por método de pago
- **Calendario integrado**: Consulta de ventas por fecha
- **Impresión de tickets**: Integración con impresoras térmicas
- **Apertura de caja**: Control automático de caja registradora
- **Teclado virtual**: Entrada de datos sin teclado físico
- **Datos encriptados**: Seguridad en el almacenamiento de información

## 📋 Requisitos

- Python 3.8 o superior
- Windows (para funcionalidad de impresión)
- Impresora térmica (opcional)

## 🔧 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/tu-usuario/tpv-bar-robledo.git
cd tpv-bar-robledo
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv
```

Activar el entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Preparar las imágenes

1. Crear directorio `archivos/` en la raíz del proyecto
2. Colocar todas las imágenes PNG necesarias en ese directorio
3. Ejecutar el script de creación de imágenes:

```bash
python create_images.py
```

### 5. Colocar el icono

Copiar el archivo `icono.ico` a la raíz del proyecto.

## 🎯 Uso

### Iniciar la aplicación

```bash
python main.py
```

### Primera ejecución

En la primera ejecución, la aplicación:
- Creará automáticamente la base de datos (`data.tpv`)
- Generará productos de ejemplo
- Creará la estructura de directorios necesaria

### Operación básica

1. **Seleccionar camarero** (si está configurado)
2. **Agregar productos** al ticket haciendo clic en ellos
3. **Finalizar venta**:
   - Efectivo: Abre caja registradora automáticamente
   - Tarjeta: Registra el pago
   - Guardar: Guarda como ticket pendiente

### Gestión de productos

1. Clic en "GESTIONAR PRODUCTOS"
2. Agregar, modificar o eliminar productos
3. Organizar por familias

### Consultar ventas

1. Acceder al calendario
2. Seleccionar fecha
3. Ver tickets del día
4. Generar reportes

## 📁 Estructura del Proyecto

```
tpv_project/
├── config/                 # Configuración
│   ├── __init__.py
│   └── settings.py
├── core/                   # Núcleo del sistema
│   ├── __init__.py
│   ├── encryption.py
│   └── image_manager.py
├── models/                 # Modelos de datos
│   ├── __init__.py
│   ├── product.py
│   ├── receipt.py
│   └── customer.py
├── controllers/            # Lógica de negocio
│   ├── __init__.py
│   ├── printer_controller.py
│   ├── calendar_controller.py
│   └── receipt_controller.py
├── views/                  # Interfaz gráfica
│   ├── __init__.py
│   ├── main_view.py
│   └── components/
│       ├── __init__.py
│       ├── base_widgets.py
│       ├── keyboard.py
│       └── ticket_display.py
├── data/                   # Gestión de datos
│   ├── __init__.py
│   └── data_manager.py
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── formatters.py
│   └── validators.py
├── main.py                 # Punto de entrada
├── create_images.py        # Script creación imágenes
├── requirements.txt        # Dependencias
└── README.md              # Esta documentación
```

## 🔒 Seguridad

### Encriptación

Todos los datos sensibles se almacenan encriptados:
- `data.tpv`: Datos generales (productos, clientes, etc.)
- `anual.YYYY.tpv`: Recibos por año
- `image.tpv`: Imágenes encriptadas

### Contraseñas

- El sistema incluye protección con contraseña
- Código de administrador para funciones especiales
- Las contraseñas se almacenan encriptadas

**IMPORTANTE**: En producción, cambiar la clave de encriptación en `config/settings.py` y almacenarla de forma segura.

## 📊 Base de Datos

### Archivos generados

- `data/data.tpv`: Datos principales
- `data/anual.YYYY.tpv`: Recibos del año YYYY
- `data/tpv.log`: Archivo de logs

### Backup

Se recomienda hacer copias de seguridad periódicas de:
- `data/data.tpv`
- `data/anual.*.tpv`

## 🖨️ Configuración de Impresoras

1. Conectar impresora térmica compatible ESC/POS
2. Instalar drivers de la impresora
3. En la aplicación:
   - Ir a "Asignar Impresoras"
   - Seleccionar impresora principal
   - Seleccionar impresora de comandas (opcional)

## 🛠️ Mantenimiento

### Actualizar imágenes

Para actualizar una imagen específica:

```bash
python create_images.py nombre_imagen ruta/a/nueva_imagen.png
```

### Limpiar datos de prueba

Eliminar los archivos `.tpv` del directorio `data/`.

### Generar datos de prueba

La aplicación incluye un generador de datos aleatorios (comentado en el código original).

## 🐛 Solución de Problemas

### Error al cargar imágenes

```
Error: Archivo de imágenes no encontrado
```

**Solución**: Ejecutar `python create_images.py`

### Error de impresión

```
Error al imprimir ticket
```

**Solución**: 
- Verificar que la impresora está conectada
- Comprobar que los drivers están instalados
- Verificar que el nombre de la impresora es correcto

### Error de base de datos

```
Error al cargar datos generales
```

**Solución**: 
- Verificar permisos de escritura en `data/`
- Eliminar `data.tpv` para regenerar

## 📝 Personalización

### Cambiar cabecera del ticket

Editar `config/settings.py`:

```python
class TicketConfig:
    HEADER = 'Tu Negocio - Nombre'
```

### Cambiar IVA predeterminado

```python
class TicketConfig:
    DEFAULT_IVA = 21.0  # Cambiar al valor deseado
```

### Ajustar colores

Modificar `config/settings.py` en la clase `ColorScheme`.

## 👥 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Fork del proyecto
2. Crear una rama para tu función
3. Commit de tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia privada. Contactar con el autor para más información.

## 👤 Autor

Proyecto desarrollado para Bar Robledo.

## 📞 Soporte

Para soporte o consultas, contactar a través de:
- Email: [tu-email]
- Teléfono: [tu-teléfono]

## 🔄 Versión

**Versión actual**: 2.0.0 (Refactorizada)

### Changelog

#### v2.0.0 (2024)
- Refactorización completa del código
- Arquitectura MVC
- Separación de responsabilidades
- Mejor organización de archivos
- Documentación mejorada
- Type hints
- Manejo de errores robusto

#### v1.0.0 (2024)
- Versión inicial
- Funcionalidades básicas de TPV

---

**¡Gracias por usar TPV Bar Robledo!** 🍺