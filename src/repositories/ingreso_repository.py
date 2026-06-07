from sqlalchemy import text
from sqlalchemy.engine import Engine
from src.models.ingresos import Ingreso


class IngresoRepository:

    def __init__(self, engine: Engine):
        self.engine = engine
    
    def crear_ingresos(self, ingreso: Ingreso):
        query = text("""
            INSERT INTO ingresos
            (user_id, fecha, categoria, monto, descripcion)
            VALUES
            (:user_id, :fecha, :categoria, :monto, :descripcion)
        """)

        with self.engine.begin() as conn:
            conn.execute(
                query,
                {
                    "user_id": ingreso.user_id,
                    "fecha": ingreso.fecha,
                    "categoria": ingreso.categoria,
                    "monto": ingreso.monto,
                    "descripcion": ingreso.descripcion
                }
            )
    
    def obtener_por_usuario_ingresos(self, user_id: int) -> list[Ingreso]: # Indica que devuelve una lista de objetos Ingreso
        query = text("""
            SELECT
                id,
                user_id,
                fecha,
                categoria,
                monto,
                descripcion
            FROM ingresos
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
            Ingreso(
                id=fila.id,
                user_id=fila.user_id,
                fecha=fila.fecha,
                categoria=fila.categoria,
                monto=fila.monto,
                descripcion=fila.descripcion or ""
            )
            for fila in filas
        ]
    
    def actualizar_ingresos(self, ingreso: Ingreso):
        query = text("""
            UPDATE ingresos
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
                    "id": ingreso.id,
                    "fecha": ingreso.fecha,
                    "categoria": ingreso.categoria,
                    "monto": ingreso.monto,
                    "descripcion": ingreso.descripcion
                }
            )
    
    def eliminar_ingresos(self, ingreso_id: int):

        query = text("""
            DELETE FROM ingresos
            WHERE id = :id
        """)

        with self.engine.begin() as conn:

            conn.execute(
                query,
                {
                    "id": ingreso_id
                }
            )