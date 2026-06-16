class Matricula:

    def __init__(self, id_matricula, fecha_matricula, tipo_matricula, periodo, estado="Activa"):
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