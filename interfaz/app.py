import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from servicios.sistema_nivelacion import SistemaNivelacion

st.set_page_config(page_title="Sistema de Nivelacion POO", layout="wide")

if "sistema" not in st.session_state:
    st.session_state.sistema = SistemaNivelacion()
    st.session_state.sistema.cargar_datos_demo()

st.sidebar.title("Menu")
st.sidebar.caption("Sistema de Nivelacion POO")

st.title("Sistema de Nivelacion POO")
st.info("Interfaz web en construccion.")
