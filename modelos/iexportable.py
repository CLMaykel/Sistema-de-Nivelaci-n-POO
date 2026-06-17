from abc import ABC, abstractmethod
#creamos la interfaz IExportable para exportar datos en diferentes formatos
class IExportable(ABC):
    #metodo con el que se exportaran los datos, cada clase que implemente esta interfaz debe definir este metodo
    @abstractmethod
    def exportar(self, datos):
        pass

#clase ExportarExcel que exporta datos a formato Excel
class ExportarExcel(IExportable):

    def exportar(self, datos):
        print("Exportando a Excel:", datos)

#clase ExportarPDF que exporta datos a formato PDF
class ExportarPDF(IExportable):
    
    def exportar(self, datos):
        print("Exportando a PDF:", datos)

