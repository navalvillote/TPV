# 📦 Guía de Instalación Completa - TPV Bar Robledo

Esta guía te llevará paso a paso desde cero hasta tener la aplicación funcionando.

---

## 📋 Requisitos Previos

- **Windows 10/11** (para funcionalidad de impresión)
- **Python 3.8 o superior**
- **Git** (opcional, para clonar el repositorio)
- **Permisos de administrador** (para instalar Python y dependencias)

---

## 🚀 Paso 1: Instalar Python

### Verificar si Python está instalado

Abre CMD o PowerShell y ejecuta:

```bash
python --version
```

Si ves algo como `Python 3.8.x` o superior, ya tienes Python instalado. **Salta al Paso 2**.

### Instalar Python (si no lo tienes)

1. Descarga Python desde: https://www.python.org/downloads/
2. Ejecuta el instalador
3. ✅ **IMPORTANTE**: Marca "Add Python to PATH"
4. Haz clic en "Install Now"
5. Reinicia la terminal

---

## 📁 Paso 2: Crear la Estructura del Proyecto

### Opción A: Crear manualmente

```bash
# Crear directorio principal
mkdir tpv_project
cd tpv_project

# Crear estructura de carpetas
mkdir config core models controllers views data utils
mkdir views\components
```

### Opción B: Script automático

Crea un archivo `crear_estructura.bat` con este contenido:

```batch
@echo off
echo Creando estructura del proyecto TPV...

mkdir config
mkdir core
mkdir models
mkdir controllers
mkdir views
mkdir views\components
mkdir data
mkdir utils
mkdir archivos

echo.
echo Estructura creada exitosamente!
echo.
pause
```

Ejecuta el script haciendo doble clic.

---

## 📄 Paso 3: Copiar los Archivos

Copia cada archivo del artifact correspondiente a su ubicación:

### Archivos de Configuración

```
config/
├── __init__.py          ← Artifact "init_files" sección config
└── settings.py          ← Artifact "config_settings"
```

### Archivos Core

```
core/
├── __init__.py          ← Artifact "init_files" sección core
├── encryption.py        ← Artifact "core_encryption"
└── image_manager.py     ← Artifact "core_image_manager"
```

### Archivos de Modelos

```
models/
├── __init__.py          ← Artifact "init_files" sección models
├── product.py           ← Artifact "models_product"
├── receipt.py           ← Artifact "models_receipt"
└── customer.py          ← Artifact "models_customer_waiter"
```

### Archivos de Controladores

```
controllers/
├── __init__.py          ← Artifact "init_files" sección controllers
├── printer_controller.py← Artifact "controller_printer"
├── calendar_controller.py← Artifact "controller_calendar"
└── receipt_controller.py← Artifact "controller_receipt"
```

### Archivos de Data

```
data/
├── __init__.py          ← Artifact "init_files" sección data
└── data_manager.py      ← Artifact "data_manager"
```

### Archivos de Utilidades

```
utils/
├── __init__.py          ← Artifact "init_files" sección utils
├── formatters.py        ← Artifact "utils_formatters"
└── validators.py        ← Artifact "utils_validators"
```

### Archivos de Vistas

```
views/
├── __init__.py          ← Artifact "init_files" sección views
├── main_view.py         ← Artifact "views_main_view" (versión completa integrada)
├── calendar_view.py     ← Artifact "views_calendar"
├── keyboard_view.py     ← Artifact "views_keyboard_full"
└── components/
    ├── __init__.py      ← Artifact "init_files" sección components
    ├── base_widgets.py  ← Artifact "views_base_widgets"
    ├── keyboard.py      ← Artifact "views_keyboard"
    └── ticket_display.py← Artifact "views_ticket_display"
```

### Archivos Raíz

```
tpv_project/
├── main.py              ← Artifact "main_script" (actualizado)
├── create_images.py     ← Artifact "create_images_script"
├── requirements.txt     ← Artifact "requirements_file"
├── README.md            ← Artifact "readme_file"
├── MIGRATION_GUIDE.md   ← Artifact "migration_guide"
└── RESUMEN_FINAL.md     ← Artifact "final_summary"
```

---

## 🔧 Paso 4: Crear Entorno Virtual

```bash
# En el directorio tpv_project
python -m venv venv
```

### Activar el entorno virtual

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Verás `(venv)` al inicio de tu línea de comandos.

---

## 📦 Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Si hay problemas con pywin32

```bash
pip uninstall pywin32
pip install pywin32
python venv\Scripts\pywin32_postinstall.py -install
```

---

## 🖼️ Paso 6: Preparar las Imágenes

### Opción A: Usar imágenes existentes

Si ya tienes las imágenes del proyecto original:

1. Copia todas las imágenes PNG a la carpeta `archivos/`
2. Ejecuta:

```bash
python create_images.py
```

### Opción B: Crear imágenes de prueba

Si no tienes las imágenes, puedes crear algunas básicas con este script `crear_imagenes_prueba.py`:

```python
from PIL import Image, ImageDraw, ImageFont
import os

# Crear directorio
os.makedirs('archivos', exist_ok=True)

# Crear imágenes básicas
imagenes = [
    'logo', 'apagado', 'barman',
    'tecla', 'tecla_doble', 'tecla_envio', 'tecla_space', 'tecla_marco',
    'tecla_efectivo', 'tecla_tarjeta', 'tecla_guardar',
    'pantalla', 'info', 'textbox'
]

for nombre in imagenes:
    # Crear imagen
    img = Image.new('RGB', (152, 70), color='gray')
    d = ImageDraw.Draw(img)
    
    # Agregar texto
    d.text((10, 25), nombre, fill='white')
    
    # Guardar versión normal
    img.save(f'archivos/{nombre}.png')
    
    # Guardar versión invertida (si aplica)
    if nombre.startswith('tecla'):
        img_inv = Image.new('RGB', (152, 70), color='lightgray')
        d_inv = ImageDraw.Draw(img_inv)
        d_inv.text((10, 25), nombre, fill='black')
        img_inv.save(f'archivos/{nombre}_p.png')

print("Imágenes de prueba creadas!")
```

