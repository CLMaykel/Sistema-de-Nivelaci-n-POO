import streamlit as st


def metric_card(titulo, valor):
    # Muestra una métrica con título y valor en la interfaz
    st.metric(titulo, valor)
