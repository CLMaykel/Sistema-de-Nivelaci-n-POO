import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio, tarjetas_navegacion
from interfaz.components.tables import curso_to_dict
from interfaz.idioma import obtener_gestor_idioma, t
from interfaz.navigation import modulos_admin_traducidos


def mostrar_dashboard(sistema):
    encabezado_pagina(t("dashboard.admin.titulo"), periodo=sistema.periodo_actual)

    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)
    periodo_actual = sistema.obtener_periodo_actual()
    gestor = obtener_gestor_idioma()

    if usuario:
        st.success(
            t(
                "dashboard.admin.sesion_activa",
                nombre=f"{usuario.nombres} {usuario.apellidos}",
                rol=gestor.traducir_rol(rol),
            )
        )
    else:
        st.info(t("dashboard.admin.modo_admin", periodo=sistema.periodo_actual))

    intro_modulo(
        t("dashboard.admin.intro", sistema=t("app.titulo_sistema")),
        "📊",
    )

    if periodo_actual:
        fila_metricas(
            [
                (t("dashboard.periodo_activo"), periodo_actual.nombre),
                (t("dashboard.estado_periodo"), periodo_actual.estado),
                (t("dashboard.periodos_registrados"), len(sistema.periodos)),
            ],
            columnas=3,
        )

    resumen = sistema.resumen()
    fila_metricas(
        [
            (t("dashboard.usuarios"), resumen.get("usuarios", 0)),
            (t("dashboard.docentes"), resumen.get("docentes", 0)),
            (t("dashboard.estudiantes"), resumen.get("estudiantes", 0)),
            (t("dashboard.cursos"), resumen.get("cursos", 0)),
        ]
    )
    fila_metricas(
        [
            (t("dashboard.aulas"), resumen.get("aulas", 0)),
            (t("dashboard.inscripciones"), sistema.total_inscripciones()),
            (t("dashboard.calificaciones"), resumen.get("calificaciones", 0)),
            (t("dashboard.asistencias"), resumen.get("asistencias", 0)),
        ]
    )
    fila_metricas(
        [
            (t("dashboard.cargas_academicas"), resumen.get("cargas", 0)),
            (t("dashboard.reportes"), resumen.get("reportes", 0)),
            (t("dashboard.matriculas"), resumen.get("matriculas", 0)),
        ],
        columnas=3,
    )

    st.divider()
    st.subheader(t("dashboard.admin.modulos_sistema"))
    tarjetas_navegacion(modulos_admin_traducidos(), prefijo_clave="admin")

    st.divider()
    st.subheader(t("dashboard.admin.cursos_activos"))

    if not sistema.cursos:
        st.info(t("dashboard.admin.sin_cursos"))
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos.values()]
    tabla_o_vacio(filas, t("dashboard.admin.sin_cursos_tabla"))
