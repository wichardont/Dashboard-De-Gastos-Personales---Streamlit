import pandas as pd

def calcular_metricas(df: pd.DataFrame) -> dict:
    return {
        "total": df["monto"].sum(),
        "promedio": df["monto"].mean(),
        "maximo": df["monto"].max(),
        "minimo": df["monto"].min()
    }


def por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("categoria")["monto"].sum().reset_index()


def por_dia(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    return df.groupby("fecha")["monto"].sum().reset_index().sort_values("fecha")