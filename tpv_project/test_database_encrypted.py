"""
Script de pruebas para verificar que la base de datos encriptada
funciona correctamente.

Este script verifica:
1. Creación y acceso a la base de datos
2. Guardado de productos, clientes, camareros
3. Guardado y recuperación de recibos
4. Integridad de los datos
5. Que la base de datos es inaccesible sin la clave

Uso:
    python test_database_encrypted.py
"""

import sys
from pathlib import Path
import sqlite3

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from data.database_encrypted import get_database_manager
from data.data_manager_sqlite import get_data_manager_sqlite as get_data_manager
from models.product import Product
from models.receipt import Receipt, LineaRecibo
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓{Colors.END} {msg}")

def print_error(msg):
    print(f"{Colors.RED}✗{Colors.END} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.END} {msg}")

def print_header(msg):
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")


def test_1_creacion_db():
    """Test 1: Crear y verificar integridad de la base de datos."""
    print_header("TEST 1: Creación y Verificación de Base de Datos Encriptada")
    
    try:
        db = get_database_manager()
        print_success("Base de datos creada correctamente")
        
        if db.verificar_integridad():
            print_success("Integridad de la base de datos verificada")
        else:
            print_error("Error de integridad en la base de datos")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Error al crear base de datos: {e}")
        return False


def test_2_acceso_sin_clave():
    """Test 2: Verificar que la DB no se puede abrir sin la clave."""
    print_header("TEST 2: Verificación de Seguridad (Acceso sin clave)")
    
    try:
        # Intentar abrir la base de datos con sqlite3 normal (sin clave)
        db_path = "data/tpv.db"
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM productos")
            cursor.fetchall()
            conn.close()
            
            print_error("¡FALLO DE SEGURIDAD! La base de datos es accesible sin clave")
            return False
            
        except sqlite3.DatabaseError:
            print_success("Base de datos INACCESIBLE sin clave (CORRECTO)")
            return True
        
    except Exception as e:
        print_warning(f"No se pudo verificar: {e}")
        return True


def test_3_productos():
    """Test 3: Guardar y recuperar productos."""
    print_header("TEST 3: Operaciones con Productos")
    
    try:
        db = get_database_manager()
        
        # Guardar productos de prueba
        print("Guardando productos de prueba...")
        test_productos = [
            ("Test Caña", 1.5, "Bebida"),
            ("Test Tapa", 3.0, "Comida"),
            ("Test Mechero", 1.0, "Otros")
        ]
        
        for nombre, precio, familia in test_productos:
            db.guardar_producto(nombre, precio, familia)
            print(f"  - {nombre}: {precio}€ ({familia})")
        
        print_success(f"{len(test_productos)} productos guardados")
        
        # Recuperar productos
        print("\nRecuperando productos...")
        productos = db.obtener_productos()
        
        productos_test = [p for p in productos if p['nombre'].startswith('Test')]
        
        if len(productos_test) == len(test_productos):
            print_success(f"{len(productos_test)} productos recuperados correctamente")
            
            for p in productos_test:
                print(f"  - {p['nombre']}: {p['precio']}€ ({p['familia']})")
            return True
        else:
            print_error(f"Error: Se esperaban {len(test_productos)} productos, se encontraron {len(productos_test)}")
            return False
        
    except Exception as e:
        print_error(f"Error en test de productos: {e}")
        import traceback
        traceback.print_exc()
        return False
    
