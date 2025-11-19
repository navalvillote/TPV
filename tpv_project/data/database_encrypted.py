"""
Sistema de base de datos SQLite ENCRIPTADA para TPV.

Este archivo implementa la opción A (recomendada): la base de datos
entera se almacena cifrada en disco usando Fernet (cryptography).

Funcionamiento resumido:
- En disco: archivo cifrado (tpv.db) — nunca en claro.
- Al abrir: se descifra a un archivo temporal, SQLite trabaja sobre él.
- Al cerrar: se cifra el temporal y se sobreescribe el archivo en disco.

Requisitos: `pip install cryptography`
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import json
import shutil
from pathlib import Path
import hashlib
import base64

from cryptography.fernet import Fernet, InvalidToken

# Importa la configuración de encriptación de tu proyecto
from config.settings import EncryptionConfig


class DatabaseManagerEncrypted:
    """Gestiona la base de datos SQLite cifrada en disco usando Fernet.

    Nota:
        - No usa SQLCipher ni extensiones C; es compatible con Python 3.13+ en Windows.
        - `EncryptionConfig.ENCRYPTION_KEY` puede ser:
            * Una clave Fernet válida (bytes o str, 44 caracteres base64 urlsafe)
            * O cualquier secreto (passphrase) — en ese caso se derivará un key determinístico
              mediante SHA-256 y se mapeará a una clave Fernet.
    """

    def __init__(self, db_path: str = "data/tpv.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Se acepta que EncryptionConfig.ENCRYPTION_KEY sea bytes o str
        raw_key = EncryptionConfig.ENCRYPTION_KEY
        if isinstance(raw_key, str):
            raw_key = raw_key.encode("utf-8")
        self._raw_key = raw_key

        # Inicializar DB (si no existe, se creará al abrir por primera vez)
        self._inicializar_db()

    # -------------------------- Helpers de cifrado --------------------------
    def _derive_fernet_key(self) -> bytes:
        """Deriva una clave Fernet a partir de _raw_key.

        Si _raw_key ya parece una clave Fernet válida (44 bytes base64 urlsafe),
        se usa tal cual. Si no, se deriva SHA256(raw_key) y se convierte a base64 urlsafe.
        """
        if self._raw_key is None:
            raise ValueError("No hay clave de encriptación configurada")

        # Si parece ya una clave Fernet válida -> usarla
        if len(self._raw_key) == 44:
            try:
                # validar base64
                base64.urlsafe_b64decode(self._raw_key)
                return self._raw_key
            except Exception:
                pass

        # Derivar: SHA256(secret) -> base64 urlsafe
        h = hashlib.sha256(self._raw_key).digest()
        return base64.urlsafe_b64encode(h)

    def _get_fernet(self) -> Fernet:
        key = self._derive_fernet_key()
        return Fernet(key)

    def _encrypt_bytes(self, data: bytes) -> bytes:
        f = self._get_fernet()
        return f.encrypt(data)

    def _decrypt_bytes(self, data: bytes) -> bytes:
        f = self._get_fernet()
        return f.decrypt(data)

    # -------------------------- Context manager ------------------------------
    @contextmanager
    def get_connection(self):
        """Context manager que devuelve una conexión sqlite3 sobre un archivo temporal

        Flujo:
            - Si existe `self.db_path` (archivo cifrado), lo descifra a archivo temporal
            - Si no existe, crea un archivo sqlite vacío temporal
            - Abre sqlite3.connect() sobre el temporal y yields la conexión
            - Al salir, cierra la conexión, cifra el contenido del temporal y sobreescribe el archivo real
            - El archivo temporal se elimina
        """
        temp_path = self.db_path.with_suffix(self.db_path.suffix + ".tmp")

        try:
            # Si existe archivo cifrado en disco, lo desciframos
            if self.db_path.exists() and self.db_path.stat().st_size > 0:
                encrypted = self.db_path.read_bytes()
                try:
                    decrypted = self._decrypt_bytes(encrypted)
                except InvalidToken:
                    raise Exception("Clave de encriptación incorrecta o archivo corrupto")

                temp_path.write_bytes(decrypted)
            else:
                # Crear una base sqlite vacía en el temporal
                conn_tmp = sqlite3.connect(str(temp_path))
                conn_tmp.execute("PRAGMA journal_mode=WAL")
                conn_tmp.commit()
                conn_tmp.close()

            # Abrir conexión sobre el temporal
            conn = sqlite3.connect(str(temp_path))
            conn.row_factory = sqlite3.Row

            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

            # Leer el contenido del temporal y cifrarlo en disco
            plain = temp_path.read_bytes()
            encrypted = self._encrypt_bytes(plain)
            # Asegurar escritura atómica: escribir a tmp y renombrar
            tmp_write = self.db_path.with_suffix(self.db_path.suffix + ".write")
            tmp_write.write_bytes(encrypted)
            tmp_write.replace(self.db_path)

        finally:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except Exception:
                pass

    # -------------------------- Inicialización ------------------------------
    def _inicializar_db(self):
        """Crea las tablas si la DB está vacía (nuevo archivo).

        Abre la conexión mediante el context manager para asegurarse de que
        el archivo temporal se inicialice y se cifre correctamente.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Comprobamos si las tablas ya existen
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productos'")
            if cursor.fetchone():
                return  # ya inicializada

            fecha_actual = datetime.now().isoformat()

            # ================================================================
            # TABLA DE PRODUCTOS
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    precio REAL NOT NULL,
                    familia TEXT NOT NULL,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TEXT NOT NULL,
                    fecha_modificacion TEXT NOT NULL,
                    usuario_modificacion TEXT
                )
            """)

            # ================================================================
            # TABLA DE HISTORIAL DE PRECIOS
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historial_precios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    producto_id INTEGER NOT NULL,
                    precio_anterior REAL NOT NULL,
                    precio_nuevo REAL NOT NULL,
                    fecha_cambio TEXT NOT NULL,
                    usuario TEXT,
                    FOREIGN KEY (producto_id) REFERENCES productos(id)
                )
            """)

            # ================================================================
            # TABLA DE CLIENTES
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    notas TEXT,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TEXT NOT NULL
                )
            """)

            # ================================================================
            # TABLA DE CAMAREROS
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS camareros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    codigo TEXT UNIQUE,
                    activo BOOLEAN DEFAULT 1,
                    fecha_creacion TEXT NOT NULL
                )
            """)

            # ================================================================
            # TABLA DE RECIBOS (TICKETS)
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS recibos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    cliente_nombre TEXT,
                    camarero_nombre TEXT,
                    estado TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    iva_porcentaje REAL NOT NULL,
                    total REAL NOT NULL,
                    impreso BOOLEAN DEFAULT 0,
                    fecha_creacion TEXT NOT NULL,
                    fecha_modificacion TEXT NOT NULL
                )
            """)

            # ================================================================
            # TABLA DE LÍNEAS DE RECIBO
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS lineas_recibo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    recibo_id INTEGER NOT NULL,
                    producto_nombre TEXT NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario REAL NOT NULL,
                    familia TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    FOREIGN KEY (recibo_id) REFERENCES recibos(id) ON DELETE CASCADE
                )
            """)

            # ================================================================
            # TABLA DE CONFIGURACIÓN
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS configuracion (
                    clave TEXT PRIMARY KEY,
                    valor TEXT NOT NULL,
                    fecha_modificacion TEXT NOT NULL
                )
            """)

            # ================================================================
            # TABLA DE AUDITORÍA
            # ================================================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS auditoria (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tabla TEXT NOT NULL,
                    accion TEXT NOT NULL,
                    registro_id INTEGER,
                    datos_anteriores TEXT,
                    datos_nuevos TEXT,
                    usuario TEXT,
                    fecha TEXT NOT NULL
                )
            """)

            # INDICES
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_recibos_fecha ON recibos(fecha)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_recibos_estado ON recibos(estado)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_recibos_cliente ON recibos(cliente_nombre)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_recibos_camarero ON recibos(camarero_nombre)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_nombre ON productos(nombre)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_productos_familia ON productos(familia)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_lineas_recibo_id ON lineas_recibo(recibo_id)")

    # ========================================================================
    # PRODUCTOS (se conservan exactamente los mismos métodos que antes)
    # ========================================================================

    def guardar_producto(self, nombre: str, precio: float, familia: str,
                        usuario: str = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("SELECT id, precio FROM productos WHERE nombre = ?", (nombre,))
            row = cursor.fetchone()

            if row:
                producto_id = row['id']
                precio_anterior = row['precio']

                cursor.execute("""
                    UPDATE productos 
                    SET precio = ?, familia = ?, fecha_modificacion = ?, usuario_modificacion = ?
                    WHERE id = ?
                """, (precio, familia, fecha_actual, usuario, producto_id))

                if precio != precio_anterior:
                    cursor.execute("""
                        INSERT INTO historial_precios 
                        (producto_id, precio_anterior, precio_nuevo, fecha_cambio, usuario)
                        VALUES (?, ?, ?, ?, ?)
                    """, (producto_id, precio_anterior, precio, fecha_actual, usuario))

                self._registrar_auditoria(
                    cursor, 'productos', 'UPDATE', producto_id,
                    {'precio': precio_anterior},
                    {'precio': precio, 'familia': familia},
                    usuario
                )
            else:
                cursor.execute("""
                    INSERT INTO productos (nombre, precio, familia, fecha_creacion, fecha_modificacion)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, precio, familia, fecha_actual, fecha_actual))

                producto_id = cursor.lastrowid

                self._registrar_auditoria(
                    cursor, 'productos', 'INSERT', producto_id,
                    None,
                    {'nombre': nombre, 'precio': precio, 'familia': familia},
                    usuario
                )

            return producto_id

    def obtener_productos(self, familia: str = None, activos: bool = True) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM productos WHERE 1=1"
            params = []

            if activos:
                query += " AND activo = 1"

            if familia:
                query += " AND familia = ?"
                params.append(familia)

            query += " ORDER BY nombre"

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def eliminar_producto(self, nombre: str, usuario: str = None) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
            row = cursor.fetchone()

            if row:
                producto_id = row['id']
                cursor.execute("""
                    UPDATE productos 
                    SET activo = 0, fecha_modificacion = ?
                    WHERE id = ?
                """, (fecha_actual, producto_id))

                self._registrar_auditoria(
                    cursor, 'productos', 'DELETE', producto_id,
                    {'activo': True},
                    {'activo': False},
                    usuario
                )

                return True

            return False

    # ========================================================================
    # RECIBOS
    # ========================================================================

    def guardar_recibo(self, recibo_data: Dict, lineas: List[Dict],
                      usuario: str = None) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("""
                INSERT INTO recibos 
                (fecha, cliente_nombre, camarero_nombre, estado, 
                 subtotal, iva_porcentaje, total, impreso, 
                 fecha_creacion, fecha_modificacion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recibo_data['fecha'],
                recibo_data.get('cliente_nombre'),
                recibo_data.get('camarero_nombre'),
                recibo_data['estado'],
                recibo_data['subtotal'],
                recibo_data['iva_porcentaje'],
                recibo_data['total'],
                recibo_data.get('impreso', False),
                fecha_actual,
                fecha_actual
            ))

            recibo_id = cursor.lastrowid

            for linea in lineas:
                cursor.execute("""
                    INSERT INTO lineas_recibo
                    (recibo_id, producto_nombre, cantidad, precio_unitario, familia, subtotal)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    recibo_id,
                    linea['producto_nombre'],
                    linea['cantidad'],
                    linea['precio_unitario'],
                    linea['familia'],
                    linea['subtotal']
                ))

            self._registrar_auditoria(
                cursor, 'recibos', 'INSERT', recibo_id,
                None,
                recibo_data,
                usuario
            )

            return recibo_id

    def obtener_recibos(self, estado: str = None, cliente: str = None,
                       fecha_inicio: str = None, fecha_fin: str = None,
                       limit: int = None, offset: int = 0) -> List[Dict]:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM recibos WHERE 1=1"
            params = []

            if estado:
                query += " AND estado = ?"
                params.append(estado)

            if cliente:
                query += " AND cliente_nombre = ?"
                params.append(cliente)

            if fecha_inicio:
                query += " AND fecha >= ?"
                params.append(fecha_inicio)

            if fecha_fin:
                query += " AND fecha <= ?"
                params.append(fecha_fin)

            query += " ORDER BY fecha DESC"

            if limit:
                query += " LIMIT ? OFFSET ?"
                params.extend([limit, offset])

            cursor.execute(query, params)
            recibos = [dict(row) for row in cursor.fetchall()]

            for recibo in recibos:
                cursor.execute("""
                    SELECT * FROM lineas_recibo WHERE recibo_id = ?
                """, (recibo['id'],))
                recibo['lineas'] = [dict(row) for row in cursor.fetchall()]

            return recibos

    def actualizar_estado_recibo(self, recibo_id: int, nuevo_estado: str,
                                 usuario: str = None) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("SELECT estado FROM recibos WHERE id = ?", (recibo_id,))
            row = cursor.fetchone()

            if row:
                estado_anterior = row['estado']

                cursor.execute("""
                    UPDATE recibos 
                    SET estado = ?, fecha_modificacion = ?
                    WHERE id = ?
                """, (nuevo_estado, fecha_actual, recibo_id))

                self._registrar_auditoria(
                    cursor, 'recibos', 'UPDATE', recibo_id,
                    {'estado': estado_anterior},
                    {'estado': nuevo_estado},
                    usuario
                )

                return True

            return False

    def eliminar_recibo(self, recibo_id: int, usuario: str = None) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM recibos WHERE id = ?", (recibo_id,))
            row = cursor.fetchone()

            if row:
                recibo_data = dict(row)
                cursor.execute("DELETE FROM recibos WHERE id = ?", (recibo_id,))

                self._registrar_auditoria(
                    cursor, 'recibos', 'DELETE', recibo_id,
                    recibo_data,
                    None,
                    usuario
                )

                return True

            return False

    # ========================================================================
    # CLIENTES
    # ========================================================================

    def guardar_cliente(self, nombre: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("""
                INSERT OR IGNORE INTO clientes (nombre, fecha_creacion)
                VALUES (?, ?)
            """, (nombre, fecha_actual))

            if cursor.rowcount > 0:
                return cursor.lastrowid
            else:
                cursor.execute("SELECT id FROM clientes WHERE nombre = ?", (nombre,))
                return cursor.fetchone()['id']

    def obtener_clientes(self, activos: bool = True) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT nombre FROM clientes WHERE 1=1"
            if activos:
                query += " AND activo = 1"
            query += " ORDER BY nombre"

            cursor.execute(query)
            return [row['nombre'] for row in cursor.fetchall()]

    def eliminar_cliente(self, nombre: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET activo = 0 WHERE nombre = ?", (nombre,))
            return cursor.rowcount > 0

    # ========================================================================
    # CAMAREROS
    # ========================================================================

    def guardar_camarero(self, nombre: str) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            cursor.execute("""
                INSERT OR IGNORE INTO camareros (nombre, fecha_creacion)
                VALUES (?, ?)
            """, (nombre, fecha_actual))

            if cursor.rowcount > 0:
                return cursor.lastrowid
            else:
                cursor.execute("SELECT id FROM camareros WHERE nombre = ?", (nombre,))
                return cursor.fetchone()['id']

    def obtener_camareros(self, activos: bool = True) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT nombre FROM camareros WHERE 1=1"
            if activos:
                query += " AND activo = 1"
            query += " ORDER BY nombre"

            cursor.execute(query)
            return [row['nombre'] for row in cursor.fetchall()]

    def eliminar_camarero(self, nombre: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE camareros SET activo = 0 WHERE nombre = ?", (nombre,))
            return cursor.rowcount > 0

    # ========================================================================
    # CONFIGURACIÓN
    # ========================================================================

    def guardar_configuracion(self, clave: str, valor: Any) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now().isoformat()

            if not isinstance(valor, str):
                valor = json.dumps(valor)

            cursor.execute("""
                INSERT OR REPLACE INTO configuracion (clave, valor, fecha_modificacion)
                VALUES (?, ?, ?)
            """, (clave, valor, fecha_actual))

    def obtener_configuracion(self, clave: str, default: Any = None) -> Any:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM configuracion WHERE clave = ?", (clave,))
            row = cursor.fetchone()

            if row:
                valor = row['valor']
                try:
                    return json.loads(valor)
                except Exception:
                    return valor

            return default

    # ========================================================================
    # UTILIDADES
    # ========================================================================

    def _registrar_auditoria(self, cursor, tabla: str, accion: str,
                            registro_id: int, datos_anteriores: Dict,
                            datos_nuevos: Dict, usuario: str):
        fecha_actual = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO auditoria 
            (tabla, accion, registro_id, datos_anteriores, datos_nuevos, usuario, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tabla,
            accion,
            registro_id,
            json.dumps(datos_anteriores) if datos_anteriores else None,
            json.dumps(datos_nuevos) if datos_nuevos else None,
            usuario,
            fecha_actual
        ))

    def crear_backup(self) -> Path:
        backup_dir = self.db_path.parent / 'backup'
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = backup_dir / f'tpv_{timestamp}.db'

        # Copiar archivo cifrado tal cual
        if self.db_path.exists():
            shutil.copy2(self.db_path, backup_path)

        # Mantener solo últimos 30 backups
        backups = sorted(backup_dir.glob('tpv_*.db'))
        if len(backups) > 30:
            for old_backup in backups[:-30]:
                old_backup.unlink()

        return backup_path

    def obtener_estadisticas(self) -> Dict:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            cursor.execute("SELECT COUNT(*) as total FROM productos WHERE activo = 1")
            stats['productos_activos'] = cursor.fetchone()['total']

            cursor.execute("""
                SELECT estado, COUNT(*) as total, SUM(total) as suma
                FROM recibos
                GROUP BY estado
            """)
            stats['recibos'] = {row['estado']: {
                'cantidad': row['total'],
                'total': row['suma'] if row['suma'] else 0
            } for row in cursor.fetchall()}

            cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE activo = 1")
            stats['clientes'] = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM camareros WHERE activo = 1")
            stats['camareros'] = cursor.fetchone()['total']

            stats['tamano_db_bytes'] = self.db_path.stat().st_size if self.db_path.exists() else 0

            return stats

    def verificar_integridad(self) -> bool:
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sqlite_master")
                cursor.fetchone()
                return True
        except Exception as e:
            print(f"Error de integridad: {e}")
            return False


# ============================================================================
# INSTANCIA GLOBAL
# ============================================================================

_db_manager = None


def get_database_manager() -> DatabaseManagerEncrypted:
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManagerEncrypted()
    return _db_manager


__all__ = [
    'DatabaseManagerEncrypted',
    'get_database_manager'
]
