import streamlit as st
import pandas as pd
from src.utils.ui_helpers import refrescar

def render_df_ingreso(df, user_id, categorias, service_ingreso):

    if df.empty:
        st.info("Áun no hay ingresos registrados")
        return

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
        st.warning("¿Seguro que quieres eliminar este ingreso?")

        col1, col2 = st.columns(2)

        if col1.button("Sí, eliminar", key="confirm_delete"):
            service_ingreso.eliminar_ingreso(st.session_state.confirmar_delete)
            del st.session_state.confirmar_delete
            refrescar("Ingreso eliminado")

        if col2.button("Cancelar", key="cancel_delete"):
            del st.session_state.confirmar_delete
    
    if "editando" in st.session_state:
        ingreso = st.session_state.editando

        st.subheader("Editar Ingreso")

        fecha = st.date_input("Fecha", pd.to_datetime(ingreso["fecha"]))


        categorias_editar = categorias.copy()

        if ingreso["categoria"] not in categorias_editar:
            categorias_editar.append(ingreso["categoria"])

        categoria = st.selectbox(
            "Categoría",
            categorias_editar,
            index=categorias_editar.index(ingreso["categoria"])
        )


        monto = st.number_input("Monto", value=float(ingreso["monto"]), min_value=0.0)
        descripcion = st.text_area("Descripción", value=ingreso["descripcion"])

        col1, col2 = st.columns(2)

        if col1.button("Guardar cambios"):
            service_ingreso.actualizar_ingreso(
                ingreso_id=ingreso["id"],
                user_id=user_id,
                fecha=pd.to_datetime(fecha).normalize(),
                categoria=categoria,
                monto=monto,
                descripcion=descripcion
            )

            del st.session_state.editando
            refrescar("Ingreso actualizado")

        if col2.button("Cancelar", key="cancel_edit"):
            del st.session_state.editando