"""Importacion de datasets universitarios desde archivos CSV."""

import csv
import io
from dataclasses import dataclass, field

from modelos.docente import Docente
from modelos.estudiante import Estudiante


@dataclass
class ResultadoImportacion:
    tipo: str
    total_filas: int
    importadas: int = 0
    omitidas: int = 0
    errores: list[str] = field(default_factory=list)

    @property
    def hubo_exito(self) -> bool:
        return self.importadas > 0


def _normalizar_clave(clave: str) -> str:
    return clave.strip().lower().replace(" ", "_")


def _normalizar_fila(fila: dict) -> dict:
    return {_normalizar_clave(k): (v.strip() if isinstance(v, str) else v) for k, v in fila.items()}


def _parse_bool(valor) -> bool:
    if isinstance(valor, bool):
        return valor
    texto = str(valor or "").strip().lower()
    return texto in ("1", "true", "si", "sí", "yes", "y")


def _valor(fila: dict, *claves, default=""):
    for clave in claves:
        if clave in fila and fila[clave] not in (None, ""):
            return fila[clave]
    return default


def _buscar_aula(sistema, codigo):
    codigo = str(codigo).strip()
    for aula in sistema.aulas.values():
        if aula.codigo == codigo:
            return aula
    raise ValueError(f"Aula no encontrada: {codigo}")


def _buscar_curso(sistema, codigo):
    codigo = str(codigo).strip()
    for curso in sistema.cursos.values():
        if curso.codigo == codigo:
            return curso
    raise ValueError(f"Curso no encontrado: {codigo}")


def _buscar_usuario_cedula(sistema, cedula):
    usuario = sistema.buscar_usuario_por_identificador(str(cedula).strip())
    if not usuario:
        raise ValueError(f"Usuario no encontrado: {cedula}")
    return usuario


def _buscar_docente(sistema, cedula):
    usuario = _buscar_usuario_cedula(sistema, cedula)
    if not isinstance(usuario, Docente):
        raise ValueError(f"La cedula {cedula} no corresponde a un docente")
    return usuario


def _buscar_estudiante(sistema, cedula):
    usuario = _buscar_usuario_cedula(sistema, cedula)
    if not isinstance(usuario, Estudiante):
        raise ValueError(f"La cedula {cedula} no corresponde a un estudiante")
    return usuario


def _buscar_horario(sistema, dia, hora_inicio, hora_fin, grupo, aula_codigo=""):
    dia = str(dia).strip()
    hora_inicio = str(hora_inicio).strip()
    hora_fin = str(hora_fin).strip()
    grupo = str(grupo).strip()
    aula_codigo = str(aula_codigo).strip()

    for horario in sistema.horarios.values():
        coincide = (
            horario.dia == dia
            and horario.hora_inicio == hora_inicio
            and horario.hora_fin == hora_fin
            and horario.grupo == grupo
        )
        if not coincide:
            continue
        if aula_codigo and horario.aula and horario.aula.codigo != aula_codigo:
            continue
        return horario

    clave = f"{dia} {hora_inicio}-{hora_fin} grupo {grupo}"
    raise ValueError(f"Horario no encontrado: {clave}")


