import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio, tarjetas_navegacion
from interfaz.components.tables import calificacion_registro_to_dict, curso_to_dict
from interfaz.idioma import t
from interfaz.navigation import modulos_docente_traducidos


def _cursos_docente(sistema, docente):
    if not docente:
        return []
    return [curso for curso in sistema.cursos.values() if curso.docente == docente]


def _resumen_docente(sistema, docente):
    intro_modulo(t("dashboard.docente.intro_resumen"), "👨‍🏫")
    cursos = _cursos_docente(sistema, docente)
    total_estudiantes = sum(len(curso.lista_estudiantes) for curso in cursos)
    calificaciones = [
        registro
        for registro in sistema.calificaciones.values()
        if registro["docente"] == docente
    ]
    asistencias = [
        registro for registro in sistema.asistencias.values() if registro["docente"] == docente
    ]

    fila_metricas(
        [
            (t("dashboard.docente.cursos_asignados"), len(cursos)),
            (t("dashboard.estudiantes"), total_estudiantes),
            (t("dashboard.calificaciones"), len(calificaciones)),
            (t("dashboard.asistencias"), len(asistencias)),
        ]
    )
    fila_metricas(
        [
            (t("dashboard.periodo_activo"), sistema.periodo_actual),
            (t("dashboard.docente.titulo_profesional"), docente.titulo_profesional),
            (t("dashboard.docente.especialidad"), docente.especialidad),
        ],
        columnas=3,
    )


def _consulta_docente(sistema, docente):
    cursos = _cursos_docente(sistema, docente)
    if not cursos:
        st.info(t("dashboard.docente.sin_cursos"))
        return

    st.markdown(f"#### {t('dashboard.docente.cursos_asignados')}")
    tabla_o_vacio([curso_to_dict(curso) for curso in cursos], t("dashboard.docente.sin_cursos"))

    calificaciones = [
        calificacion_registro_to_dict(registro)
        for registro in sistema.calificaciones.values()
        if registro["docente"] == docente
    ]
    st.markdown(f"#### {t('dashboard.docente.calificaciones_registradas')}")
    tabla_o_vacio(calificaciones, t("dashboard.docente.sin_calificaciones"))


def mostrar_dashboard_docente(sistema):
    encabezado_pagina(t("dashboard.docente.titulo"), periodo=sistema.periodo_actual)

    docente = obtener_usuario_actual(sistema)
    if not docente:
        st.warning(t("dashboard.docente.no_docente"))
        return

    st.markdown(
        f"### {t('dashboard.docente.bienvenido', nombre=f'{docente.nombres} {docente.apellidos}')}"
    )

    tab_resumen, tab_consulta = st.tabs(
        [t("dashboard.docente.tab_resumen"), t("dashboard.docente.tab_consulta")]
    )

    with tab_resumen:
        _resumen_docente(sistema, docente)
        cursos = _cursos_docente(sistema, docente)
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card(t("dashboard.cursos"), len(cursos))
        with col2:
            metric_card(t("dashboard.estudiantes"), sum(len(c.lista_estudiantes) for c in cursos))
        with col3:
            metric_card(t("dashboard.periodo"), sistema.periodo_actual)

        st.divider()
        st.subheader(t("dashboard.docente.accesos_rapidos"))
        tarjetas_navegacion(modulos_docente_traducidos(), prefijo_clave="docente")

    with tab_consulta:
        _consulta_docente(sistema, docente)
