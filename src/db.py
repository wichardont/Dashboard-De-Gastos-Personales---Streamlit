from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
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
def hash_password(password: str) -> str:
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

    except IntegrityError as e:
        print(e)
        return False

# LOGIN
def login_usuario(username: str, password: str) -> dict | None:

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