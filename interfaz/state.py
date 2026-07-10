import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from servicios.sistema_nivelacion import SistemaNivelacion


def get_sistema():
    # Obtiene o inicializa la instancia del sistema de nivelación en la sesión
    if "sistema" not in st.session_state:
        sistema = SistemaNivelacion()
        ok, mensaje, modo = sistema.inicializar_datos()
        st.session_state.sistema = sistema
        st.session_state.db_cargada = ok
        st.session_state.modo_datos = modo
        st.session_state.db_mensaje = mensaje
    return st.session_state.sistema
