import streamlit as st
import pandas as pd

from src.db import engine


from src.repositories.gasto_repository import GastoRepository
from src.services.gasto_service import GastoService
from src.views.formulario_gastos import render_formulario
from src.views.graficos_gastos import render_graficos
from src.views.df_gastos import render_df


repo_gasto = GastoRepository(engine)
service_gasto = GastoService(repo_gasto)


from src.repositories.ingreso_repository import IngresoRepository
from src.services.ingreso_service import IngresoService
from src.views.formulario_ingresos import render_formulario_ingreso
from src.views.graficos_ingresos import render_graficos_ingreso
from src.views.df_ingresos import render_df_ingreso


repo_ingreso = IngresoRepository(engine)
service_ingreso = IngresoService(repo_ingreso)


@st.cache_data
def cargar_gastos(user_id):
    gastos = service_gasto.obtener_gastos_usuario(user_id)

    df_gastos = pd.DataFrame(
        [g.to_dict() for g in gastos]
        )

    if not df_gastos.empty:
        df_gastos["fecha"] = pd.to_datetime(df_gastos["fecha"])

    return df_gastos


@st.cache_data
def cargar_ingresos(user_id):
    ingresos = service_ingreso.obtener_ingresos_usuario(user_id)

    df_ingresos = pd.DataFrame(
        [i.to_dict() for i in ingresos]
        )

    if not df_ingresos.empty:
        df_ingresos["fecha"] = pd.to_datetime(df_ingresos["fecha"])

    return df_ingresos


def render_app():

    # CARGAR DATOS
    user_id = st.session_state.user["id"]

    df_gastos = cargar_gastos(user_id)
    categorias_gastos = service_gasto.obtener_categorias(df_gastos)

    df_ingresos = cargar_ingresos(user_id)
    categorias_ingresos = service_ingreso.obtener_categorias(df_ingresos)

    
    st.title("Dashboard de Finanzas Personales")

    st.sidebar.header("Navegación")

    modulo = st.sidebar.selectbox("Módulo", ["Gastos", "Ingresos"])


    if modulo == "Gastos":

        if "pagina" not in st.session_state:
            st.session_state.pagina = "Añadir Gasto"

        if st.sidebar.button("Añadir Gasto", width=115):
            st.session_state.pagina = "Añadir Gasto"

        if st.sidebar.button("Gráficos", width=115):
            st.session_state.pagina = "Gráficos"

        if st.sidebar.button("DataFrame", width=115):
            st.session_state.pagina = "DataFrame"


        if st.session_state.pagina == "Añadir Gasto":

            render_formulario(user_id=user_id, categorias=categorias_gastos, service_gasto=service_gasto)
        
        if "mensaje" in st.session_state:
            st.success(st.session_state.mensaje)
            del st.session_state.mensaje


        if st.session_state.pagina == "Gráficos":

            render_graficos(df_gastos)


        if st.session_state.pagina == "DataFrame":
            
            render_df(df=df_gastos, user_id=user_id, categorias=categorias_gastos, service_gasto=service_gasto)
    

    elif modulo == "Ingresos":

        if "pagina_ingreso" not in st.session_state:
            st.session_state.pagina_ingreso = "Añadir Ingreso"

        if st.sidebar.button("Añadir Ingreso", width=115):
            st.session_state.pagina_ingreso = "Añadir Ingreso"

        if st.sidebar.button("Gráficos", width=115):
            st.session_state.pagina_ingreso = "Gráficos Ingreso"

        if st.sidebar.button("DataFrame", width=115):
            st.session_state.pagina_ingreso = "DataFrame Ingreso"


        if st.session_state.pagina_ingreso == "Añadir Ingreso":

            render_formulario_ingreso(user_id=user_id, categorias=categorias_ingresos, service_ingreso=service_ingreso)
        
        if "mensaje" in st.session_state:
            st.success(st.session_state.mensaje)
            del st.session_state.mensaje


        if st.session_state.pagina_ingreso == "Gráficos Ingreso":

            render_graficos_ingreso(df_ingresos)


        if st.session_state.pagina_ingreso == "DataFrame Ingreso":
            
            render_df_ingreso(df=df_ingresos, user_id=user_id, categorias=categorias_ingresos, service_ingreso=service_ingreso)