CONFIG_TIPOS = {
    "periodos": {
        "orden": 1,
        "columnas_requeridas": ["nombre", "fecha_inicio", "fecha_fin"],
        "columnas_opcionales": ["estado"],
        "descripcion": "Periodos academicos del sistema",
    },
    "docentes": {
        "orden": 2,
        "columnas_requeridas": [
            "cedula",
            "nombres",
            "apellidos",
            "correo",
            "contrasena",
            "telefono",
            "titulo_profesional",
            "especialidad",
        ],
        "columnas_opcionales": [],
        "descripcion": "Docentes de la universidad",
    },
    "estudiantes": {
        "orden": 3,
        "columnas_requeridas": [
            "cedula",
            "nombres",
            "apellidos",
            "correo",
            "contrasena",
            "telefono",
            "tipo_documento",
            "fecha_nacimiento",
        ],
        "columnas_opcionales": ["discapacidad"],
        "descripcion": "Estudiantes de nivelacion",
    },
    "administradores": {
        "orden": 4,
        "columnas_requeridas": [
            "cedula",
            "nombres",
            "apellidos",
            "correo",
            "contrasena",
            "telefono",
            "cargo",
        ],
        "columnas_opcionales": [],
        "descripcion": "Administradores del sistema",
    },
    "aulas": {
        "orden": 5,
        "columnas_requeridas": ["codigo", "nombre", "capacidad", "piso", "edificio"],
        "columnas_opcionales": [],
        "descripcion": "Aulas y espacios fisicos",
    },
    "horarios": {
        "orden": 6,
        "columnas_requeridas": [
            "dia",
            "hora_inicio",
            "hora_fin",
            "modalidad",
            "grupo",
            "aula_codigo",
        ],
        "columnas_opcionales": [],
        "descripcion": "Bloques horarios vinculados a aulas",
    },
    "cursos": {
        "orden": 7,
        "columnas_requeridas": [
            "codigo",
            "nombre",
            "nivel",
            "paralelo",
            "cupo_maximo",
            "docente_cedula",
            "horario_dia",
            "horario_hora_inicio",
            "horario_hora_fin",
            "horario_grupo",
            "aula_codigo",
        ],
        "columnas_opcionales": [],
        "descripcion": "Cursos de nivelacion",
    },
    "matriculas": {
        "orden": 8,
        "columnas_requeridas": ["estudiante_cedula", "curso_codigo"],
        "columnas_opcionales": ["periodo_nombre", "tipo_matricula", "fecha_matricula"],
        "descripcion": "Inscripciones de estudiantes en cursos",
    },
    "cargas_academicas": {
        "orden": 9,
        "columnas_requeridas": ["estudiante_cedula"],
        "columnas_opcionales": ["periodo_nombre"],
        "descripcion": "Cargas academicas por estudiante y periodo",
    },
    "calificaciones": {
        "orden": 10,
        "columnas_requeridas": [
            "docente_cedula",
            "curso_codigo",
            "estudiante_cedula",
            "parcial1",
            "parcial2",
        ],
        "columnas_opcionales": ["observacion"],
        "descripcion": "Notas parciales por estudiante y curso",
    },
    "asistencias": {
        "orden": 11,
        "columnas_requeridas": [
            "docente_cedula",
            "curso_codigo",
            "estudiante_cedula",
            "fecha",
            "estado",
        ],
        "columnas_opcionales": ["observacion"],
        "descripcion": "Registro de asistencia",
    },
}

PLANTILLAS_CSV = {
    "periodos": (
        "nombre,fecha_inicio,fecha_fin,estado\n"
        "2026-1,2026-01-01,2026-06-30,Abierto\n"
    ),
    "docentes": (
        "cedula,nombres,apellidos,correo,contrasena,telefono,titulo_profesional,especialidad\n"
        "1400006666,Maria,Gomez,mgomez@uleam.edu.ec,doc789,0994445566,Licenciada,Programacion OO\n"
    ),
    "estudiantes": (
        "cedula,nombres,apellidos,correo,contrasena,telefono,tipo_documento,fecha_nacimiento,discapacidad\n"
        "1400005555,Ana,Lopez,alopez@uleam.edu.ec,est789,0991112233,Cedula,2005-01-10,false\n"
    ),
    "administradores": (
        "cedula,nombres,apellidos,correo,contrasena,telefono,cargo\n"
        "1400007777,Luis,Ramirez,lramirez@uleam.edu.ec,adm789,0998887766,Coordinador\n"
    ),
    "aulas": (
        "codigo,nombre,capacidad,piso,edificio\n"
        "B201,Aula 201,40,2,Bloque B\n"
    ),
    "horarios": (
        "dia,hora_inicio,hora_fin,modalidad,grupo,aula_codigo\n"
        "Martes,10:00,12:00,Presencial,A,B201\n"
    ),
    "cursos": (
        "codigo,nombre,nivel,paralelo,cupo_maximo,docente_cedula,horario_dia,horario_hora_inicio,"
        "horario_hora_fin,horario_grupo,aula_codigo\n"
        "POO-002,Programacion OO II,Nivelacion,B,25,1400006666,Martes,10:00,12:00,A,B201\n"
    ),
    "matriculas": (
        "estudiante_cedula,curso_codigo,periodo_nombre,tipo_matricula,fecha_matricula\n"
        "1400005555,POO-002,2026-1,Regular,2026-01-15\n"
    ),
    "cargas_academicas": (
        "estudiante_cedula,periodo_nombre\n"
        "1400005555,2026-1\n"
    ),
    "calificaciones": (
        "docente_cedula,curso_codigo,estudiante_cedula,parcial1,parcial2,observacion\n"
        "1400006666,POO-002,1400005555,8.0,9.0,Buen trabajo\n"
    ),
    "asistencias": (
        "docente_cedula,curso_codigo,estudiante_cedula,fecha,estado,observacion\n"
        "1400006666,POO-002,1400005555,2026-03-15,Presente,\n"
    ),
}