Ejecuta:
```bash
python crear_imagenes_prueba.py
python create_images.py
```

---

## 🔑 Paso 7: Copiar el Icono

Copia `icono.ico` a la raíz del proyecto:

```
tpv_project/
├── icono.ico    ← Aquí
├── main.py
└── ...
```

Si no tienes el icono, puedes crear uno básico o la aplicación funcionará sin él (mostrará un aviso).

---

## 💾 Paso 8: Migrar Datos Existentes (Opcional)

Si tienes datos del sistema anterior:

```bash
# Crear directorio data si no existe
mkdir data

# Copiar archivos de datos
copy ruta\antigua\data.tpv data\
copy ruta\antigua\anual.*.tpv data\
```

El archivo `image.tpv` debe estar en la raíz (ya se creó en el Paso 6).

---

## ▶️ Paso 9: Ejecutar la Aplicación

```bash
python main.py
```

### Primera Ejecución

La aplicación:
1. Validará la configuración
2. Cargará las imágenes
3. Creará la base de datos con productos de ejemplo
4. Mostrará la interfaz gráfica

### Salida Esperada

```
============================================================
  INICIANDO TPV - BAR ROBLEDO
============================================================

Validando configuración...
✓ Configuración válida

Configurando idioma...
✓ Configuración regional establecida

Cargando imágenes...
✓ Imágenes cargadas: 25

Inicializando datos...
✓ Base de datos creada con productos de ejemplo
  - Productos: 18
  - Clientes: 0
  - Camareros: 0
  - Tickets pendientes: 0

Creando controladores...
✓ Controladores creados
  - Impresoras disponibles: 2

Creando interfaz gráfica...
✓ Interfaz creada correctamente

============================================================
  APLICACIÓN INICIADA - ¡BIENVENIDO!
============================================================

  Presione ESC para salir
```

---

## ✅ Paso 10: Verificar Funcionamiento

### Prueba Básica

1. **Agregar productos al ticket**
   - Haz clic en productos de bebidas/comidas
   - Verifica que aparecen en el ticket

2. **Cambiar entre familias**
   - Clic en "MOSTRAR CONSUMICIONES"
   - Navega entre Bebidas, Comidas, Otros

3. **Teclado numérico**
   - Ingresa un precio
   - Clic en "OK" para agregar producto "Varios"

4. **Finalizar venta**
   - Clic en botón "efectivo" o "tarjeta"
   - Verifica que el ticket se guarda

5. **Gestionar productos**
   - Clic en "GESTIONAR PRODUCTOS"
   - Prueba agregar un producto nuevo

6. **Calendario**
   - Clic en "guardar" sin productos
   - Verifica que se abre el calendario
   - Navega por fechas

---

## 🐛 Solución de Problemas Comunes

### Error: No se encuentra el módulo 'tkinter'

**Windows:**
```bash
# Reinstalar Python marcando "tcl/tk and IDLE"
```

**Linux:**
```bash
sudo apt-get install python3-tk
```

### Error: No se encuentra image.tpv

```bash
# Verificar que existe el directorio archivos con imágenes PNG
dir archivos

# Ejecutar script de creación
python create_images.py
```

### Error: ModuleNotFoundError

```bash
# Verificar que el entorno virtual está activado
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: Permission denied en archivos

```bash
# Ejecutar como administrador o verificar permisos
# Windows: Clic derecho > Ejecutar como administrador
```

### Error de impresión

```bash
# Reinstalar pywin32
pip uninstall pywin32
pip install pywin32
python venv\Scripts\pywin32_postinstall.py -install
```

### La aplicación se ve pixelada en Windows

Agregar al inicio de `main.py`:

```python
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
```

---

## 🎓 Siguientes Pasos

1. **Configurar impresoras**
   - En el calendario, ir a "Asignar Impresoras"
   - Seleccionar impresora principal y de comandas

2. **Agregar productos reales**
   - Eliminar productos de ejemplo
   - Agregar tus productos mediante "GESTIONAR PRODUCTOS"

3. **Configurar camareros**
   - Clic en botón de camarero (barman)
   - Gestionar camareros

4. **Ajustar IVA**
   - En el calendario, usar botones +/- junto a "% de IVA"

5. **Backup inicial**
   - Copiar `data/` a un lugar seguro
   - Configurar backups automáticos

---

## 📚 Documentación Adicional

- **README.md**: Documentación general
- **MIGRATION_GUIDE.md**: Guía de migración desde versión anterior
- **RESUMEN_FINAL.md**: Resumen completo del proyecto

---

## 🆘 Soporte

Si encuentras problemas:

1. Verifica esta guía paso a paso
2. Revisa la sección de solución de problemas
3. Consulta los logs en `data/tpv.log`
4. Revisa el código con los comentarios incluidos

---

## ✨ ¡Felicidades!

Has instalado exitosamente el sistema TPV Bar Robledo refactorizado.

**Características disponibles:**
- ✅ Gestión completa de productos
- ✅ Sistema de tickets y recibos
- ✅ Tickets pendientes de pago
- ✅ Múltiples camareros
- ✅ Calendario con reportes
- ✅ Impresión de tickets
- ✅ Apertura de caja
- ✅ Teclado virtual
- ✅ Datos encriptados
- ✅ Interfaz moderna y funcional

**¡Disfruta de tu nuevo sistema TPV!** 🎉

---

*Última actualización: Noviembre 2024*