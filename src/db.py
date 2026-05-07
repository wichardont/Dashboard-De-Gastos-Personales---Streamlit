import sqlite3
import pandas as pd
import hashlib

db_path = "data/gastos.db"

# Conexión
def conectar():
    return sqlite3.connect(db_path)

# Crear tablas
def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    # tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # tabla gastos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        fecha TEXT,
        categoria TEXT,
        monto REAL,
        descripcion TEXT,
        FOREIGN KEY(user_id) REFERENCES usuarios(id)
    )
    """)

    conn.commit()
    conn.close()

# Hashear la contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registrar usuario
def registrar_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Iniciar sesión (login)
def login_usuario(username, password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (username, hash_password(password))
    )

    user = cursor.fetchone()
    conn.close()

    return user  # None si no existe

# Insertar gasto
def insertar_gasto(user_id, fecha, categoria, monto, descripcion):
    conn = conectar()
    cursor = conn.cursor()

    # asegurar formato fecha
    fecha = pd.to_datetime(fecha).strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO gastos (user_id, fecha, categoria, monto, descripcion)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, fecha, categoria, monto, descripcion))

    conn.commit()
    conn.close()

# Obtener gasto por usuario
def obtener_gastos(user_id):
    conn = conectar()

    df = pd.read_sql(
        "SELECT id, fecha, categoria, monto, descripcion FROM gastos WHERE user_id = ?",
        conn,
        params=(user_id,)
    )

    conn.close()

    if not df.empty:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df
def eliminar_gasto(gasto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))

    conn.commit()
    conn.close()


def actualizar_gasto(gasto_id, fecha, categoria, monto, descripcion):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE gastos
        SET fecha = ?, categoria = ?, monto = ?, descripcion = ?
        WHERE id = ?
    """, (fecha, categoria, monto, descripcion, gasto_id))

    conn.commit()
    conn.close()