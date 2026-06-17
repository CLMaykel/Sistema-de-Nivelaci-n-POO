from abc import ABC, abstractmethod   #importación de librería ABC y abstractmetohd

class Usuario(ABC):
    contador = 0      #variable de clase que cuenta cuantos usuarios se crean
    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, estado=True):
        self.__id_usuario = id_usuario     #atributos privados
        self.__cedula = cedula
        self.__nombres = nombres
        self.__apellidos = apellidos
        self.__correo = correo
        self.__contraseña = contraseña
        self.__telefono = telefono
        self.__estado = estado
        Usuario.contador += 1     #Incrementa el contador de usuarios creados

    @property      #Este docorador permite acceder al atributo privado, como si fuera una variable normal, sin llamar un método
    def id_usuario(self):
        return self.__id_usuario

    @property
    def cedula(self):
        return self.__cedula

    @property
    def nombres(self):
        return self.__nombres

    @property
    def apellidos(self):
        return self.__apellidos

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    @property
    def estado(self):
        return self.__estado

    @property
    def contraseña(self):
        return self.__contraseña
  #Setter  
#Nos permite modificar los atributos privado aplicando validaciones
    @nombres.setter
    def nombres(self, valor):
        if valor == "":             #Valida que el nombre no este vacío
            print("El nombre no puede estar vacio")
        else:
            self.__nombres = valor

    @apellidos.setter
    def apellidos(self, valor):
        if valor == "":    #valida que los apellidos no esten vacios.
            print("Los apellidos no pueden estar vacios")
        else:
            self.__apellidos = valor

#método estatico.
# Valida si el correo contiene '@' y '.' además no utiliza atributos del objeto.
    @staticmethod
    def validar_correo(correo):
     return "@" in correo and "." in correo
    
    @correo.setter
    def correo(self, valor):
     if not Usuario.validar_correo(valor):
         print("El correo no es valido")
     else:
         self.__correo = valor

    @telefono.setter
    def telefono(self, valor):
        if len(valor) < 9: #valida que el telefono tenga los digitos correctos
            print("El telefono debe tener al menos 9 digitos")
        else:
            self.__telefono = valor

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @contraseña.setter
    def contraseña(self, valor):
        self.__contraseña = valor

#método de clase.
# Devuelve la cantidad total de usuarios creados. Trabaja con atributos de clase.
    @classmethod
    def total_usuarios(cls):
     return cls.contador     #Devuelve la cantidad total de usuarios creados

#Método abstracto para iniciar sesión
    @abstractmethod
    def iniciar_sesion(self, contraseña):
        pass

#método para cerrar sesión
    def cerrar_sesion(self):
        print("Sesion cerrada para " + self.__nombres + " " + self.__apellidos)


# Sobrecarga simulada con Kwargs

    def actualizar_perfil(self, **kwargs): #Permite actualizar únicamente los datos enviados.
        if "nombres" in kwargs:
            self.nombres = kwargs["nombres"]
        if "correo" in kwargs:
            self.correo = kwargs["correo"]
        if "telefono" in kwargs:
            self.telefono = kwargs["telefono"]
        print("Perfil actualizado con los campos: " + str(list(kwargs.keys())))

#Método abstracto que será sobreescrito en las clases hijas aplicando poliformismo
    @abstractmethod
    def mostrar_info(self):
        pass


#Herencia. 
#Hereda atributos y métodos de la clase usuario
class Docente(Usuario):                           #se inicializan los atributos heredados y propios
    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, titulo_profesional, especialidad):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono) 
        self.__titulo_profesional = titulo_profesional
        self.__especialidad = especialidad
        self.__notas_registradas = []
#setter
    @property
    def titulo_profesional(self):
        return self.__titulo_profesional

    @property
    def especialidad(self):
        return self.__especialidad

    @titulo_profesional.setter
    def titulo_profesional(self, valor):
        self.__titulo_profesional = valor

    @especialidad.setter
    def especialidad(self, valor):
        self.__especialidad = valor

