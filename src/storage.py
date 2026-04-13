import pandas as pd

def cargar_datos():
    try:
        return pd.read_csv("data/gastos.csv", parse_dates=["fecha"])
    except:
        return pd.DataFrame(
        columns=["fecha", "categoria", "monto", "descripcion"]
        )

def guardar_datos(df):
    df.to_csv("data/gastos.csv", index=False)