def listar_tipos_entidad():
    return sorted(CONFIG_TIPOS.keys(), key=lambda t: CONFIG_TIPOS[t]["orden"])


def obtener_config_tipo(tipo: str) -> dict:
    if tipo not in CONFIG_TIPOS:
        raise ValueError(f"Tipo de entidad no soportado: {tipo}")
    return CONFIG_TIPOS[tipo]


def obtener_plantilla_csv(tipo: str) -> str:
    if tipo not in PLANTILLAS_CSV:
        raise ValueError(f"No hay plantilla para el tipo: {tipo}")
    return PLANTILLAS_CSV[tipo]


def leer_csv(contenido) -> list[dict]:
    if isinstance(contenido, bytes):
        texto = contenido.decode("utf-8-sig")
    else:
        texto = str(contenido)

    if not texto.strip():
        return []

    lector = csv.DictReader(io.StringIO(texto))
    if not lector.fieldnames:
        return []

    filas = []
    for indice, fila in enumerate(lector, start=2):
        normalizada = _normalizar_fila(fila)
        if any(str(v).strip() for v in normalizada.values()):
            normalizada["_fila_csv"] = indice
            filas.append(normalizada)
    return filas


def validar_columnas(filas: list[dict], tipo: str) -> list[str]:
    config = obtener_config_tipo(tipo)
    if not filas:
        return ["El archivo CSV no contiene filas de datos."]

    faltantes = [
        col
        for col in config["columnas_requeridas"]
        if col not in filas[0]
    ]
    if faltantes:
        return [f"Faltan columnas requeridas: {', '.join(faltantes)}"]
    return []


def _importar_periodo(sistema, fila):
    sistema.registrar_periodo(
        _valor(fila, "nombre"),
        _valor(fila, "fecha_inicio"),
        _valor(fila, "fecha_fin"),
        _valor(fila, "estado", default="Abierto") or "Abierto",
    )


def _importar_docente(sistema, fila):
    sistema.registrar_usuario(
        "Docente",
        _valor(fila, "cedula"),
        _valor(fila, "nombres"),
        _valor(fila, "apellidos"),
        _valor(fila, "correo"),
        _valor(fila, "contrasena"),
        _valor(fila, "telefono"),
        titulo_profesional=_valor(fila, "titulo_profesional"),
        especialidad=_valor(fila, "especialidad"),
    )


def _importar_estudiante(sistema, fila):
    sistema.registrar_usuario(
        "Estudiante",
        _valor(fila, "cedula"),
        _valor(fila, "nombres"),
        _valor(fila, "apellidos"),
        _valor(fila, "correo"),
        _valor(fila, "contrasena"),
        _valor(fila, "telefono"),
        tipo_documento=_valor(fila, "tipo_documento", default="Cedula") or "Cedula",
        fecha_nacimiento=_valor(fila, "fecha_nacimiento"),
        discapacidad=_parse_bool(_valor(fila, "discapacidad", default="false")),
    )


def _importar_administrador(sistema, fila):
    sistema.registrar_usuario(
        "Administrador",
        _valor(fila, "cedula"),
        _valor(fila, "nombres"),
        _valor(fila, "apellidos"),
        _valor(fila, "correo"),
        _valor(fila, "contrasena"),
        _valor(fila, "telefono"),
        cargo=_valor(fila, "cargo"),
    )


def _importar_aula(sistema, fila):
    sistema.registrar_aula(
        _valor(fila, "codigo"),
        _valor(fila, "nombre"),
        _valor(fila, "capacidad"),
        _valor(fila, "piso"),
        _valor(fila, "edificio"),
    )


