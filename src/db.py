from sqlalchemy import create_engine, text
import pandas as pd
import hashlib
from dotenv import load_dotenv
import os

# CARGAR EL .env
load_dotenv()

# URL DE SUPABASE
DB_URL = os.getenv("DB_URL")

# ENGINE
engine = create_engine(DB_URL, pool_size=2, max_overflow=0)

# HASHEAR LA CONTRASEÑA
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# REGISTRAR USUARIO
def registrar_usuario(username, password):

    password_hash = hash_password(password)

    try:
        with engine.begin() as conn:

            conn.execute(
                text("""
                    INSERT INTO usuarios (username, password)
                    VALUES (:username, :password)
                """),
                {
                    "username": username,
                    "password": password_hash
                }
            )

        return True

    except Exception as e:
        print(e)
        return False

# LOGIN
def login_usuario(username, password):

    password_hash = hash_password(password)

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT *
                FROM usuarios
                WHERE username = :username
                AND password = :password
            """),
            {
                "username": username,
                "password": password_hash
            }
        )

        user = result.fetchone()

    return dict(user._mapping) if user else None


# INSERTAR GASTO
def insertar_gasto(user_id, fecha, categoria, monto, descripcion):

    fecha = pd.to_datetime(fecha).strftime("%Y-%m-%d")

    with engine.begin() as conn:

        conn.execute(
            text("""
                INSERT INTO gastos
                (user_id, fecha, categoria, monto, descripcion)

                VALUES
                (:user_id, :fecha, :categoria, :monto, :descripcion)
            """),
            {
                "user_id": user_id,
                "fecha": fecha,
                "categoria": categoria,
                "monto": monto,
                "descripcion": descripcion
            }
        )


# OBTENER GASTOS
def obtener_gastos(user_id):

    query = text("""
        SELECT id, fecha, categoria, monto, descripcion
        FROM gastos
        WHERE user_id = :user_id
    """)

    df = pd.read_sql(
        query,
        engine,
        params={"user_id": user_id}
    )

    if not df.empty:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df


# ELIMINAR GASTO
def eliminar_gasto(gasto_id):

    with engine.begin() as conn:

        conn.execute(
            text("""
                DELETE FROM gastos
                WHERE id = :id
            """),
            {
                "id": gasto_id
            }
        )


# ACTUALIZAR GASTO
def actualizar_gasto(gasto_id, fecha, categoria, monto, descripcion):

    fecha = pd.to_datetime(fecha).strftime("%Y-%m-%d")

    with engine.begin() as conn:

        conn.execute(
            text("""
                UPDATE gastos

                SET
                    fecha = :fecha,
                    categoria = :categoria,
                    monto = :monto,
                    descripcion = :descripcion

                WHERE id = :id
            """),
            {
                "id": gasto_id,
                "fecha": fecha,
                "categoria": categoria,
                "monto": monto,
                "descripcion": descripcion
            }
        )