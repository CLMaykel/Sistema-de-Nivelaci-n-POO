import streamlit as st

from interfaz.components.tables import horario_to_dict


def mostrar_horarios(sistema):
    st.title("Horarios")
    st.subheader("Horarios registrados")

    if not sistema.horarios:
        st.warning("No hay horarios registrados.")
        return

    filas = [horario_to_dict(horario) for horario in sistema.horarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
