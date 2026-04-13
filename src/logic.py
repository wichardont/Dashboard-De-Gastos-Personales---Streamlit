import pandas as pd

def calcular_metricas(df):
    return {
        "total": df["monto"].sum(),
        "promedio": df["monto"].mean(),
        "maximo": df["monto"].max(),
        "minimo": df["monto"].min()
    }


def gastos_por_categoria(df):
    return df.groupby("categoria")["monto"].sum().reset_index()


def gastos_por_dia(df):
    df = df.copy()
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.strftime("%Y-%m-%d")
    return df.groupby("fecha")["monto"].sum().reset_index().sort_values("fecha")