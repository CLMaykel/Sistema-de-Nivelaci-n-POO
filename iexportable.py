from abc import ABC, abstractmethod

class IExportable(ABC):

    @abstractmethod
    def exportar(self, datos):
        pass


class ExportarExcel(IExportable):

    def exportar(self, datos):
        print("Exportando a Excel:", datos)


class ExportarPDF(IExportable):

    def exportar(self, datos):
        print("Exportando a PDF:", datos)

