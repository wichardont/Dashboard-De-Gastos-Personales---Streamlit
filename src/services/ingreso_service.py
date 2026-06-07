from src.models.ingresos import Ingreso
from src.repositories.ingreso_repository import IngresoRepository


class IngresoService:

    def __init__(self, repository: IngresoRepository):
        self.repository = repository

    def obtener_ingresos_usuario(self, user_id: int) -> list[Ingreso]:
        return self.repository.obtener_por_usuario_ingresos(user_id)

    def crear_ingreso(self, user_id, fecha, categoria, monto, descripcion=""):

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if not categoria.strip():
            raise ValueError("La categoría es obligatoria")
        
        categoria = categoria.strip().title()

        ingreso = Ingreso(
            id=None,
            user_id=user_id,
            fecha=fecha,
            categoria=categoria,
            monto=monto,
            descripcion=descripcion
        )

        self.repository.crear_ingresos(ingreso)

    def actualizar_ingreso(
        self,
        ingreso_id,
        user_id,
        fecha,
        categoria,
        monto,
        descripcion=""
    ):

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if not categoria.strip():
            raise ValueError("La categoría es obligatoria")
        
        categoria = categoria.strip().title()

        ingreso = Ingreso(
            id=ingreso_id,
            user_id=user_id,
            fecha=fecha,
            categoria=categoria,
            monto=monto,
            descripcion=descripcion
        )

        self.repository.actualizar_ingresos(ingreso)

    def eliminar_ingreso(self, ingreso_id):
        self.repository.eliminar_ingresos(ingreso_id)
    
    def obtener_categorias(self, df):
        categorias_default = [
            "Salario", "Ingreso extra", "Otro"
        ]

        if df.empty:
            return categorias_default

        categorias = categorias_default.copy()

        for categoria in df["categoria"].unique():

            if categoria not in categorias:
                categorias.append(categoria)

        return categorias