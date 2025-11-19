"""
Script para migrar del sistema de archivos al sistema SQLite ENCRIPTADA.

Este script migra todos los datos existentes a una base de datos SQLite
completamente encriptada e inaccesible desde fuera de la aplicación.

Uso:
    python migrar_a_sqlite_encriptada.py
"""

import sys
from pathlib import Path
from datetime import datetime
import shutil

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from data.data_manager import get_data_manager as get_data_manager_old
from data.database_encrypted import get_database_manager


def main():
    """Función principal de migración."""
    
    print()
    print("=" * 70)
    print("  MIGRACIÓN A SISTEMA SQLite ENCRIPTADA")
    print("  La base de datos será INACCESIBLE desde fuera de la aplicación")
    print("=" * 70)
    print()
    
    # ========================================================================
    # PASO 1: Cargar datos del sistema antiguo
    # ========================================================================
    print("PASO 1: Cargando datos del sistema antiguo...")
    print("-" * 70)
    
    try:
        data_manager_old = get_data_manager_old()
        
        if not data_manager_old.cargar_datos_generales():
            print("⚠ No se encontraron datos previos")
            respuesta = input("¿Desea crear una base de datos nueva? (s/n): ")
            if respuesta.lower() not in ['s', 'si', 'sí']:
                print("Migración cancelada")
                return 1
            
            # Crear datos de ejemplo
            print("Creando datos de ejemplo...")
            data_manager_old.crear_datos_ejemplo()
            data_manager_old.guardar_datos_generales()
        
        print("✓ Datos antiguos cargados correctamente")
        print()
        
        # Mostrar resumen de datos antiguos
        print("Resumen de datos a migrar:")
        print(f"  - Productos: {data_manager_old.products.obtener_numero_productos()}")
        print(f"  - Clientes: {data_manager_old.customers.obtener_numero_clientes()}")
        print(f"  - Camareros: {data_manager_old.waiters.obtener_numero_camareros()}")
        print(f"  - Tickets pendientes: {len(data_manager_old.receipts_pending)}")
        print()
        
    except Exception as e:
        print(f"✗ Error al cargar datos antiguos: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ========================================================================
    # PASO 2: Crear base de datos SQLite ENCRIPTADA
    # ========================================================================
    print("PASO 2: Creando base de datos SQLite ENCRIPTADA...")
    print("-" * 70)
    
    try:
        db = get_database_manager()
        print("✓ Base de datos encriptada creada")
        print("✓ La base de datos NO puede abrirse sin la clave de la aplicación")
        print()
        
    except Exception as e:
        print(f"✗ Error al crear base de datos: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ========================================================================
    # PASO 3: Migrar datos
    # ========================================================================
    print("PASO 3: Migrando datos a la base de datos encriptada...")
    print("-" * 70)
    
    try:
        # Migrar productos
        print("Migrando productos...", end=" ")
        productos = data_manager_old.products.obtener_todos()
        for producto in productos:
            db.guardar_producto(
                producto.nombre,
                producto.precio,
                producto.familia
            )
        print(f"✓ {len(productos)} productos migrados")
        
        # Migrar clientes
        print("Migrando clientes...", end=" ")
        clientes = data_manager_old.customers.obtener_todos()
        for cliente in clientes:
            db.guardar_cliente(cliente)
        print(f"✓ {len(clientes)} clientes migrados")
        
        # Migrar camareros
        print("Migrando camareros...", end=" ")
        camareros = data_manager_old.waiters.obtener_todos()
        for camarero in camareros:
            db.guardar_camarero(camarero)
        print(f"✓ {len(camareros)} camareros migrados")
        
        # Migrar recibos pendientes
        print("Migrando recibos pendientes...", end=" ")
        for recibo in data_manager_old.receipts_pending:
            recibo_data = {
                'fecha': recibo.fecha,
                'cliente_nombre': recibo.nombre,
                'camarero_nombre': recibo.camarero,
                'estado': recibo.estado,
                'subtotal': recibo.calcular_subtotal(),
                'iva_porcentaje': data_manager_old.iva,
                'total': recibo.calcular_total(),
                'impreso': recibo.impreso
            }
            
            lineas = []
            for linea in recibo.pedido:
                lineas.append({
                    'producto_nombre': linea.nombre,
                    'cantidad': linea.cantidad,
                    'precio_unitario': linea.precio,
                    'familia': linea.familia,
                    'subtotal': linea.calcular_total()
                })
            
            db.guardar_recibo(recibo_data, lineas)
        
        print(f"✓ {len(data_manager_old.receipts_pending)} recibos pendientes migrados")
        
        # Migrar recibos anuales (pagados)
        print("Migrando recibos pagados del año actual...", end=" ")
        anio_actual = datetime.now().year
        receipt_manager = data_manager_old.cargar_recibos_anuales(anio_actual)
        
        total_recibos_pagados = 0
        for mes_recibos in receipt_manager._recibos_anuales:
            for recibo in mes_recibos:
                recibo_data = {
                    'fecha': recibo.fecha,
                    'cliente_nombre': recibo.nombre,
                    'camarero_nombre': recibo.camarero,
                    'estado': recibo.estado,
                    'subtotal': recibo.calcular_subtotal(),
                    'iva_porcentaje': data_manager_old.iva,
                    'total': recibo.calcular_total(),
                    'impreso': recibo.impreso
                }
                
                lineas = []
                for linea in recibo.pedido:
                    lineas.append({
                        'producto_nombre': linea.nombre,
                        'cantidad': linea.cantidad,
                        'precio_unitario': linea.precio,
                        'familia': linea.familia,
                        'subtotal': linea.calcular_total()
                    })
                
                db.guardar_recibo(recibo_data, lineas)
                total_recibos_pagados += 1
        
        print(f"✓ {total_recibos_pagados} recibos pagados migrados")
        
        # Migrar configuración
        print("Migrando configuración...", end=" ")
        db.guardar_configuracion('iva', data_manager_old.iva)
        db.guardar_configuracion('password', data_manager_old.password)
        db.guardar_configuracion('impresoras', data_manager_old.printers)
        print("✓ Configuración migrada")
        
        print()
        
    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ========================================================================
    # PASO 4: Verificar migración
    # ========================================================================
    print("PASO 4: Verificando integridad de la migración...")
    print("-" * 70)
    
    try:
        if not db.verificar_integridad():
            print("✗ Error: La base de datos no pasó la verificación de integridad")
            return 1
        
        stats = db.obtener_estadisticas()
        
        print("✓ Base de datos verificada correctamente")
        print()
        print("Estadísticas de la base de datos migrada:")
        print(f"  - Productos activos: {stats['productos_activos']}")
        print(f"  - Clientes: {stats['clientes']}")
        print(f"  - Camareros: {stats['camareros']}")
        
        if 'recibos' in stats:
            for estado, info in stats['recibos'].items():
                print(f"  - Recibos {estado}: {info['cantidad']} (Total: {info['total']:.2f}€)")
        
        print(f"  - Tamaño de DB encriptada: {stats['tamano_db_bytes'] / 1024:.2f} KB")
        print()
        
    except Exception as e:
        print(f"✗ Error en la verificación: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # ========================================================================
    # PASO 5: Crear backup del sistema antiguo
    # ========================================================================
    print("PASO 5: Creando backup del sistema antiguo...")
    print("-" * 70)
    
    try:
        backup_dir = Path('data/backup_sistema_antiguo')
        backup_dir.mkdir(exist_ok=True, parents=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Backup de archivos .tpv
        archivos_backup = []
        if Path('data/data.tpv').exists():
            archivos_backup.append(Path('data/data.tpv'))
        
        archivos_backup.extend(Path('data').glob('anual.*.tpv'))
        
        for archivo in archivos_backup:
            destino = backup_dir / f'{Path(archivo).stem}_{timestamp}.tpv.backup'
            shutil.copy2(archivo, destino)
            print(f"  ✓ {archivo} → {destino.name}")
        
        print()
        print("✓ Backup del sistema antiguo completado")
        print(f"✓ Archivos guardados en: {backup_dir}")
        print()
        
    except Exception as e:
        print(f"⚠ Advertencia: No se pudo crear backup completo: {e}")
        print()
    
    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("=" * 70)
    print("  ✓ MIGRACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("Próximos pasos:")
    print()
    print("1. ✓ Datos migrados a SQLite ENCRIPTADA")
    print("2. ✓ Base de datos INACCESIBLE desde fuera de la aplicación")
    print("3. ✓ Backup del sistema antiguo creado")
    print()
    print("4. ⚠ IMPORTANTE: Ejecute el script de prueba:")
    print("   python test_database_encrypted.py")
    print()
    print("5. Si las pruebas son exitosas, la aplicación usará automáticamente")
    print("   la nueva base de datos encriptada.")
    print()
    print("6. Los archivos antiguos .tpv están respaldados en:")
    print(f"   {backup_dir}")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())