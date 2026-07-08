from modelos.detalle_calificacion import DetalleCalificacion
class Calificacion:

    nota_minima = 7.0 # Nota mínima requerida para aprobar la asignatura.

    def __init__(self, id_calificacion, nota_parcial1, nota_parcial2, estado="Pendiente"):
        self.__id_calificacion = id_calificacion
        self.__nota_parcial1 = nota_parcial1
        self.__nota_parcial2 = nota_parcial2
        self.__estado = estado
        self.__detalles = []
#uso de propiedades para acceder a los atributos privados 
    # Métodos Getter (lectura)
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
        
# Métodos Setter (modificación)
    @nota_parcial1.setter
    def nota_parcial1(self, valor):
        if valor < 0 or valor > 10:
            print("La nota debe estar entre 0 y 10")
        else:
            self.__nota_parcial1 = valor

    @nota_parcial2.setter
    def nota_parcial2(self, valor):      #Permite modificar la nota del primer parcial.
        if valor < 0 or valor > 10:
            print("La nota debe estar entre 0 y 10") #Valida que la nota esté entre 0 y 10.
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
        return resumen    # Retorna un diccionario con la información principal de la calificación.

    def mostrar_info(self):   # Muestra un resumen de la calificación incluyendo las notas parciales y la nota final.
        print("Calificacion " + str(self.__id_calificacion) + " P1: " + str(self.__nota_parcial1) + " P2: " + str(self.__nota_parcial2) + " Nota final: " + str(self.nota_final))
