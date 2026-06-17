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