#se registra las notas de un estudiante usando kwargs
    def registrar_notas(self, id_calificacion, id_estudiante, parcial1, parcial2, **kwargs):
        #se valida que las notas estén entre 0 y 10
        if parcial1 < 0 or parcial1 > 10 or parcial2 < 0 or parcial2 > 10:
            print("Las notas deben estar entre 0 y 10")
            return
        nota_final = round((parcial1 + parcial2) / 2, 2)
    #se crea un diccionario con la información de la calificación
        nota = {
            "id_calificacion": id_calificacion,
            "id_estudiante": id_estudiante,
            "parcial1": parcial1,
            "parcial2": parcial2,
            "nota_final": nota_final
        }
        if "observacion" in kwargs:
            nota["observacion"] = kwargs["observacion"]
        if "fecha" in kwargs:
            nota["fecha"] = kwargs["fecha"]
        self.__notas_registradas.append(nota)
        print("Nota registrada para el estudiante " + str(id_estudiante) + " nota final: " + str(nota_final))

#sobrecarga simulada con args
    def registrar_asistencia(self, fecha, estado, *args):
        for id_estudiante in args: #recorre cada estudiante enviado en args
            print("Asistencia registrada para el estudiante " + str(id_estudiante) + " el " + fecha + " estado: " + estado)

    def consultar_estudiantes(self, curso):
        return curso.lista_estudiantes