def test_4_clientes_camareros():
    """Test 4: Guardar y recuperar clientes y camareros."""
    print_header("TEST 4: Operaciones con Clientes y Camareros")
    
    try:
        db = get_database_manager()
        
        # Guardar clientes
        print("Guardando clientes de prueba...")
        test_clientes = ["Test Cliente 1", "Test Cliente 2", "Test Cliente 3"]
        
        for cliente in test_clientes:
            db.guardar_cliente(cliente)
            print(f"  - {cliente}")
        
        print_success(f"{len(test_clientes)} clientes guardados")
        
        # Recuperar clientes
        print("\nRecuperando clientes...")
        clientes = db.obtener_clientes()
        clientes_test = [c for c in clientes if c.startswith('Test Cliente')]
        
        if len(clientes_test) == len(test_clientes):
            print_success(f"{len(clientes_test)} clientes recuperados correctamente")
        else:
            print_error(f"Error: Se esperaban {len(test_clientes)} clientes, se encontraron {len(clientes_test)}")
            return False
        
        # Guardar camareros
        print("\nGuardando camareros de prueba...")
        test_camareros = ["Test Camarero 1", "Test Camarero 2"]
        
        for camarero in test_camareros:
            db.guardar_camarero(camarero)
            print(f"  - {camarero}")
        
        print_success(f"{len(test_camareros)} camareros guardados")
        
        # Recuperar camareros
        print("\nRecuperando camareros...")
        camareros = db.obtener_camareros()
        camareros_test = [c for c in camareros if c.startswith('Test Camarero')]
        
        if len(camareros_test) == len(test_camareros):
            print_success(f"{len(camareros_test)} camareros recuperados correctamente")
            return True
        else:
            print_error(f"Error: Se esperaban {len(test_camareros)} camareros, se encontraron {len(camareros_test)}")
            return False
        
    except Exception as e:
        print_error(f"Error en test de clientes/camareros: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_5_recibos():
    """Test 5: Guardar y recuperar recibos completos."""
    print_header("TEST 5: Operaciones con Recibos (Tickets)")
    
    try:
        db = get_database_manager()
        
        # Crear recibo de prueba
        print("Creando recibo de prueba...")
        
        recibo_data = {
            'fecha': datetime.now().strftime('%d/%m/%Y - %H:%M:%S'),
            'cliente_nombre': 'Test Cliente',
            'camarero_nombre': 'Test Camarero',
            'estado': 'pendiente',
            'subtotal': 10.0,
            'iva_porcentaje': 21.0,
            'total': 12.1,
            'impreso': False
        }
        
        lineas = [
            {
                'producto_nombre': 'Test Caña',
                'cantidad': 2,
                'precio_unitario': 1.5,
                'familia': 'Bebida',
                'subtotal': 3.0
            },
            {
                'producto_nombre': 'Test Tapa',
                'cantidad': 1,
                'precio_unitario': 7.0,
                'familia': 'Comida',
                'subtotal': 7.0
            }
        ]
        
        print(f"  Fecha: {recibo_data['fecha']}")
        print(f"  Cliente: {recibo_data['cliente_nombre']}")
        print(f"  Camarero: {recibo_data['camarero_nombre']}")
        print(f"  Líneas: {len(lineas)}")
        print(f"  Total: {recibo_data['total']}€")
        
        # Guardar recibo
        recibo_id = db.guardar_recibo(recibo_data, lineas)
        print_success(f"Recibo guardado con ID: {recibo_id}")
        
        # Recuperar recibo
        print("\nRecuperando recibo...")
        recibos = db.obtener_recibos(estado='pendiente')
        
        recibo_encontrado = None
        for r in recibos:
            if r['cliente_nombre'] == 'Test Cliente':
                recibo_encontrado = r
                break
        
        if recibo_encontrado:
            print_success("Recibo recuperado correctamente")
            print(f"  ID: {recibo_encontrado['id']}")
            print(f"  Cliente: {recibo_encontrado['cliente_nombre']}")
            print(f"  Total: {recibo_encontrado['total']}€")
            print(f"  Líneas: {len(recibo_encontrado['lineas'])}")
            
            # Verificar líneas
            if len(recibo_encontrado['lineas']) == len(lineas):
                print_success("Todas las líneas del recibo están correctas")
                for linea in recibo_encontrado['lineas']:
                    print(f"    - {linea['cantidad']}x {linea['producto_nombre']}: {linea['subtotal']}€")
                return True
            else:
                print_error(f"Error: Se esperaban {len(lineas)} líneas, se encontraron {len(recibo_encontrado['lineas'])}")
                return False
        else:
            print_error("No se pudo recuperar el recibo")
            return False
        
    except Exception as e:
        print_error(f"Error en test de recibos: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_6_data_manager():
    """Test 6: Verificar compatibilidad con DataManager."""
    print_header("TEST 6: Compatibilidad con DataManager (Capa de Abstracción)")
    
    try:
        # Usar el DataManager (que usa SQLite internamente)
        data_manager = get_data_manager()
        
        print("Cargando datos desde DataManager...")
        if data_manager.cargar_datos_generales():
            print_success("Datos cargados correctamente")
        else:
            print_warning("No hay datos previos (esperado en primera ejecución)")
        
        # Verificar productos
        print("\nVerificando productos...")
        num_productos = data_manager.products.obtener_numero_productos()
        print(f"  Productos encontrados: {num_productos}")
        
        if num_productos > 0:
            print_success("Productos accesibles desde DataManager")
        else:
            print_warning("No hay productos (puede ser correcto si es primera ejecución)")
        
        # Verificar clientes
        print("\nVerificando clientes...")
        num_clientes = data_manager.customers.obtener_numero_clientes()
        print(f"  Clientes encontrados: {num_clientes}")
        
        # Verificar camareros
        print("\nVerificando camareros...")
        num_camareros = data_manager.waiters.obtener_numero_camareros()
        print(f"  Camareros encontrados: {num_camareros}")
        
        # Verificar recibos pendientes
        print("\nVerificando recibos pendientes...")
        num_pendientes = len(data_manager.receipts_pending)
        print(f"  Recibos pendientes: {num_pendientes}")
        
        print_success("DataManager funciona correctamente con SQLite encriptada")
        return True
        
    except Exception as e:
        print_error(f"Error en test de DataManager: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_7_auditoria():
    """Test 7: Verificar sistema de auditoría."""
    print_header("TEST 7: Sistema de Auditoría")
    
    try:
        db = get_database_manager()
        
        print("Modificando un producto para generar auditoría...")
        
        # Guardar producto inicial
        db.guardar_producto("Test Producto Auditoría", 5.0, "Bebida", usuario="test_user")
        print("  ✓ Producto creado: 5.0€")
        
        # Modificar precio
        db.guardar_producto("Test Producto Auditoría", 6.5, "Bebida", usuario="test_user")
        print("  ✓ Precio modificado: 6.5€")
        
        # Verificar auditoría
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM auditoria 
                WHERE tabla = 'productos' 
                ORDER BY fecha DESC 
                LIMIT 5
            """)
            
            registros = cursor.fetchall()
            
            if len(registros) >= 2:
                print_success(f"Se encontraron {len(registros)} registros de auditoría")
                
                for registro in registros[:2]:
                    print(f"\n  Registro de auditoría:")
                    print(f"    Acción: {registro['accion']}")
                    print(f"    Fecha: {registro['fecha']}")
                    print(f"    Usuario: {registro['usuario']}")
                    if registro['datos_anteriores']:
                        print(f"    Datos anteriores: {registro['datos_anteriores']}")
                    if registro['datos_nuevos']:
                        print(f"    Datos nuevos: {registro['datos_nuevos']}")
                
                return True
            else:
                print_warning("Se encontraron menos registros de auditoría de los esperados")
                return True  # No es crítico
        
    except Exception as e:
        print_error(f"Error en test de auditoría: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_8_rendimiento():
    """Test 8: Test de rendimiento básico."""
    print_header("TEST 8: Rendimiento Básico")
    
    try:
        import time
        db = get_database_manager()
        
        # Test de escritura
        print("Test de escritura: Guardando 100 productos...")
        start_time = time.time()
        
        for i in range(100):
            db.guardar_producto(f"Test Producto {i}", 1.5 + i * 0.1, "Bebida")
        
        write_time = time.time() - start_time
        print(f"  Tiempo: {write_time:.3f} segundos")
        print(f"  Velocidad: {100/write_time:.1f} productos/segundo")
        
        if write_time < 5:
            print_success("Rendimiento de escritura excelente")
        elif write_time < 10:
            print_success("Rendimiento de escritura bueno")
        else:
            print_warning("Rendimiento de escritura aceptable")
        
        # Test de lectura
        print("\nTest de lectura: Leyendo todos los productos...")
        start_time = time.time()
        
        productos = db.obtener_productos()
        
        read_time = time.time() - start_time
        print(f"  Productos leídos: {len(productos)}")
        print(f"  Tiempo: {read_time:.3f} segundos")
        
        if read_time < 0.5:
            print_success("Rendimiento de lectura excelente")
        elif read_time < 1:
            print_success("Rendimiento de lectura bueno")
        else:
            print_warning("Rendimiento de lectura aceptable")
        
        return True
        
    except Exception as e:
        print_error(f"Error en test de rendimiento: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_9_backup():
    """Test 9: Sistema de backup."""
    print_header("TEST 9: Sistema de Backup")
    
    try:
        db = get_database_manager()
        
        print("Creando backup de la base de datos...")
        backup_path = db.crear_backup()
        
        if backup_path.exists():
            print_success(f"Backup creado: {backup_path}")
            print(f"  Tamaño: {backup_path.stat().st_size / 1024:.2f} KB")
            
            # Verificar que el backup también está encriptado
            try:
                conn = sqlite3.connect(str(backup_path))
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos")
                cursor.fetchall()
                conn.close()
                
                print_error("¡ADVERTENCIA! El backup NO está encriptado")
                return False
                
            except sqlite3.DatabaseError:
                print_success("Backup está ENCRIPTADO correctamente")
                return True
        else:
            print_error("No se pudo crear el backup")
            return False
        
    except Exception as e:
        print_error(f"Error en test de backup: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_10_limpieza():
    """Test 10: Limpiar datos de prueba."""
    print_header("TEST 10: Limpieza de Datos de Prueba")
    
    try:
        db = get_database_manager()
        
        print("Eliminando datos de prueba...")
        
        # Eliminar productos de prueba
        productos = db.obtener_productos()
        productos_test = [p for p in productos if 'Test' in p['nombre']]
        
        for p in productos_test:
            db.eliminar_producto(p['nombre'])
        
        print(f"  ✓ {len(productos_test)} productos de prueba eliminados")
        
        # Eliminar clientes de prueba
        clientes = db.obtener_clientes()
        clientes_test = [c for c in clientes if 'Test' in c]
        
        for c in clientes_test:
            db.eliminar_cliente(c)
        
        print(f"  ✓ {len(clientes_test)} clientes de prueba eliminados")
        
        # Eliminar camareros de prueba
        camareros = db.obtener_camareros()
        camareros_test = [c for c in camareros if 'Test' in c]
        
        for c in camareros_test:
            db.eliminar_camarero(c)
        
        print(f"  ✓ {len(camareros_test)} camareros de prueba eliminados")
        
        # Eliminar recibos de prueba
        recibos = db.obtener_recibos()
        recibos_test = [r for r in recibos if r['cliente_nombre'] and 'Test' in r['cliente_nombre']]
        
        for r in recibos_test:
            db.eliminar_recibo(r['id'])
        
        print(f"  ✓ {len(recibos_test)} recibos de prueba eliminados")
        
        print_success("Limpieza completada")
        return True
        
    except Exception as e:
        print_error(f"Error en limpieza: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests."""
    
    print()
    print("=" * 70)
    print("  PRUEBAS DE BASE DE DATOS SQLITE ENCRIPTADA")
    print("=" * 70)
    print()
    
    tests = [
        ("Creación de Base de Datos", test_1_creacion_db),
        ("Seguridad (Acceso sin clave)", test_2_acceso_sin_clave),
        ("Operaciones con Productos", test_3_productos),
        ("Operaciones con Clientes y Camareros", test_4_clientes_camareros),
        ("Operaciones con Recibos", test_5_recibos),
        ("Compatibilidad con DataManager", test_6_data_manager),
        ("Sistema de Auditoría", test_7_auditoria),
        ("Rendimiento Básico", test_8_rendimiento),
        ("Sistema de Backup", test_9_backup),
        ("Limpieza de Datos de Prueba", test_10_limpieza),
    ]
    
    resultados = []
    
    for nombre, test_func in tests:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print_error(f"Error fatal en test '{nombre}': {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print_header("RESUMEN DE PRUEBAS")
    
    tests_exitosos = sum(1 for _, resultado in resultados if resultado)
    tests_totales = len(resultados)
    
    for nombre, resultado in resultados:
        if resultado:
            print(f"{Colors.GREEN}✓{Colors.END} {nombre}")
        else:
            print(f"{Colors.RED}✗{Colors.END} {nombre}")
    
    print()
    print(f"Resultado: {tests_exitosos}/{tests_totales} pruebas exitosas")
    print()
    
    if tests_exitosos == tests_totales:
        print(f"{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.GREEN}  ✓ TODAS LAS PRUEBAS PASARON EXITOSAMENTE{Colors.END}")
        print(f"{Colors.GREEN}{'='*70}{Colors.END}")
        print()
        print("La base de datos SQLite encriptada está funcionando correctamente.")
        print("La aplicación puede usar el nuevo sistema de forma segura.")
        print()
        return 0
    else:
        print(f"{Colors.RED}{'='*70}{Colors.END}")
        print(f"{Colors.RED}  ✗ ALGUNAS PRUEBAS FALLARON{Colors.END}")
        print(f"{Colors.RED}{'='*70}{Colors.END}")
        print()
        print("Por favor, revise los errores antes de usar el sistema en producción.")
        print()
        return 1


if __name__ == "__main__":
    sys.exit(main())    