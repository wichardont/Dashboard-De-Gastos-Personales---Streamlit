import streamlit as st
from src.ui import render_app
from src.db import login_usuario, registrar_usuario


def limpiar_campos():
    keys = [
        "login_user",
        "login_pass",
        "register_user",
        "register_pass"
        ]

    for key in keys:
        if key in st.session_state:
            del st.session_state[key]


def mostrar_login():
    st.title("Login")

    menu = st.selectbox("Selecciona opción", ["Iniciar Sesión", "Registrarse"], key = "menu_login")

    if menu == "Registrarse":
        user = st.text_input("Usuario", key = "register_user")
        password = st.text_input("Contraseña", type="password", key = "register_pass")

        if st.button("Registrar"):
            if registrar_usuario(user, password):
                st.success("Usuario creado")
                limpiar_campos()
            else:
                st.error("El usuario ya existe")

    elif menu == "Iniciar Sesión":
        user = st.text_input("Usuario", key = "login_user")
        password = st.text_input("Contraseña", type="password", key = "login_pass")

        if st.button("Entrar"):
            usuario = login_usuario(user, password)

            if usuario:
                limpiar_campos()
                st.session_state.user = usuario
                st.success(f"Bienvenido {user}")
                st.rerun()  # Recargar la app
            else:
                st.error("Credenciales incorrectas")

def main():

    st.markdown(
        """
        <html lang="es">
        """,
        unsafe_allow_html=True
    )

    st.set_page_config(
        page_title="Gastos Personales",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if "user" not in st.session_state:
        mostrar_login()
    else:
        st.sidebar.write(f"👤 {st.session_state.user["username"]}")

        if st.sidebar.button("Cerrar sesión"):
            del st.session_state.user
            st.rerun()
        
        st.sidebar.markdown("---")

        render_app()

if __name__ == "__main__":
    main()