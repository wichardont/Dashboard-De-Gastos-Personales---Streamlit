from src.models.gastos import Gasto
from src.repositories.gasto_repository import GastoRepository


class GastoService:

    def __init__(self, repository: GastoRepository):
        self.repository = repository

    def obtener_gastos_usuario(self, user_id: int) -> list[Gasto]:
        return self.repository.obtener_por_usuario(user_id)

    def crear_gasto(self, user_id, fecha, categoria, monto, descripcion=""):

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if not categoria.strip():
            raise ValueError("La categoría es obligatoria")
        
        categoria = categoria.strip().title()

        gasto = Gasto(
            id=None,
            user_id=user_id,
            fecha=fecha,
            categoria=categoria,
            monto=monto,
            descripcion=descripcion
        )

        self.repository.crear(gasto)

    def actualizar_gasto(
        self,
        gasto_id,
        user_id,
        fecha,
        categoria,
        monto,
        descripcion=""
    ):

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        gasto = Gasto(
            id=gasto_id,
            user_id=user_id,
            fecha=fecha,
            categoria=categoria,
            monto=monto,
            descripcion=descripcion
        )

        self.repository.actualizar(gasto)

    def eliminar_gasto(self, gasto_id):
        self.repository.eliminar(gasto_id)
    
    def obtener_categorias(self, df):
        categorias_default = [
            "Comida",
            "Transporte",
            "Ocio",
            "Otro"
        ]

        if df.empty:
            return categorias_default

        categorias = categorias_default.copy()

        for categoria in df["categoria"].unique():

            if categoria not in categorias:
                categorias.append(categoria)

        return categorias