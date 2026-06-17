from modelos.usuario import Usuario


class Administrador(Usuario):

    def __init__(self, id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono, id_administrador, cargo):
        super().__init__(id_usuario, cedula, nombres, apellidos, correo, contraseña, telefono)
        self.__id_administrador = id_administrador
        self.__cargo = cargo

    @property
    def id_administrador(self):
        return self.__id_administrador

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, valor):
        self.__cargo = valor

    def gestionar_usuario(self, accion, usuario, motivo=None, fecha=None):
        if usuario is None:
            raise ValueError("Debe proporcionar un usuario para gestionar")

        if accion not in ("activar", "desactivar"):
            raise ValueError(f"Acción no reconocida: {accion}")

        usuario.estado = accion == "activar"
        estado_texto = "activado" if usuario.estado else "desactivado"
        mensaje = f"Usuario {usuario.nombres} {usuario.apellidos} {estado_texto}"

        detalles = []
        if motivo:
            detalles.append(f"Motivo: {motivo}")
        if fecha:
            detalles.append(f"Fecha del cambio: {fecha}")

        if detalles:
            mensaje += ". " + ", ".join(detalles)

        print(mensaje)
        return mensaje

    def gestionar_procesos(self, proceso):
        mensaje = "Proceso ejecutado: " + proceso
        print(mensaje)
        return mensaje

    def gestionar_reportes(self):
        mensaje = "Reporte generado por: " + self.nombres + " " + self.apellidos + " cargo: " + self.__cargo
        print(mensaje)
        return mensaje

    def configurar_parametros(self, *args):
        lineas = []
        for item in args:
            clave = str(item[0])
            valor = str(item[1])
            lineas.append("Parametro configurado: " + clave + " = " + valor)
        mensaje = "\n".join(lineas) if lineas else "Sin parametros configurados"
        print(mensaje)
        return mensaje

    def gestionar_cursos(self, accion, curso):
        if curso is None:
            raise ValueError("Debe proporcionar un curso para gestionar")

        if accion == "abrir":
            curso.abrir_curso()
            mensaje = f"Administrador {self.nombres} {self.apellidos} abrió el curso {curso.nombre}"
        elif accion == "cerrar":
            curso.cerrar_curso()
            mensaje = f"Administrador {self.nombres} {self.apellidos} cerró el curso {curso.nombre}"
        else:
            raise ValueError(f"Acción no reconocida: {accion}")

        print(mensaje)
        return mensaje

    def iniciar_sesion(self, contraseña):
        if self.contraseña == contraseña and self.estado == True:
            mensaje = "Inicio de sesion como administrador correctamente para " + self.nombres + " " + self.apellidos
            print(mensaje)
            return True
        else:
            mensaje = "Contraseña incorrecta o usuario inactivo"
            print(mensaje)
            return False

    def mostrar_info(self):
        mensaje = (
            "Administrador: " + self.nombres + " " + self.apellidos + "\n"
            + "Cedula: " + self.cedula + "\n"
            + "Cargo: " + self.__cargo + "\n"
            + "Correo: " + self.correo
        )
        print(mensaje)
        return mensaje
