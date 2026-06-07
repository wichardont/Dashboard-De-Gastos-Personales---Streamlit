from dataclasses import dataclass

import pandas as pd

@dataclass
class Ingreso:
    id: int | None
    user_id: int
    fecha: pd.Timestamp
    categoria: str
    monto: float
    descripcion: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "fecha": self.fecha,
            "categoria": self.categoria,
            "monto": self.monto,
            "descripcion": self.descripcion
        }