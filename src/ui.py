import streamlit as st
import pandas as pd
import plotly.express as px

from src.storage import cargar_datos, guardar_datos
from src.logic import calcular_metricas, gastos_por_categoria, gastos_por_dia


def render_app():

    st.set_page_config(
        page_title="Gastos Personales",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CARGAR DATOS
    if "gastos" not in st.session_state:
        st.session_state.gastos = cargar_datos()

    df = st.session_state.gastos

    st.title("Dashboard de Gastos Personales")

    st.sidebar.header("Navegación")

    opciones_navegacion = ["Añadir Gasto", "Gráficos", "DataFrame"]
    pestania = st.sidebar.selectbox("Menú", options = opciones_navegacion)

    match pestania:
        case "Añadir Gasto":
            # FORMULARIO
            with st.form("aniadir_gasto"):
                fecha = st.date_input("Fecha")
                fecha = pd.to_datetime(fecha).normalize()
                categoria = st.selectbox("Categoría", ["Comida", "Transporte", "Ocio", "Otro"])
                monto = st.number_input("Monto", min_value=0.0)
                descripcion = st.text_area("Descripción (opcional)", height=100)

                registrar = st.form_submit_button("Registrar Gasto")

                if registrar:
                    nuevo = pd.DataFrame([{
                        "fecha": fecha,
                        "categoria": categoria,
                        "monto": monto,
                        "descripcion": descripcion
                    }])

                    st.session_state.gastos = pd.concat([df, nuevo], ignore_index=True)
                    guardar_datos(st.session_state.gastos)

                    st.success("Gasto registrado")

        case "Gráficos":
            # VALIDACIÓN
            if df.empty:
                st.info("Áun no hay gastos registrados")
                return

            # MÉTRICAS
            st.subheader("Métricas")

            metricas = calcular_metricas(df)

            with st.container():
                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Total", f"${metricas['total']:,.2f}")
                col2.metric("Promedio", f"${metricas['promedio']:,.2f}")
                col3.metric("Máximo", f"${metricas['maximo']:,.2f}")
                col4.metric("Mínimo", f"${metricas['minimo']:,.2f}")

            st.markdown("---")

            # GRÁFICAS
            st.subheader("Gráficas")

            with st.container():
                col1, col2 = st.columns(2)

                with col1:
                    # gráfico por día
                    df_dia = gastos_por_dia(df)
                    fig_dia = px.bar(df_dia, x="fecha", y="monto", title="Gastos por día")
                    fig_dia.update_xaxes(type="category")

                    st.plotly_chart(fig_dia, use_container_width=True)
                
                with col2:
                    # gráfico por categoría
                    df_cat = gastos_por_categoria(df)
                    fig_cat = px.pie(df_cat, names="categoria", values="monto", title="Gastos por categoría")

                    st.plotly_chart(fig_cat, use_container_width=True)
        
        case "DataFrame":
            st.subheader("DataFrame actual")
            
            st.dataframe(df)