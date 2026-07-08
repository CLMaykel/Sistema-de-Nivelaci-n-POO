import streamlit as st


def obtener_opciones_por_rol(rol):
    if rol == "Administrador":
        return [
            "Dashboard",
            "Usuarios",
            "Aulas",
            "Horarios",
            "Cursos",
            "Inscripciones",
            "Cargas Academicas",
            "Reportes",
            "Acerca del Sistema",
        ]

    if rol == "Docente":
        return [
            "Dashboard Docente",
            "Mis Cursos",
            "Mis Horarios",
            "Estudiantes",
            "Reportes Docente",
            "Acerca del Sistema",
        ]

    if rol == "Estudiante":
        return [
            "Dashboard Estudiante",
            "Mis Cursos",
            "Mi Horario",
            "Mi Carga Academica",
            "Mi Perfil",
            "Acerca del Sistema",
        ]

    return []


def navegar_a(opcion):
    """Sincroniza sidebar y contenido al elegir un modulo desde el dashboard."""
    st.session_state.nav_seleccion = opcion
    st.session_state.nav_radio = opcion
    st.rerun()


MODULOS_ADMIN = [
    ("Usuarios", "Gestion de estudiantes, docentes y administradores"),
    ("Aulas", "Registro y consulta de espacios fisicos"),
    ("Horarios", "Planificacion de dias, horas y modalidad"),
    ("Cursos", "Creacion de cursos de nivelacion"),
    ("Inscripciones", "Matricula de estudiantes en cursos"),
    ("Cargas Academicas", "Generacion de carga por periodo"),
    ("Reportes", "Exportacion PDF y Excel"),
]

MODULOS_DOCENTE = [
    ("Mis Cursos", "Consulta de cursos asignados al docente"),
    ("Mis Horarios", "Horarios de los cursos del docente"),
    ("Estudiantes", "Listado, notas y asistencia de estudiantes"),
    ("Reportes Docente", "Resumen academico de sus cursos"),
]

MODULOS_ESTUDIANTE = [
    ("Mis Cursos", "Cursos en los que esta inscrito"),
    ("Mi Horario", "Horario de clases personal"),
    ("Mi Carga Academica", "Asignaturas y creditos del periodo"),
    ("Mi Perfil", "Datos personales, calificaciones y asistencia"),
]