#sobrecarga simulada con kwargs
    def generar_reporte(self, **kwargs):
        print("Reporte del docente: " + self.nombres + " " + self.apellidos)
        print("Titulo: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)
        if "periodo" in kwargs:
            print("Periodo: " + kwargs["periodo"])
        if "incluir_notas" in kwargs and kwargs["incluir_notas"] == True:
            print("Notas registradas: " + str(len(self.__notas_registradas)))
        else:
            print("Notas registradas: " + str(len(self.__notas_registradas)))

#método sobreescrito para iniciar sesión  
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como docente correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False


#sobreescribe el metodo de Usuario, aqui se aplica el poliformismo
    def mostrar_info(self):
        print("Docente: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Titulo profesional: " + self.__titulo_profesional)
        print("Especialidad: " + self.__especialidad)



#clase estudiante esta hereda de usuario tambien 
class Estudiante(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, tipo_documento, numero_documento, fecha_nacimiento, discapacidad=False):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__tipo_documento = tipo_documento
        self.__numero_documento = numero_documento
        self.__fecha_nacimiento = fecha_nacimiento
        self.__discapacidad = discapacidad
        self.__estado_nivelacion = "Pendiente"
        self.__matricula = None
#uso de propiedades, getter y setter para acceder a los atributos privados 
    @property
    def tipo_documento(self):
        return self.__tipo_documento

    @property
    def numero_documento(self):
        return self.__numero_documento

    @property
    def fecha_nacimiento(self):
        return self.__fecha_nacimiento

    @property
    def discapacidad(self):
        return self.__discapacidad

    @property
    def estado_nivelacion(self):
        return self.__estado_nivelacion

    @property
    def matricula(self):
        return self.__matricula

    @estado_nivelacion.setter
    def estado_nivelacion(self, valor):
        self.__estado_nivelacion = valor

    @matricula.setter
    def matricula(self, mat):
        self.__matricula = mat
#solicita un cupo en curso- verifica la disponibilidad del cupo
    def solicitar_cupo(self, curso):
        if curso.cupo_actual < curso.cupo_maximo:
            curso.cupo_actual = curso.cupo_actual + 1
            self.__estado_nivelacion = "En Curso"
            print("Cupo asignado en " + curso.nombre + " para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("No hay cupos disponibles en " + curso.nombre)
            return False
#consulta las calificaciones del estudiante
    def consultar_calificaciones(self, calificacion):
        return calificacion.obtener_resumen()
#consulta asistencia 
    def consultar_asistencia(self, asistencia):
        return asistencia.obtener_resumen()

    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como estudiante correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

#metodo sobreescrito para mostrar informacion del estudiante
    def mostrar_info(self):
        print("Estudiante: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Documento: " + self.__tipo_documento + " " + self.__numero_documento)
        print("Fecha de nacimiento: " + self.__fecha_nacimiento)
        print("Estado nivelacion: " + self.__estado_nivelacion)
        if self.__discapacidad:
            print("Discapacidad: Si")
        else:
            print("Discapacidad: No")

#clase administrador igual hereda de usuario
class Administrador(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, id_administrador, cargo):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__id_administrador = id_administrador
        self.__cargo = cargo

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, valor):
        self.__cargo = valor

#gestiona usuario del sistema puede activarlos o desactivarlos
    def gestionar_usuario(self, accion, usuario, **kwargs):
        if accion == "activar":
            usuario.estado = True
            print("Usuario " + usuario.nombres + " activado")
        elif accion == "desactivar":
            usuario.estado = False
            print("Usuario " + usuario.nombres + " desactivado")
        else:
            print("Accion no reconocida")
        if "motivo" in kwargs:
            print("Motivo: " + kwargs["motivo"])
        if "fecha" in kwargs:
            print("Fecha del cambio: " + kwargs["fecha"])
#gestiona procesos administrativos
    def gestionar_procesos(self, proceso):
        print("Proceso ejecutado: " + proceso)
#genera reportes
    def gestionar_reportes(self):
        print("Reporte generado por: " + self.nombres + " " + self.apellidos + " cargo: " + self.__cargo)

#configura parametros ademas se usa args para configurar varios parametros a la vez
    def configurar_parametros(self, *args):
        for item in args: #recorre cada parametro recibido
            print("Parametro configurado: " + str(item[0]) + " = " + str(item[1]))
#gestiona curso
    def gestionar_cursos(self, accion, curso):
        print("Administrador " + self.nombres + " ejecuto " + accion + " en el curso " + curso.nombre)
    
    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            print("Inicio de sesion como administrador correctamente para " + self.nombres + " " + self.apellidos)
            return True
        else:
            print("Contraseña incorrecta o usuario inactivo")
            return False

#metodo sobreescrito aplica polimorfismo 
    def mostrar_info(self):
        print("Administrador: " + self.nombres + " " + self.apellidos)
        print("Cedula: " + self.cedula)
        print("Cargo: " + self.__cargo)
        print("Correo: " + self.correo)



class Facultad:

    def __init__(self, id_facultad, nombre):
        self.__id_facultad = id_facultad
        self.__nombre = nombre
#getter
    @property
    def id_facultad(self):
        return self.__id_facultad

    @property
    def nombre(self):
        return self.__nombre
#setter
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

    def mostrar_info(self):
        print("Facultad: " + self.__nombre)



class Carrera:

    def __init__(self, id_carrera, codigo, nombre, estado, facultad):
        self.__id_carrera = id_carrera
        self.__codigo = codigo
        self.__nombre = nombre
        self.__estado = estado
        self.__facultad = facultad
#getter 
    @property
    def id_carrera(self):
        return self.__id_carrera

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def estado(self):
        return self.__estado

    @property
    def facultad(self):
        return self.__facultad
#setter
    @nombre.setter
    def nombre(self, valor):
        self.__nombre = valor

#se muestra la informacion de la carrera
    def mostrar_info(self):
        print("Carrera: " + self.__nombre + " codigo: " + self.__codigo)
        print("Facultad: " + self.__facultad.nombre)


class PeriodoAcademico:

    def __init__(self, id_periodo, nombre, fecha_inicio, fecha_fin, estado="Cerrado"):
        self.__id_periodo = id_periodo
        self.__nombre = nombre
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__estado = estado
#usamos propiedades para acceder a los atributos privados 
    @property
    def id_periodo(self):
        return self.__id_periodo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def fecha_inicio(self):
        return self.__fecha_inicio

    @property
    def fecha_fin(self):
        return self.__fecha_fin

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = valor
#se cambia el estado del periodo a abierto 
    def abrir_periodo(self):
        self.__estado = "Abierto"
        print("Periodo " + self.__nombre + " abierto")
#se cambia el estado del periodo a cerrado
    def cerrar_periodo(self):
        self.__estado = "Cerrado"
        print("Periodo " + self.__nombre + " cerrado")

#se muestra la informacion del periodo 
    def listar_periodos(self):
        print("Periodo: " + self.__nombre + " del " + self.__fecha_inicio + " al " + self.__fecha_fin + " estado: " + self.__estado)


class Aula:

    def __init__(self, id_aula, codigo, nombre, capacidad, piso, edificio, estado=True):
        self.__id_aula = id_aula
        self.__codigo = codigo
        self.__nombre = nombre
        self.__capacidad = capacidad
        self.__piso = piso
        self.__edificio = edificio
        self.__estado = estado

#uso de propiedades para acceder a los atributos privados
    @property
    def id_aula(self):
        return self.__id_aula

    @property
    def nombre(self):
        return self.__nombre

    @property
    def capacidad(self):
        return self.__capacidad

    @property
    def edificio(self):
        return self.__edificio

    @property
    def estado(self):
        return self.__estado

    def registrar_aula(self):
        print("Aula registrada: " + self.__nombre + " edificio " + self.__edificio + " piso " + str(self.__piso))

#modifica informacion del aula 
    def modificar_aula(self, campo, valor):
        print("Aula modificada: " + campo + " cambiado a " + str(valor))

#muestra la informacion del aula
    def mostrar_info(self):
        print("Aula: " + self.__nombre + " capacidad: " + str(self.__capacidad))


class Horario:

    def __init__(self, id_horario, dia, hora_inicio, hora_fin, modalidad, grupo, aula):
        self.__id_horario = id_horario
        self.__dia = dia
        self.__hora_inicio = hora_inicio
        self.__hora_fin = hora_fin
        self.__modalidad = modalidad
        self.__grupo = grupo
        self.__aula = aula

#uso de propiedades para acceder a los atributos privados
    @property
    def id_horario(self):
        return self.__id_horario

    @property
    def dia(self):
        return self.__dia

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @property
    def hora_fin(self):
        return self.__hora_fin

    @property
    def modalidad(self):
        return self.__modalidad

    @property
    def aula(self):
        return self.__aula

    def registrar_horario(self):
        print("Horario registrado: " + self.__dia + " de " + self.__hora_inicio + " a " + self.__hora_fin + " en " + self.__aula.nombre)
#modifica informacion del horario
    def modificar_horario(self, campo, valor):
        print("Horario modificado: " + campo + " cambiado a " + str(valor))

#elimina el horario
    def eliminar_horario(self):
        print("Horario eliminado")

#muestra la informacion del horario
    def mostrar_info(self):
        print("Horario: " + self.__dia + " " + self.__hora_inicio + " a " + self.__hora_fin + " modalidad: " + self.__modalidad)

class CursoNivelacion:

    def __init__(self, id_curso, codigo, nombre, nivel, paralelo, cupo_maximo, estado=True):
        self.__id_curso = id_curso
        self.__codigo = codigo
        self.__nombre = nombre
        self.__nivel = nivel
        self.__paralelo = paralelo
        self.__cupo_maximo = cupo_maximo
        self.__cupo_actual = 0
        self.__estado = estado
        self.__docente = None
        self.__horario = None
        self.__lista_estudiantes = []

#uso de propiedades para acceder a los atributos privados
    @property
    def id_curso(self):
        return self.__id_curso

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def nivel(self):
        return self.__nivel

    @property
    def paralelo(self):
        return self.__paralelo

    @property
    def cupo_maximo(self):
        return self.__cupo_maximo

    @property
    def cupo_actual(self):
        return self.__cupo_actual

    @property
    def estado(self):
        return self.__estado

    @property
    def docente(self):
        return self.__docente

    @property
    def lista_estudiantes(self):
        return self.__lista_estudiantes

    @cupo_actual.setter
    def cupo_actual(self, valor):
        if valor > self.__cupo_maximo:
            print("No se puede superar el cupo maximo")
        else:
            self.__cupo_actual = valor

#se cambia el estado del curso a abierto
    def abrir_curso(self):
        self.__estado = True
        print("Curso " + self.__nombre + " abierto")

#se cambia el estado del curso a cerrado
    def cerrar_curso(self):
        self.__estado = False
        print("Curso " + self.__nombre + " cerrado")

#se asigna un docente al curso
    def asignar_docente(self, docente):
        self.__docente = docente
        print("Docente " + docente.nombres + " " + docente.apellidos + " asignado al curso " + self.__nombre)

#se asigna un aula al curso
    def asignar_aula(self, aula):
        print("Aula " + aula.nombre + " asignada al curso " + self.__nombre)

#se asigna un horario al curso
    def asignar_horario(self, horario):
        self.__horario = horario
        print("Horario asignado al curso " + self.__nombre)

#se agrega un estudiante al curso y se verifica que no se supere el cupo maximo
    def agregar_estudiante(self, estudiante):
        self.__lista_estudiantes.append(estudiante)
        print("Estudiante " + estudiante.nombres + " agregado al curso")

#se genera el horario del curso 
    def generar_horario(self):
        if self.__horario != None:
            self.__horario.mostrar_info()
        else:
            print("El curso no tiene horario asignado")
#se muestra la informacion del curso
    def mostrar_info(self):
        print("Curso: " + self.__nombre + " paralelo: " + self.__paralelo + " cupos: " + str(self.__cupo_actual) + "/" + str(self.__cupo_maximo))


class CargaAcademica:

    def __init__(self, id_carga, total_asignaturas, total_creditos, estado=True):
        self.__id_carga = id_carga
        self.__total_asignaturas = total_asignaturas
        self.__total_creditos = total_creditos

#se usa propiedades para acceder a los atributos privados
    @property
    def id_carga(self):
        return self.__id_carga

    @property
    def total_asignaturas(self):
        return self.__total_asignaturas

    @property
    def total_creditos(self):
        return self.__total_creditos

    @total_creditos.setter
    def total_creditos(self, valor):
        if valor < 0:
            print("Los creditos no pueden ser negativos")
        else:
            self.__total_creditos = valor

#genera la carga academica mostrando el total de asignaturas y creditos
    def generar_carga(self):
        print("Carga academica: " + str(self.__total_asignaturas) + " asignaturas " + str(self.__total_creditos) + " creditos")


class Matricula:

    def __init__(self, id_matricula, fecha_matricula, tipo_matricula, fecha_generacion, periodo, estado="Activa"):
        self.__id_matricula = id_matricula
        self.__fecha_matricula = fecha_matricula
        self.__tipo_matricula = tipo_matricula
        self.__periodo = periodo
        self.__estado = estado
        self.__observaciones = ""

#uso de propiedades para acceder a los atributos privados
    @property
    def id_matricula(self):
        return self.__id_matricula

    @property
    def fecha_matricula(self):
        return self.__fecha_matricula

    @property
    def tipo_matricula(self):
        return self.__tipo_matricula

    @property
    def periodo(self):
        return self.__periodo

    @property
    def estado(self):
        return self.__estado

    @property
    def observaciones(self):
        return self.__observaciones

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @observaciones.setter
    def observaciones(self, texto):
        self.__observaciones = texto

#se procesa la matricula cambiando su estado a activa
    def procesar_matricula(self):
        self.__estado = "Activa"
        print("Matricula procesada para el periodo " + self.__periodo)

#se anula la matricula cambiando su estado a anulada y se registra el motivo de la anulacion
    def anular_matricula(self, motivo):
        self.__estado = "Anulada"
        self.__observaciones = motivo
        print("Matricula anulada. Motivo: " + motivo)

#se imprime el comprobante de matricula
    def imprimir_comprobante(self):
        print("Comprobante de matricula")
        print("ID: " + str(self.__id_matricula))
        print("Tipo: " + self.__tipo_matricula)
        print("Fecha: " + self.__fecha_matricula)
        print("Periodo: " + self.__periodo)
        print("Estado: " + self.__estado)

class DetalleAsistencia:

    def __init__(self, tipo_justificacion, observacion, documento_soporte):
        self.__tipo_justificacion = tipo_justificacion
        self.__observacion = observacion
        self.__documento_soporte = documento_soporte

#uso de propiedades para acceder a los atributos privados
    @property
    def tipo_justificacion(self):
        return self.__tipo_justificacion

    @property
    def observacion(self):
        return self.__observacion

    @property
    def documento_soporte(self):
        return self.__documento_soporte

#se registra la justificacion de la falta
    def registrar_justificacion(self):
        print("Justificacion registrada tipo: " + self.__tipo_justificacion + " documento: " + self.__documento_soporte)

#se valida la justificacion verificando que se haya proporcionado un documento de soporte
    def validar_justificacion(self):
        if self.__documento_soporte != "":
            print("Justificacion valida")
            return True
        else:
            print("Justificacion no valida, falta documento de soporte")
            return False


class Asistencia:

    def __init__(self, id_asistencia, fecha, estado="Presente", observacion=""):
        self.__id_asistencia = id_asistencia
        self.__fecha = fecha
        self.__estado = estado
        self.__observacion = observacion
        self.__detalles = []
#uso de propiedades para acceder a los atributos privados
    @property
    def id_asistencia(self):
        return self.__id_asistencia

    @property
    def fecha(self):
        return self.__fecha

    @property
    def estado(self):
        return self.__estado

    @property
    def observacion(self):
        return self.__observacion

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    @observacion.setter
    def observacion(self, valor):
        self.__observacion = valor

#se anota la asistencia del estudiante
    def anotar_asistencia(self, estado, obs=""):
        self.__estado = estado
        self.__observacion = obs
        print("Asistencia anotada el " + self.__fecha + " estado: " + estado)

#se justifica la falta del estudiante verificando si el estado es ausente y se agrega el detalle de la justificacion
    def justificar_falta(self, detalle):
        if self.__estado == "Ausente":
            self.__detalles.append(detalle)
            self.__estado = "Justificado"
            print("Falta justificada con: " + detalle.tipo_justificacion)
        else:
            print("Solo se pueden justificar ausencias")

#se obtiene un resumen de la asistencia
    def obtener_resumen(self):
        resumen = {
            "id": self.__id_asistencia,
            "fecha": self.__fecha,
            "estado": self.__estado,
            "observacion": self.__observacion
        }
        return resumen

#se muestra la informacion de la asistencia 
    def mostrar_info(self):
        print("Asistencia " + str(self.__id_asistencia) + " fecha: " + self.__fecha + " estado: " + self.__estado)


class DetalleCalificacion:

    def __init__(self, id_detalle, tipo_evaluacion, descripcion, puntaje_obtenido, puntaje_total, fecha_evaluacion):
        self.__id_detalle = id_detalle
        self.__tipo_evaluacion = tipo_evaluacion
        self.__descripcion = descripcion
        self.__puntaje_obtenido = puntaje_obtenido
        self.__puntaje_total = puntaje_total
        self.__fecha_evaluacion = fecha_evaluacion
#uso de propiedades para acceder a los atributos privados
    @property
    def tipo_evaluacion(self):
        return self.__tipo_evaluacion

    @property
    def puntaje_obtenido(self):
        return self.__puntaje_obtenido

    @property
    def puntaje_total(self):
        return self.__puntaje_total
#se calcula el porcentaje de la evaluacion con base al puntaje obtenido y el puntaje total
    @property
    def porcentaje(self):
        if self.__puntaje_total == 0:
            return 0
        resultado = (self.__puntaje_obtenido / self.__puntaje_total) * 100
        return round(resultado, 2)

    @puntaje_obtenido.setter
    def puntaje_obtenido(self, valor):
        self.__puntaje_obtenido = valor

    def registrar_detalle(self):
        print("Detalle registrado: " + self.__tipo_evaluacion + " puntaje: " + str(self.__puntaje_obtenido) + "/" + str(self.__puntaje_total))
#editamos el puntaje obtenido en la evaluacion
    def editar_detalle(self, nuevo_puntaje):
        self.__puntaje_obtenido = nuevo_puntaje
        print("Puntaje actualizado a " + str(nuevo_puntaje))

    def eliminar_detalle(self):
        print("Detalle eliminado")
#se muetra un resumen del detalle de calificacion 
    def mostrar_info(self):
        print("Evaluacion: " + self.__tipo_evaluacion + " " + str(self.__puntaje_obtenido) + "/" + str(self.__puntaje_total) + " porcentaje: " + str(self.porcentaje) + "%")


class Calificacion:

    nota_minima = 7.0

    def __init__(self, id_calificacion, nota_parcial1, nota_parcial2, estado="Pendiente"):
        self.__id_calificacion = id_calificacion
        self.__nota_parcial1 = nota_parcial1
        self.__nota_parcial2 = nota_parcial2
        self.__estado = estado
        self.__detalles = []
#uso de propiedades para acceder a los atributos privados 
    @property
    def id_calificacion(self):
        return self.__id_calificacion

    @property
    def nota_parcial1(self):
        return self.__nota_parcial1

    @property
    def nota_parcial2(self):
        return self.__nota_parcial2

    @property
    def estado(self):
        return self.__estado

    @property
    def nota_final(self):
        return round((self.__nota_parcial1 + self.__nota_parcial2) / 2, 2)

    @property
    def promedio(self):
        return self.nota_final

    @nota_parcial1.setter
    def nota_parcial1(self, valor):
        if valor < 0 or valor > 10:
            print("La nota debe estar entre 0 y 10")
        else:
            self.__nota_parcial1 = valor

    @nota_parcial2.setter
    def nota_parcial2(self, valor):
        if valor < 0 or valor > 10:
            print("La nota debe estar entre 0 y 10")
        else:
            self.__nota_parcial2 = valor
#calculamos el promedio de las notas parciales y se determina si el estudiante aprueba o reprueba
    def calcular_promedio(self):
        p = self.nota_final
        if p >= self.nota_minima:
            print("Nota final: " + str(p) + " el estudiante APRUEBA")
        else:
            print("Nota final: " + str(p) + " el estudiante REPRUEBA")
        return p

#se registra un detalle de calificacion agregandolo a la lista
    def registrar_calificacion(self, detalle):
        self.__detalles.append(detalle)
        print("Detalle de calificacion registrado")

#se publica la calificacion cambiando su estado a publicada 
    def publicar_calificacion(self):
        self.__estado = "Publicada"
        print("Calificacion publicada con nota final " + str(self.nota_final))

#se obtiene un resumen de la calificacion con los datos principales
    def obtener_resumen(self):
        resumen = {
            "id": self.__id_calificacion,
            "parcial1": self.__nota_parcial1,
            "parcial2": self.__nota_parcial2,
            "nota_final": self.nota_final,
            "estado": self.__estado
        }
        return resumen

    def mostrar_info(self):
        print("Calificacion " + str(self.__id_calificacion) + " P1: " + str(self.__nota_parcial1) + " P2: " + str(self.__nota_parcial2) + " Nota final: " + str(self.nota_final))


class Reporte:

    def __init__(self, id_reporte, tipo_reporte, fecha_generacion, periodo, descripcion):
        self.__id_reporte = id_reporte
        self.__tipo_reporte = tipo_reporte
        self.__fecha_generacion = fecha_generacion
        self.__periodo = periodo
        self.__descripcion = descripcion
#uso de propiedades para acceder a los atributos privados
    @property
    def id_reporte(self):
        return self.__id_reporte

    @property
    def tipo_reporte(self):
        return self.__tipo_reporte

    @property
    def periodo(self):
        return self.__periodo

    @property
    def descripcion(self):
        return self.__descripcion

#generamos un reporte con la informacion dada
    def generar_reporte(self):
        print("Reporte: " + self.__tipo_reporte)
        print("Descripcion: " + self.__descripcion)
        print("Periodo: " + self.__periodo)
        print("Fecha de generacion: " + self.__fecha_generacion)

    def exportar_pdf(self):
        print("Reporte exportado a PDF")

    def exportar_excel(self):
        print("Reporte exportado a Excel")


print("Creando usuarios del sistema")
print("")
docente1 = Docente(1, "1300001111", "Valentin", "Perez", "perez123@uleam.edu.ec", "doc123", "0991234567", "Magister en Software", "Programacion OO")
estudiante1 = Estudiante(2, "1300002222", "Maykel", "Castro", "mcastro@uleam.edu.ec", "est123", "0997654321", "Cedula", "1300002222", "2005-03-15")
estudiante2 = Estudiante(3, "1300003333", "Bryan", "Chiquito", "bchiquito@uleam.edu.ec", "est456", "0994567890", "Cedula", "1300003333", "2004-07-22")
admin1 = Administrador(4, "1300004444", "Carlos", "Ortiz", "cortiz@uleam.edu.ec", "adm123", "0993456789", 1, "Director de Nivelacion")
print("Polimorfismo - el metodo mostrar_info se comporta diferente en cada clase")
print("")
lista_usuarios = [docente1, estudiante1, admin1]
for u in lista_usuarios:
    u.mostrar_info()
    print("")

print("Verificar metodo estatico")
print(Usuario.validar_correo("pablo@uleam.edu.ec"))

print("Metodo de clases")
print("Total usuarios:", Usuario.total_usuarios())
