# Plan para la interfaz grafica

## Objetivo

Crear una demo funcional con interfaz grafica usando Programacion Orientada a Objetos. La interfaz debe permitir registrar usuarios, cursos, cargas academicas y reportes usando las clases del sistema.

## Estructura propuesta

- `modelos/`: clases principales del dominio, como `Usuario`, `Docente`, `Estudiante`, `CursoNivelacion`, `CargaAcademica` y `Reporte`.
- `servicios/`: logica que coordina objetos, como `FabricaUsuario`.
- `interfaz/`: ventanas, formularios y componentes visuales.
- `app/`: programas de demostracion y puntos de entrada.
- `docs/`: diagramas y documentacion.
- `legacy/`: versiones antiguas o monoliticas que sirven como referencia.

## Primera version de la demo

1. Ventana principal con secciones para usuarios, cursos, carga academica y reportes.
2. Formulario de usuarios conectado a `FabricaUsuario`.
3. Tabla o lista para mostrar usuarios registrados.
4. Formulario para crear cursos de nivelacion.
5. Accion para agregar estudiantes a un curso.
6. Formulario para generar carga academica.
7. Boton para generar reportes en consola o en una zona de texto.

## Clases que se deben aprovechar

- `FabricaUsuario`: crea estudiantes, docentes y administradores.
- `CursoNivelacion`: administra cupos y estudiantes inscritos.
- `CargaAcademica`: muestra asignaturas y creditos.
- `Reporte`: genera y exporta informacion usando `IExportable`.

## Siguiente paso tecnico

Crear una clase `SistemaNivelacion` en `servicios/` para guardar en memoria las listas de usuarios, cursos, cargas y reportes. La interfaz grafica debe hablar con esa clase y no crear objetos directamente.

