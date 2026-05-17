import streamlit as st
import pandas as pd
import plotly.express as px

from src.db import obtener_gastos, insertar_gasto, eliminar_gasto, actualizar_gasto
from src.logic import calcular_metricas, gastos_por_categoria, gastos_por_dia


@st.cache_data
def cargar_gastos(user_id):
    return obtener_gastos(user_id)


def render_app():

    st.set_page_config(
        page_title="Gastos Personales",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CARGAR DATOS
    user_id = st.session_state.user["id"]

    df = cargar_gastos(user_id)

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
                    if monto <= 0:
                        st.warning("El monto debe ser mayor a 0")
                    else:
                        insertar_gasto(user_id, fecha, categoria, monto, descripcion)
                        st.cache_data.clear()
                        st.session_state.mensaje = "Gasto registrado"
                        st.rerun()
            
            if "mensaje" in st.session_state:
                st.success(st.session_state.mensaje)
                del st.session_state.mensaje

        case "Gráficos":
            # VALIDACIÓN
            if df.empty:
                st.info("Áun no hay gastos registrados")
                return
            
            st.subheader("Filtros")
            
            #FILTROS POR FECHA
            fecha_min = df["fecha"].min()
            fecha_max = df["fecha"].max()

            rango_fechas = st.date_input(
                "Rango de fechas",
                value=(fecha_min, fecha_max)
            )

            #FILTROS POR CATEGORIA
            categorias = df["categoria"].unique().tolist()

            categorias_seleccionadas = st.multiselect(
                "Categorías",
                options=categorias,
                default=categorias
            )

            #APLICAR FILTROS
            df_filtrado = df.copy()

            # filtro por fechas
            if len(rango_fechas) == 2:
                inicio, fin = rango_fechas
                df_filtrado = df_filtrado[
                    (df_filtrado["fecha"] >= pd.to_datetime(inicio)) &
                    (df_filtrado["fecha"] <= pd.to_datetime(fin))
                ]

            # filtro por categoría
            df_filtrado = df_filtrado[
                df_filtrado["categoria"].isin(categorias_seleccionadas)
            ]

            # MÉTRICAS
            st.subheader("Métricas")

            metricas = calcular_metricas(df_filtrado)

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
                    df_dia = gastos_por_dia(df_filtrado)
                    fig_dia = px.bar(df_dia, x="fecha", y="monto", title="Gastos por día")
                    fig_dia.update_xaxes(type="category")

                    st.plotly_chart(fig_dia, use_container_width=True)
                
                with col2:
                    # gráfico por categoría
                    df_cat = gastos_por_categoria(df_filtrado)
                    fig_cat = px.pie(df_cat, names="categoria", values="monto", title="Gastos por categoría")

                    st.plotly_chart(fig_cat, use_container_width=True)
        
        case "DataFrame":
            st.subheader("DataFrame actual")
            
            for i, row in df.iterrows():
                col1, col2, col3, col4, col5, col6 = st.columns([2,2,2,3,2,2])

                col1.write(row["fecha"])
                col2.write(row["categoria"])
                col3.write(f"${row['monto']:.2f}")
                col4.write(row["descripcion"])

                # BOTÓN EDITAR
                if col5.button("Editar", key=f"edit_{row['id']}"):
                    st.session_state.editando = row.to_dict()

                # BOTÓN ELIMINAR
                if col6.button("Eliminar", key=f"delete_{row['id']}"):
                    st.session_state.confirmar_delete = row["id"]
            
            if "confirmar_delete" in st.session_state:
                st.warning("¿Seguro que quieres eliminar este gasto?")

                col1, col2 = st.columns(2)

                if col1.button("Sí, eliminar"):
                    eliminar_gasto(st.session_state.confirmar_delete)
                    st.cache_data.clear()
                    del st.session_state.confirmar_delete
                    st.session_state.mensaje = "Gasto eliminado"
                    st.rerun()

                if col2.button("Cancelar"):
                    del st.session_state.confirmar_delete
            
            if "editando" in st.session_state:
                gasto = st.session_state.editando

                st.subheader("Editar gasto")

                fecha = st.date_input("Fecha", pd.to_datetime(gasto["fecha"]))
                categoria = st.selectbox(
                    "Categoría",
                    ["Comida", "Transporte", "Ocio", "Otro"],
                    index=["Comida", "Transporte", "Ocio", "Otro"].index(gasto["categoria"])
                )
                monto = st.number_input("Monto", value=float(gasto["monto"]), min_value=0.0)
                descripcion = st.text_area("Descripción", value=gasto["descripcion"])

                col1, col2 = st.columns(2)

                if col1.button("Guardar cambios"):
                    actualizar_gasto(
                        gasto["id"],
                        pd.to_datetime(fecha).normalize(),
                        categoria,
                        monto,
                        descripcion
                    )
                    st.cache_data.clear()

                    del st.session_state.editando
                    st.session_state.mensaje = "Gasto actualizado"
                    st.rerun()

                if col2.button("Cancelar"):
                    del st.session_state.editando