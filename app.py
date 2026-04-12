import streamlit as st
import pandas as pd
import plotly.express as px
from src.funciones import pestania_aniadir_gasto, pestania_graficos

st.set_page_config(
    page_title="Gastos Personales", # Título de la página
    layout="wide", # Diseño de la página (anchura completa) o cambiar a "centered" para centrado
    initial_sidebar_state="expanded", # Estado inicial de la barra lateral, "expanded" o "collapsed"
)

def main():
    if "gastos" not in st.session_state:
        try:
            st.session_state.gastos = pd.read_csv("data/gastos.csv", parse_dates=["fecha"])
        except:
            st.session_state.gastos = pd.DataFrame(
            columns=["fecha", "categoria", "monto", "descripcion"]
        )
            
    st.title("Dashboard de Gastos Personales")
    st.sidebar.header("Navegación")

    opciones_navegacion = ["Añadir Gasto", "Gráficos"]
    pestania = st.sidebar.selectbox("Menú", options = opciones_navegacion)

    match pestania:
        case "Añadir Gasto":
            pestania_aniadir_gasto()

        case "Gráficos":
            pestania_graficos()

if __name__ == "__main__":
    main()