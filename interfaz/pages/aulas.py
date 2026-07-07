import streamlit as st

from interfaz.components.tables import aula_to_dict


def mostrar_aulas(sistema):
    st.title("Aulas")
    st.subheader("Aulas registradas")

    if not sistema.aulas:
        st.warning("No hay aulas registradas.")
        return

    filas = [aula_to_dict(aula) for aula in sistema.aulas]
    st.dataframe(filas, use_container_width=True, hide_index=True)
