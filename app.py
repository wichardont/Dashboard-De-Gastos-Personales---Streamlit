import streamlit as st
from src.ui import render_app
from src.db import login_usuario, registrar_usuario


def mostrar_login():
    st.title("Login")

    menu = st.selectbox("Selecciona opción", ["Iniciar Sesión", "Registrarse"])

    if menu == "Registrarse":
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Registrar"):
            if registrar_usuario(user, password):
                st.success("Usuario creado")
            else:
                st.error("El usuario ya existe")

    elif menu == "Iniciar Sesión":
        user = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Entrar"):
            usuario = login_usuario(user, password)

            if usuario:
                st.session_state.user = usuario
                st.success(f"Bienvenido {user}")
                st.rerun()  # Recargar la app
            else:
                st.error("Credenciales incorrectas")

def main():
    if "user" not in st.session_state:
        mostrar_login()
    else:
        st.sidebar.write(f"👤 {st.session_state.user["username"]}")

        if st.sidebar.button("Cerrar sesión"):
            del st.session_state.user
            st.rerun()

        render_app()

if __name__ == "__main__":
    main()