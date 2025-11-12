# 👤 Sistema de Selección de Camarero

## 📋 Descripción

Al iniciar la aplicación, se muestra automáticamente el panel de selección de camareros. El usuario **debe seleccionar un camarero** antes de poder realizar cualquier venta.

---

## 🚀 Flujo de Inicio

### 1. Al Iniciar la Aplicación

```
┌─────────────────────────────────────┐
│  Se carga la aplicación             │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│  ¿Hay camareros configurados?       │
└─────────────┬───────────────────────┘
              │
        ┌─────┴─────┐
        │           │
      SÍ            NO
        │           │
        ▼           ▼
┌───────────┐  ┌──────────────────────┐
│ Mostrar   │  │ Mostrar productos    │
│ panel de  │  │ + mensaje advertencia│
│ camareros │  │                      │
└───────────┘  └──────────────────────┘
```

### 2. Selección de Camarero

**Panel de Camareros muestra:**
- ✅ Botón "GESTIONAR CAMAREROS" (para añadir/eliminar)
- ✅ Lista de todos los camareros disponibles

**Al hacer clic en un camarero:**
1. Se selecciona como camarero actual
2. Se muestra su nombre en la barra superior
3. Se guarda el camarero anterior (si había uno)
4. Se vuelve automáticamente al panel de productos
5. Ya se puede empezar a vender

---

## 🔒 Validaciones Implementadas

### Bloqueo de Ventas sin Camarero

Si se intenta realizar alguna acción sin haber seleccionado camarero:

#### 1. Al hacer clic en un producto
```
❌ Mensaje: "Camarero no seleccionado"
   "Debe seleccionar un camarero antes de realizar ventas.
    Haga clic en el botón de camarero (barman) para seleccionar uno."
```

#### 2. Al usar el teclado numérico (OK)
```
❌ Mensaje: "Camarero no seleccionado"
   "Debe seleccionar un camarero antes de realizar ventas."
```

#### 3. Al finalizar venta (efectivo/tarjeta)
```
❌ Mensaje: "Camarero no seleccionado"
   "Debe seleccionar un camarero antes de finalizar ventas."
```

**Nota:** El botón "guardar" (consultar tickets) NO requiere camarero seleccionado.

---

## 🔄 Cambiar de Camarero Durante el Uso

### Opción 1: Botón de Camarero Actual

En la barra superior hay un botón con el icono de camarero (barman):
1. Hacer clic en el botón
2. Se abre el panel de camareros
3. Seleccionar nuevo camarero
4. Se vuelve automáticamente a ventas

### Opción 2: Marco de Camarero Anterior

Si hay un camarero anterior guardado:
1. Hacer clic en el marco del camarero anterior
2. Se intercambian automáticamente:
   - El actual pasa a ser anterior
   - El anterior pasa a ser actual

---

## 👥 Gestionar Camareros

### Añadir un Nuevo Camarero

1. En el panel de camareros, clic en "GESTIONAR CAMAREROS"
2. Se abre el teclado virtual en modo Camarero
3. Escribir el nombre del nuevo camarero
4. Clic en "Agregar"
5. El camarero se añade a la lista

### Eliminar un Camarero

1. En el panel de camareros, clic en "GESTIONAR CAMAREROS"
2. Se abre el teclado virtual en modo Camarero
3. Seleccionar camarero del listado (o escribir nombre)
4. Clic en "Eliminar"
5. El camarero se elimina

### Ver Tickets de un Camarero

1. En el panel de camareros, clic en "GESTIONAR CAMAREROS"
2. Se abre el teclado virtual en modo Camarero
3. Seleccionar camarero del listado
4. Clic en "Tickets"
5. Se abre el calendario con los tickets del camarero

---

## 💾 Persistencia

### Camarero Actual
- ❌ **NO se guarda** entre sesiones
- ✅ Cada vez que se inicia la app, hay que seleccionar camarero

