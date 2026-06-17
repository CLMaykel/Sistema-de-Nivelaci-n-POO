#importamos las clases de los diferentes tipos de usuarios
from docente import Docente
from estudiante import Estudiante
from admin import Administrador

#hacemos uso del patrón Factory Method para crear una fábrica de usuarios
class FabricaUsuario:
    
    #método crear_usuario que recibe el tipo de usuario y los argumentos necesarios para crear una instancia del mismo 
    def crear_usuario(self, tipo_usuario, *args, **kwargs):
        if tipo_usuario == "Estudiante":
            return Estudiante(*args, **kwargs)
        elif tipo_usuario == "Docente":
            return Docente(*args, **kwargs)
        elif tipo_usuario == "Administrador" or tipo_usuario == "Admin":
            return Administrador(*args, **kwargs)
        else:
            #si el tipo de usuario ingresado no conduerda con ninguno de los casos anteriores, se lanza una excepción 
            raise ValueError(f"Tipo de usuario no válido: {tipo_usuario}")
