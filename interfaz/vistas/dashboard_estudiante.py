import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio, tarjetas_navegacion
from interfaz.components.tables import (
    asistencia_registro_to_dict,
    calificacion_registro_to_dict,
    carga_to_dict,
    curso_to_dict,
)
from interfaz.idioma import t
from interfaz.navigation import modulos_estudiante_traducidos


def _cursos_estudiante(sistema, estudiante):
    if not estudiante:
        return []
    return sistema.obtener_cursos_estudiante(estudiante)


def _cargas_estudiante(sistema, estudiante):
    if not estudiante:
        return []
    return [
        carga
        for carga in sistema.cargas_academicas.values()
        if carga.estudiante == estudiante
    ]


def _resumen_estudiante(sistema, estudiante):
    intro_modulo(t("dashboard.estudiante.intro_resumen"), "🎓")
    cursos = _cursos_estudiante(sistema, estudiante)
    cargas = _cargas_estudiante(sistema, estudiante)
    calificaciones = sistema.obtener_calificaciones_estudiante(estudiante)
    asistencias = sistema.obtener_asistencias_estudiante(estudiante)

    fila_metricas(
        [
            (t("dashboard.estudiante.cursos_inscritos"), len(cursos)),
            (t("dashboard.estudiante.estado_nivelacion"), estudiante.estado_nivelacion),
            (t("dashboard.calificaciones"), len(calificaciones)),
            (t("dashboard.asistencias"), len(asistencias)),
        ]
    )
    fila_metricas(
        [
            (t("dashboard.cargas_academicas"), len(cargas)),
            (t("dashboard.periodo_activo"), sistema.periodo_actual),
        ],
        columnas=2,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card(t("dashboard.cursos"), len(cursos))
    with col2:
        metric_card(t("dashboard.estado"), estudiante.estado_nivelacion)
    with col3:
        metric_card(t("dashboard.periodo"), sistema.periodo_actual)

    st.divider()
    st.subheader(t("dashboard.estudiante.accesos_rapidos"))
    tarjetas_navegacion(modulos_estudiante_traducidos(), prefijo_clave="estudiante")


def _consulta_estudiante(sistema, estudiante):
    cursos = _cursos_estudiante(sistema, estudiante)
    cargas = _cargas_estudiante(sistema, estudiante)
    calificaciones = sistema.obtener_calificaciones_estudiante(estudiante)
    asistencias = sistema.obtener_asistencias_estudiante(estudiante)

    st.markdown(f"#### {t('dashboard.estudiante.mis_cursos')}")
    tabla_o_vacio([curso_to_dict(curso) for curso in cursos], t("dashboard.estudiante.sin_cursos"))

    st.markdown(f"#### {t('dashboard.estudiante.mi_carga')}")
    tabla_o_vacio([carga_to_dict(carga) for carga in cargas], t("dashboard.estudiante.sin_carga"))

    st.markdown(f"#### {t('dashboard.estudiante.mis_calificaciones')}")
    tabla_o_vacio(
        [calificacion_registro_to_dict(registro) for registro in calificaciones],
        t("dashboard.estudiante.sin_calificaciones"),
    )

    st.markdown(f"#### {t('dashboard.estudiante.mi_asistencia')}")
    tabla_o_vacio(
        [asistencia_registro_to_dict(registro) for registro in asistencias],
        t("dashboard.estudiante.sin_asistencia"),
    )


def mostrar_dashboard_estudiante(sistema):
    encabezado_pagina(t("dashboard.estudiante.titulo"), periodo=sistema.periodo_actual)

    estudiante = obtener_usuario_actual(sistema)
    if not estudiante:
        st.warning(t("dashboard.estudiante.no_estudiante"))
        return

    st.markdown(
        f"### {t('dashboard.estudiante.bienvenido', nombre=f'{estudiante.nombres} {estudiante.apellidos}')}"
    )

    tab_resumen, tab_consulta = st.tabs(
        [t("dashboard.docente.tab_resumen"), t("dashboard.docente.tab_consulta")]
    )

    with tab_resumen:
        _resumen_estudiante(sistema, estudiante)

    with tab_consulta:
        _consulta_estudiante(sistema, estudiante)
