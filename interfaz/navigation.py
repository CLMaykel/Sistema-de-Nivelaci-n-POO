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
