import streamlit as st
import pandas as pd

from src.db import engine
from src.repositories.gasto_repository import GastoRepository
from src.services.gasto_service import GastoService
from src.views.formulario_gastos import render_formulario
from src.views.graficos_gastos import render_graficos
from src.views.df_gastos import render_df


repo = GastoRepository(engine)
service = GastoService(repo)


@st.cache_data
def cargar_gastos(user_id):
    gastos = service.obtener_gastos_usuario(user_id)

    df = pd.DataFrame(
        [g.to_dict() for g in gastos]
        )

    if not df.empty:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df


def render_app():

    # CARGAR DATOS
    user_id = st.session_state.user["id"]

    df = cargar_gastos(user_id)

    categorias = service.obtener_categorias(df)

    st.title("Dashboard de Gastos Personales")

    st.sidebar.header("Navegación")

    if "pagina" not in st.session_state:
        st.session_state.pagina = "Añadir Gasto"

    if st.sidebar.button("Añadir Gasto", width=115):
        st.session_state.pagina = "Añadir Gasto"

    if st.sidebar.button("Gráficos", width=115):
        st.session_state.pagina = "Gráficos"

    if st.sidebar.button("DataFrame", width=115):
        st.session_state.pagina = "DataFrame"


    if st.session_state.pagina == "Añadir Gasto":

        render_formulario(user_id=user_id, categorias=categorias, service=service)
    
    if "mensaje" in st.session_state:
        st.success(st.session_state.mensaje)
        del st.session_state.mensaje


    if st.session_state.pagina == "Gráficos":

        render_graficos(df)


    if st.session_state.pagina == "DataFrame":
        
        render_df(df=df, user_id=user_id, categorias=categorias, service=service)