### Lista de Camareros
- ✅ **SÍ se guarda** en `data/data.tpv`
- ✅ Los camareros configurados persisten entre sesiones

### Camarero en Tickets
- ✅ Cada ticket guarda el nombre del camarero que lo creó
- ✅ Esta información se mantiene para siempre
- ✅ Útil para reportes y auditorías

---

## 🎨 Interfaz

### Barra Superior

```
┌────────────────────────────────────────────────────────┐
│ [Logo] Está atendiendo el camarero:                   │
│        [Nombre del Camarero Actual]                    │
│                                  [Anterior] [👤] [⚡]  │
└────────────────────────────────────────────────────────┘
```

**Elementos:**
- `[Logo]`: Logo de la aplicación
- `Nombre del Camarero Actual`: Nombre en grande
- `[Anterior]`: Marco con camarero anterior (clic para intercambiar)
- `[👤]`: Botón para abrir panel de camareros
- `[⚡]`: Botón de apagar

---

## 🔧 Casos Especiales

### Primera Vez (Sin Camareros Configurados)

Si es la primera vez que se usa la aplicación:

1. No aparece el panel de camareros
2. Se muestra el panel de productos
3. Mensaje en consola: "No hay camareros configurados"
4. Hay que:
   - Clic en botón de camarero
   - Clic en "GESTIONAR CAMAREROS"
   - Añadir camareros
   - Seleccionar uno

### Cambio Rápido de Camarero

Para turnos rápidos entre dos camareros:

1. **Camarero A** trabaja → Seleccionar A
2. **Camarero B** toma el relevo:
   - Clic en botón camarero
   - Seleccionar B
   - A pasa a "Anterior"
3. **Camarero A** vuelve:
   - Clic en marco "Anterior"
   - Se intercambian automáticamente

---

## 📊 Reportes por Camarero

En el calendario se pueden ver tickets por camarero:

1. Abrir calendario (botón "guardar" sin productos)
2. En el botón "comodín", cambiar a modo camarero
3. Seleccionar camarero del dropdown
4. Ver todos sus tickets en el listado

---

## 🐛 Solución de Problemas

### No aparece el panel de camareros al inicio

**Causa:** No hay camareros configurados

**Solución:**
1. Clic en botón de camarero (barman)
2. Clic en "GESTIONAR CAMAREROS"
3. Añadir al menos un camarero
4. Reiniciar la aplicación

### No puedo hacer ventas

**Causa:** No hay camarero seleccionado

**Solución:**
1. Clic en botón de camarero (barman)
2. Seleccionar un camarero de la lista
3. Ya se puede vender

### El camarero no se guarda

**Comportamiento esperado:** El camarero actual NO se guarda entre sesiones por seguridad.

Cada sesión debe empezar con selección de camarero.

---

## ✅ Ventajas del Sistema

1. ✅ **Trazabilidad**: Cada ticket tiene su camarero asignado
2. ✅ **Seguridad**: Obliga a identificarse antes de vender
3. ✅ **Control**: Reportes individuales por camarero
4. ✅ **Auditoría**: Historial completo de quién vendió qué
5. ✅ **Responsabilidad**: Cada camarero es responsable de sus ventas

---

## 📝 Notas Técnicas

### Archivo: `views/main_view.py`

**Cambios implementados:**

1. **Líneas 765-780**: `inicializar_datos()`
   - Muestra panel de camareros al inicio
   - Valida si hay camareros configurados

2. **Líneas 397-408**: `_on_producto_press()`
   - Validación de camarero antes de agregar producto

3. **Líneas 416-438**: `_on_tecla_numerica()`
   - Validación de camarero antes de agregar producto "Varios"

4. **Líneas 454-469**: `_on_boton_pago_release()`
   - Validación de camarero antes de finalizar venta

5. **Líneas 556-570**: `_on_camarero_seleccion_release()`
   - Mensaje de confirmación al seleccionar camarero

---

**¡Sistema de camareros completamente funcional!** 👤✅