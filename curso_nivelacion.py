class CursoNivelacion:

    def __init__(self, id_curso, codigo, nombre, nivel, paralelo, cupo_maximo, docente, horario, aula, estado=True):
        self.__id_curso = id_curso
        self.__codigo = codigo
        self.__nombre = nombre
        self.__nivel = nivel
        self.__paralelo = paralelo
        self.__cupo_maximo = cupo_maximo
        self.__cupo_actual = 0
        self.__estado = estado
        self.__docente = docente
        self.__horario = horario
        self.__aula = aula
        self.__lista_estudiantes = []

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
        elif valor < 0:
            print("El cupo actual no puede ser negativo")
        else:
            self.__cupo_actual = valor

    def abrir_curso(self):
        self.__estado = True
        print("Curso " + self.__nombre + " abierto")

    def cerrar_curso(self):
        self.__estado = False
        print("Curso " + self.__nombre + " cerrado")

    def agregar_estudiante(self, estudiante):
        if self.__cupo_actual < self.__cupo_maximo:
            self.__lista_estudiantes.append(estudiante)
            self.__cupo_actual += 1
            print("Estudiante " + estudiante.nombres + " agregado al curso")
        else:
            print("No hay cupos disponibles en " + self.__nombre)

    def generar_horario(self):
        if self.__horario is not None:
            self.__horario.mostrar_info()
        else:
            print("El curso no tiene horario asignado")

    def mostrar_info(self):
        print("Curso: " + self.__nombre + " paralelo: " + self.__paralelo + " cupos: " + str(self.__cupo_actual) + "/" + str(self.__cupo_maximo))
        print("Docente: " + self.__docente.nombres + " " + self.__docente.apellidos)
        print("Aula: " + self.__aula.nombre)

