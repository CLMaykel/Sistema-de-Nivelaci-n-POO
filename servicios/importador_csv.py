"""Importacion de datasets universitarios desde un CSV unificado acoplado."""

import csv
import io
from collections import defaultdict
from dataclasses import dataclass, field

from modelos.docente import Docente
from modelos.estudiante import Estudiante

ORDEN_TIPOS_REGISTRO = [
    "periodo",
    "docente",
    "estudiante",
    "administrador",
    "aula",
    "horario",
    "curso",
    "matricula",
    "carga_academica",
    "calificacion",
    "asistencia",
]

COLUMNAS_MODELO = [
    "tipo_registro",
    "periodo_nombre",
    "fecha_inicio",
    "fecha_fin",
    "estado_periodo",
    "cedula",
    "nombres",
    "apellidos",
    "correo",
    "contrasena",
    "telefono",
    "titulo_profesional",
    "especialidad",
    "cargo",
    "tipo_documento",
    "fecha_nacimiento",
    "discapacidad",
    "codigo_aula",
    "nombre_aula",
    "capacidad",
    "piso",
    "edificio",
    "dia",
    "hora_inicio",
    "hora_fin",
    "modalidad",
    "grupo",
    "aula_codigo",
    "codigo_curso",
    "nombre_curso",
    "nivel",
    "paralelo",
    "cupo_maximo",
    "docente_cedula",
    "horario_dia",
    "horario_hora_inicio",
    "horario_hora_fin",
    "horario_grupo",
    "aula_codigo_curso",
    "estudiante_cedula",
    "curso_codigo",
    "tipo_matricula",
    "fecha_matricula",
    "parcial1",
    "parcial2",
    "observacion_nota",
    "fecha_asistencia",
    "estado_asistencia",
    "observacion_asistencia",
]

TIPOS_REGISTRO_VALIDOS = set(ORDEN_TIPOS_REGISTRO)


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


@dataclass
class ResultadoImportacionDataset:
    total_filas: int
    importadas: int = 0
    omitidas: int = 0
    errores: list[str] = field(default_factory=list)
    resumen_por_tipo: dict[str, dict] = field(default_factory=dict)

    @property
    def hubo_exito(self) -> bool:
        return self.importadas > 0 and not self.errores


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


def obtener_plantilla_csv() -> str:
    return ",".join(COLUMNAS_MODELO) + "\n"


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
        if any(str(v).strip() for k, v in normalizada.items() if k != "_fila_csv"):
            normalizada["_fila_csv"] = indice
            filas.append(normalizada)
    return filas


def contar_por_tipo(filas: list[dict]) -> dict[str, int]:
    conteo = defaultdict(int)
    for fila in filas:
        tipo = _valor(fila, "tipo_registro")
        if tipo:
            conteo[tipo] += 1
    return dict(conteo)


def validar_modelo_dataset(filas: list[dict]) -> list[str]:
    if not filas:
        return ["El archivo CSV no contiene filas de datos."]

    errores = []
    if "tipo_registro" not in filas[0]:
        return ["Falta la columna requerida: tipo_registro"]

    for fila in filas:
        numero = fila.get("_fila_csv", "?")
        tipo = _valor(fila, "tipo_registro")
        if not tipo:
            errores.append(f"Fila {numero}: tipo_registro vacio")
        elif tipo not in TIPOS_REGISTRO_VALIDOS:
            errores.append(f"Fila {numero}: tipo_registro invalido '{tipo}'")
    return errores


def _importar_periodo(sistema, fila):
    sistema.registrar_periodo(
        _valor(fila, "periodo_nombre", "nombre"),
        _valor(fila, "fecha_inicio"),
        _valor(fila, "fecha_fin"),
        _valor(fila, "estado_periodo", "estado", default="Abierto") or "Abierto",
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
        _valor(fila, "codigo_aula", "codigo"),
        _valor(fila, "nombre_aula", "nombre"),
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
    aula_codigo = _valor(fila, "aula_codigo_curso", "aula_codigo")
    aula = _buscar_aula(sistema, aula_codigo)
    horario = _buscar_horario(
        sistema,
        _valor(fila, "horario_dia"),
        _valor(fila, "horario_hora_inicio"),
        _valor(fila, "horario_hora_fin"),
        _valor(fila, "horario_grupo"),
        aula_codigo,
    )
    sistema.registrar_curso(
        _valor(fila, "codigo_curso", "codigo"),
        _valor(fila, "nombre_curso", "nombre"),
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
        observacion=_valor(fila, "observacion_nota", "observacion"),
    )


def _importar_asistencia(sistema, fila):
    docente = _buscar_docente(sistema, _valor(fila, "docente_cedula"))
    curso = _buscar_curso(sistema, _valor(fila, "curso_codigo"))
    estudiante = _buscar_estudiante(sistema, _valor(fila, "estudiante_cedula"))
    sistema.registrar_asistencia(
        docente,
        curso,
        estudiante,
        _valor(fila, "fecha_asistencia", "fecha"),
        _valor(fila, "estado_asistencia", "estado"),
        observacion=_valor(fila, "observacion_asistencia", "observacion"),
    )


_IMPORTADORES = {
    "periodo": _importar_periodo,
    "docente": _importar_docente,
    "estudiante": _importar_estudiante,
    "administrador": _importar_administrador,
    "aula": _importar_aula,
    "horario": _importar_horario,
    "curso": _importar_curso,
    "matricula": _importar_matricula,
    "carga_academica": _importar_carga,
    "calificacion": _importar_calificacion,
    "asistencia": _importar_asistencia,
}


def _importar_grupo(sistema, tipo: str, filas: list[dict]) -> ResultadoImportacion:
    resultado = ResultadoImportacion(tipo=tipo, total_filas=len(filas))
    importador = _IMPORTADORES[tipo]

    for fila in filas:
        numero = fila.get("_fila_csv", "?")
        try:
            importador(sistema, fila)
            resultado.importadas += 1
        except Exception as error:
            resultado.omitidas += 1
            resultado.errores.append(f"[{tipo}] Fila {numero}: {error}")

    return resultado


def importar_dataset(sistema, filas: list[dict]) -> ResultadoImportacionDataset:
    resultado = ResultadoImportacionDataset(total_filas=len(filas))
    errores_modelo = validar_modelo_dataset(filas)
    if errores_modelo:
        resultado.errores.extend(errores_modelo)
        return resultado

    agrupadas: dict[str, list[dict]] = defaultdict(list)
    for fila in filas:
        agrupadas[_valor(fila, "tipo_registro")].append(fila)

    for tipo in ORDEN_TIPOS_REGISTRO:
        filas_tipo = agrupadas.get(tipo, [])
        if not filas_tipo:
            continue

        parcial = _importar_grupo(sistema, tipo, filas_tipo)
        resultado.importadas += parcial.importadas
        resultado.omitidas += parcial.omitidas
        resultado.errores.extend(parcial.errores)
        resultado.resumen_por_tipo[tipo] = {
            "total": parcial.total_filas,
            "importadas": parcial.importadas,
            "omitidas": parcial.omitidas,
        }

    return resultado
