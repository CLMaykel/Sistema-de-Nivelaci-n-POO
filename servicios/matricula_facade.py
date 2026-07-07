# matricula_facade.py
from modelos.matricula import Matricula


class MatriculaFacade:
    
    def __init__(self, periodo, curso, estudiante):
        self.__periodo = periodo
        self.__curso = curso
        self.__estudiante = estudiante

    def matricular(self, id_matricula, fecha, tipo):
        if self.__periodo.estado == "Cerrado":
            print("No se puede matricular, el periodo está cerrado")
            return False
        self.__curso.agregar_estudiante(self.__estudiante)
        
        matricula = Matricula(id_matricula, fecha, tipo, self.__periodo.nombre)
        matricula.procesar_matricula()
        self.__estudiante.matricula = matricula
        
        print("Matricula completada para " + self.__estudiante.nombres)
        return True
