import streamlit as st

def refrescar(mensaje):

    st.cache_data.clear()
    st.session_state.mensaje = mensaje
    st.rerun()