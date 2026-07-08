import streamlit as st

from interfaz.components.cards import metric_card


def intro_modulo(descripcion, icono=""):
    prefijo = f"{icono} " if icono else ""
    st.markdown(f"{prefijo}{descripcion}")


def fila_metricas(metricas, columnas=4):
    cols = st.columns(columnas)
    for indice, (etiqueta, valor) in enumerate(metricas):
        with cols[indice % columnas]:
            metric_card(etiqueta, valor)


def tabla_o_vacio(filas, mensaje):
    if not filas:
        st.info(mensaje)
        return False
    st.dataframe(filas, use_container_width=True, hide_index=True)
    return True


def detalle_entidad(titulo, campos):
    with st.expander(titulo, expanded=False):
        for etiqueta, valor in campos:
            st.write(f"**{etiqueta}:** {valor}")
