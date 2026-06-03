from sqlalchemy import text
from sqlalchemy.engine import Engine
from src.models.gastos import Gasto


class GastoRepository:

    def __init__(self, engine: Engine):
        self.engine = engine
    
    def crear(self, gasto: Gasto):
        query = text("""
            INSERT INTO gastos
            (user_id, fecha, categoria, monto, descripcion)
            VALUES
            (:user_id, :fecha, :categoria, :monto, :descripcion)
        """)

        with self.engine.begin() as conn:
            conn.execute(
                query,
                {
                    "user_id": gasto.user_id,
                    "fecha": gasto.fecha,
                    "categoria": gasto.categoria,
                    "monto": gasto.monto,
                    "descripcion": gasto.descripcion
                }
            )
    
    def obtener_por_usuario(self, user_id: int) -> list[Gasto]: # Indica que devuelve una lista de objetos Gasto
        query = text("""
            SELECT
                id,
                user_id,
                fecha,
                categoria,
                monto,
                descripcion
            FROM gastos
            WHERE user_id = :user_id
            ORDER BY fecha DESC
        """)

        with self.engine.connect() as conn:

            result = conn.execute(
                query,
                {"user_id": user_id}
            )

            filas = result.fetchall()

        return [
            Gasto(
                id=fila.id,
                user_id=fila.user_id,
                fecha=fila.fecha,
                categoria=fila.categoria,
                monto=fila.monto,
                descripcion=fila.descripcion or ""
            )
            for fila in filas
        ]
    
    def actualizar(self, gasto: Gasto):
        query = text("""
            UPDATE gastos
            SET
                fecha = :fecha,
                categoria = :categoria,
                monto = :monto,
                descripcion = :descripcion
            WHERE id = :id
        """)

        with self.engine.begin() as conn:

            conn.execute(
                query,
                {
                    "id": gasto.id,
                    "fecha": gasto.fecha,
                    "categoria": gasto.categoria,
                    "monto": gasto.monto,
                    "descripcion": gasto.descripcion
                }
            )
    
    def eliminar(self, gasto_id: int):

        query = text("""
            DELETE FROM gastos
            WHERE id = :id
        """)

        with self.engine.begin() as conn:

            conn.execute(
                query,
                {
                    "id": gasto_id
                }
            )