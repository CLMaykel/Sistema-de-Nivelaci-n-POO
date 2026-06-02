from usuario import Usuario
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
