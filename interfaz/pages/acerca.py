import streamlit as st

from interfaz.branding import (
    FACULTAD,
    MODULO_POO,
    NOMBRE_SISTEMA,
    PERIODO_ACTUAL,
    SIGLAS,
    UNIVERSIDAD,
    encabezado_pagina,
)


def mostrar_acerca(sistema):
    encabezado_pagina("Acerca del sistema")

    st.markdown(
        f"""
        ### {SIGLAS} · {UNIVERSIDAD}

        **{NOMBRE_SISTEMA}** es una aplicacion web desarrollada para la gestion
        academica de procesos de nivelacion en la {FACULTAD}.

        - **Asignatura:** {MODULO_POO}
        - **Periodo academico:** {PERIODO_ACTUAL}
        - **Tecnologia:** Python, POO y Streamlit
        - **Correos institucionales:** dominio `@uleam.edu.ec`

        ### Funcionalidades

        - Gestion de usuarios, aulas, horarios y cursos
        - Inscripciones y cargas academicas
        - Generacion de reportes en PDF y Excel

        ### Patrones POO aplicados

        Herencia, polimorfismo, Factory Method y Strategy.

        ### Acceso por roles

        El sistema utiliza una interfaz diferenciada por roles, permitiendo que
        administradores, docentes y estudiantes accedan unicamente a las funciones
        correspondientes a su perfil. Esta separacion mejora la organizacion, la
        seguridad visual y la experiencia de usuario dentro del sistema academico.
        """
    )

    st.info(f"Institucion: {UNIVERSIDAD} ({SIGLAS})")
