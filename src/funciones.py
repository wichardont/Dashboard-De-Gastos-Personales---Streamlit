import pandas as pd
import streamlit as st
import plotly.express as px

def registrar_gasto(fecha, categoria, monto, descripcion):
        nuevo = pd.DataFrame([{
                "fecha": fecha,
                "categoria": categoria,
                "monto": monto,
                "descripcion": descripcion
                }])
        st.session_state.gastos = pd.concat(
                [st.session_state.gastos, nuevo],
                ignore_index=True
                ) 
        return nuevo

def pestania_aniadir_gasto():
        with st.form(key = "aniadir_gasto"):
                fecha = st.date_input("Ingresa la fecha")
                categoria = st.selectbox("Selecciona la categoría del gasto",
                                ["Comida", "Transporte", "Ocio", "Otro"])
                monto = st.number_input("Ingresa el monto gastado", min_value=0.0)
                descripcion = st.text_area("Añade una descripcion del gasto (opcional)", height=100)

                registrar = st.form_submit_button("Registrar Gasto")

                if registrar:
                        registrar_gasto(fecha, categoria, monto, descripcion)
                        st.success("Gasto Registrado")
                        st.session_state.gastos.to_csv("data/gastos.csv", index=False) # guardar automáticamente

def pestania_graficos():
        df = st.session_state.gastos
        with st.container():
                col1, col2, col3 = st.columns(3)
                with col1:
                        #Métrica (Total gastado)
                        st.metric("Total gastado",
                                f"${df["monto"].sum():,.0f}",
                                delta=None)  
                with col2:
                        #Métrica (Promedio)
                        st.metric("Promedio gastado",
                                f"${df["monto"].mean():,.0f}",
                                delta=None)
                with col3:
                        #Métrica (Máximo)
                        st.metric("Máximo gastado",
                                f"${df["monto"].max():,.0f}",
                                delta=None)
                
                st.markdown("---")
        
        with st.container():
                col1, col2 = st.columns(2)
                with col1:
                        #Gráfico de lineas
                        #Gastos por día
                        gastos_dia = df.groupby("fecha")["monto"].sum().reset_index()
                        gastos_dia = gastos_dia.sort_values("fecha")

                        fig = px.bar(
                                gastos_dia,
                                x="fecha",
                                y="monto",
                                title="Gastos por día"
                                )

                        st.plotly_chart(fig, use_container_width=True)
        
                with col2:
                        #Pastel
                        #Agrupar por categoría
                        gastos_categoria = df.groupby("categoria")["monto"].sum().reset_index()
                        fig = px.pie(gastos_categoria,
                                values = "monto",
                                names = "categoria",
                                title = "Gastos por categoría")
                        
                        st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("---")
                
                st.dataframe(df)