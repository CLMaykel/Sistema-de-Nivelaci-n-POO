import streamlit as st

from interfaz.pages.dashboard import mostrar_dashboard

OPCIONES = [
    "Dashboard",
    "Usuarios",
    "Aulas",
    "Horarios",
    "Cursos",
    "Inscripciones",
    "Cargas Academicas",
    "Reportes",
    "Acerca del Sistema",
]


def mostrar_acerca():
    st.title("Acerca del Sistema")
    st.write(
        "Sistema academico de nivelacion desarrollado en Python con Programacion Orientada a Objetos."
    )
    st.write("Interfaz web local con Streamlit.")


def main():
    st.set_page_config(page_title="Sistema de Nivelacion POO", layout="wide")

    from interfaz.state import get_sistema

    sistema = get_sistema()

    opcion = st.sidebar.radio("Navegacion", OPCIONES)

    if opcion == "Dashboard":
        mostrar_dashboard(sistema)
    elif opcion == "Acerca del Sistema":
        mostrar_acerca()
    else:
        st.title(opcion)
        st.info("Modulo en construccion.")
