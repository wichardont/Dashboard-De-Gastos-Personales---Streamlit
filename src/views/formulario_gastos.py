import streamlit as st
import pandas as pd
from datetime import datetime

from src.utils.ui_helpers import refrescar

def render_formulario(user_id, categorias, service):

    st.subheader("Formulario para añadir gastos")
    
    fecha = st.date_input("Fecha", value=datetime.now())
    fecha = pd.to_datetime(fecha).normalize()
    categoria = st.selectbox(
        "Categoría",
        categorias
    )

    if categoria == "Otro":
        nueva_categoria = st.text_input("Nueva categoría")


    monto = st.number_input("Monto", min_value=0.0, step=1.0)
    descripcion = st.text_area("Descripción (opcional)", height=100)

    registrar = st.button("Registrar Gasto")

    if registrar:
        if monto <= 0:
            st.warning("El monto debe ser mayor a 0")
        else:
            categoria_final = categoria

            if categoria == "Otro":
                if not nueva_categoria.strip():
                    st.warning("Escribe una nueva categoria")
                    st.stop()

                categoria_final = nueva_categoria.strip().title()

            service.crear_gasto(
                user_id=user_id,
                fecha=fecha,
                categoria=categoria_final,
                monto=monto,
                descripcion=descripcion
            )
            
            refrescar("Gasto registrado")