def _importar_horario(sistema, fila):
    aula = _buscar_aula(sistema, _valor(fila, "aula_codigo"))
    sistema.registrar_horario(
        _valor(fila, "dia"),
        _valor(fila, "hora_inicio"),
        _valor(fila, "hora_fin"),
        _valor(fila, "modalidad"),
        _valor(fila, "grupo"),
        aula,
    )


def _importar_curso(sistema, fila):
    docente = _buscar_docente(sistema, _valor(fila, "docente_cedula"))
    aula = _buscar_aula(sistema, _valor(fila, "aula_codigo"))
    horario = _buscar_horario(
        sistema,
        _valor(fila, "horario_dia"),
        _valor(fila, "horario_hora_inicio"),
        _valor(fila, "horario_hora_fin"),
        _valor(fila, "horario_grupo"),
        _valor(fila, "aula_codigo"),
    )
    sistema.registrar_curso(
        _valor(fila, "codigo"),
        _valor(fila, "nombre"),
        _valor(fila, "nivel"),
        _valor(fila, "paralelo"),
        _valor(fila, "cupo_maximo"),
        docente,
        horario,
        aula,
    )


def _importar_matricula(sistema, fila):
    estudiante = _buscar_estudiante(sistema, _valor(fila, "estudiante_cedula"))
    curso = _buscar_curso(sistema, _valor(fila, "curso_codigo"))
    periodo = _valor(fila, "periodo_nombre") or None
    tipo_matricula = _valor(fila, "tipo_matricula", default="Regular") or "Regular"
    fecha = _valor(fila, "fecha_matricula") or None
    sistema.inscribir_estudiante(
        curso,
        estudiante,
        periodo=periodo,
        tipo_matricula=tipo_matricula,
        fecha=fecha,
    )


def _importar_carga(sistema, fila):
    estudiante = _buscar_estudiante(sistema, _valor(fila, "estudiante_cedula"))
    periodo = _valor(fila, "periodo_nombre") or None
    sistema.registrar_carga_academica(estudiante, periodo=periodo)


def _importar_calificacion(sistema, fila):
    docente = _buscar_docente(sistema, _valor(fila, "docente_cedula"))
    curso = _buscar_curso(sistema, _valor(fila, "curso_codigo"))
    estudiante = _buscar_estudiante(sistema, _valor(fila, "estudiante_cedula"))
    sistema.registrar_calificacion(
        docente,
        curso,
        estudiante,
        _valor(fila, "parcial1"),
        _valor(fila, "parcial2"),
        observacion=_valor(fila, "observacion"),
    )


def _importar_asistencia(sistema, fila):
    docente = _buscar_docente(sistema, _valor(fila, "docente_cedula"))
    curso = _buscar_curso(sistema, _valor(fila, "curso_codigo"))
    estudiante = _buscar_estudiante(sistema, _valor(fila, "estudiante_cedula"))
    sistema.registrar_asistencia(
        docente,
        curso,
        estudiante,
        _valor(fila, "fecha"),
        _valor(fila, "estado"),
        observacion=_valor(fila, "observacion"),
    )


_IMPORTADORES = {
    "periodos": _importar_periodo,
    "docentes": _importar_docente,
    "estudiantes": _importar_estudiante,
    "administradores": _importar_administrador,
    "aulas": _importar_aula,
    "horarios": _importar_horario,
    "cursos": _importar_curso,
    "matriculas": _importar_matricula,
    "cargas_academicas": _importar_carga,
    "calificaciones": _importar_calificacion,
    "asistencias": _importar_asistencia,
}


def importar_filas(sistema, tipo: str, filas: list[dict]) -> ResultadoImportacion:
    if tipo not in _IMPORTADORES:
        raise ValueError(f"Tipo de entidad no soportado: {tipo}")

    resultado = ResultadoImportacion(tipo=tipo, total_filas=len(filas))
    errores_columnas = validar_columnas(filas, tipo)
    if errores_columnas:
        resultado.errores.extend(errores_columnas)
        return resultado

    importador = _IMPORTADORES[tipo]
    for fila in filas:
        numero = fila.get("_fila_csv", "?")
        try:
            importador(sistema, fila)
            resultado.importadas += 1
        except Exception as error:
            resultado.omitidas += 1
            resultado.errores.append(f"Fila {numero}: {error}")

    return resultado
