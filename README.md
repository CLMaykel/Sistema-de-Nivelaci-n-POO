# Sistema de Nivelación Académica — ULEAM

Aplicación web para la gestión integral de procesos de nivelación académica, desarrollada como proyecto de **Programación Orientada a Objetos (POO)** para la **Universidad Laica Eloy Alfaro de Manabí (ULEAM)**.

**Demo en línea:** [sistema-nivelacion-poo.streamlit.app](https://sistema-nivelacion-poo.streamlit.app)

---

## Descripción

El sistema centraliza la operación académica de nivelación: usuarios, aulas, horarios, cursos, matrículas, cargas académicas, calificaciones, asistencia, importación masiva de datos y generación de reportes exportables.

Está diseñado para tres perfiles de acceso — **Administrador**, **Docente** y **Estudiante** — con autenticación real y control de permisos por rol.

---

## Características principales

| Módulo | Descripción |
|--------|-------------|
| **Autenticación** | Login por cédula o correo `@uleam.edu.ec` y contraseña. El rol se asigna automáticamente según el tipo de usuario. |
| **Gestión académica** | Usuarios, aulas, horarios, cursos, inscripciones y cargas por periodo. |
| **Seguimiento** | Calificaciones (escala 0–10, aprobado ≥ 7.0) y control de asistencia. |
| **Reportes** | Exportación filtrable en **PDF** y **Excel** por rol (admin, docente, estudiante). |
| **Importación CSV** | Carga masiva unificada con columna `tipo_registro`. |
| **Persistencia SQL** | Microsoft SQL Server con fallback en memoria si la BD no está disponible. |
| **Idioma ES/EN** | Interfaz bilingüe en login, menú, sidebar y dashboards. |
| **Branding ULEAM** | Identidad institucional con logos oficiales y paleta rojo–blanco–verde. |

---

## Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3 |
| Paradigma | Programación Orientada a Objetos |
| Interfaz web | [Streamlit](https://streamlit.io/) |
| Base de datos | Microsoft SQL Server |
| Conectividad | `pyodbc` + ODBC Driver 17 |
| Reportes | `fpdf2` (PDF), `openpyxl` (Excel) |

---

## Arquitectura del proyecto

```
Sistema-de-Nivelacion-POO/
├── interfaz/                  # Capa de presentación (Streamlit)
│   ├── app.py                 # Punto de entrada de la aplicación
│   ├── auth.py                # Login y gestión de sesión
│   ├── state.py               # Estado global y carga de datos
│   ├── navigation.py          # Menú por rol
│   ├── idioma.py              # Internacionalización ES/EN
│   ├── branding.py            # Identidad visual ULEAM
│   ├── styles.py              # Estilos CSS personalizados
│   ├── components/            # Componentes reutilizables
│   ├── vistas/                # Pantallas por módulo
│   └── assets/                # Logos institucionales
├── modelos/                   # Entidades del dominio (POO)
├── servicios/                 # Lógica de negocio y orquestación
│   ├── sistema_nivelacion.py  # Orquestador principal
│   ├── importador_csv.py      # Importación masiva CSV
│   ├── exportador_reportes.py # Generación PDF/Excel
│   └── repositorios/          # Capa de persistencia SQL
├── app/                       # Programa de consola (demos POO)
├── POOPROYECTO.sql            # Script de creación de BD
├── requirements.txt           # Dependencias Python
└── .streamlit/                # Configuración Streamlit
```

### Flujo de datos

1. `get_sistema()` crea una instancia de `SistemaNivelacion` por sesión.
2. `inicializar_datos()` intenta conectar a SQL Server; si falla, carga datos de demostración en memoria.
3. Las operaciones de escritura persisten en SQL cuando la base de datos está activa.

### Patrones de diseño aplicados

- **Herencia y polimorfismo** — Jerarquía de usuarios (`Administrador`, `Docente`, `Estudiante`).
- **Factory Method** — Creación tipada de entidades del dominio.
- **Facade** — Proceso de matrícula simplificado (`MatriculaFacade`).
- **Strategy** — Exportación de reportes en distintos formatos (`IExportable`).
- **Singleton** — Gestor de idioma y configuración de sesión.
- **Repository** — Capa de persistencia SQL con fallback en memoria.

---

## Requisitos previos

- **Python 3.10+**
- **pip** (gestor de paquetes Python)
- **SQL Server** (local o remoto) — opcional; sin BD funciona en modo demo
- **ODBC Driver 17 for SQL Server** — [Descarga Microsoft](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/CLOG-U/Sistema-de-Nivelaci-n-POO.git
cd Sistema-de-Nivelacion-POO
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos (opcional)

1. Ejecutar el script `POOPROYECTO.sql` en SQL Server Management Studio o `sqlcmd`.
2. Copiar la plantilla de secrets:

```bash
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

3. Editar `.streamlit/secrets.toml` con sus credenciales:

```toml
[database]
server = "localhost"
database = "PROYECTOPOO"
driver = "ODBC Driver 17 for SQL Server"
username = "sa"
password = "su_contrasena"
```

> Si no configura SQL Server, la aplicación iniciará en **modo demostración en memoria**. Los datos no se guardarán entre sesiones.

### 5. Ejecutar la aplicación

```bash
streamlit run interfaz/app.py
```

Abra el navegador en `http://localhost:8501`.

---

## Credenciales de demostración

| Rol | Cédula | Correo | Contraseña |
|-----|--------|--------|------------|
| Administrador | 1300004444 | cortiz@uleam.edu.ec | adm123 |
| Docente | 1300001111 | perez123@uleam.edu.ec | doc123 |
| Estudiante | 1300002222 | mcastro@uleam.edu.ec | est123 |
| Estudiante | 1300003333 | bchiquito@uleam.edu.ec | est456 |

---

## Roles y permisos

### Administrador
Dashboard, usuarios, aulas, horarios, cursos, inscripciones, cargas académicas, reportes institucionales, importación de datos y configuración del sistema.

### Docente
Cursos asignados, horarios, listado de estudiantes, registro de notas y asistencia, reportes de sus cursos.

### Estudiante
Cursos inscritos, horario personal, carga académica, perfil con calificaciones y asistencia, reportes personales.

---

## Importación de datos CSV

El sistema admite la carga masiva de un **único archivo CSV** con la columna obligatoria `tipo_registro`.

**Plantilla de referencia:** `servicios/plantilla_dataset_nivelacion.csv`

**Orden de procesamiento:**

```
periodo → docente → estudiante → administrador → aula → horario → curso
→ matricula → carga_academica → calificacion → asistencia
```

**Uso:** Inicie sesión como Administrador → **Importar Datos** → subir CSV → **Importar dataset completo**.

---

## Reportes exportables

Cada rol puede generar documentos **PDF** o **Excel** filtrando por periodo y tipo de contenido:

| Rol | Tipos de reporte |
|-----|------------------|
| Administrador | Asistencia, calificaciones, inscripciones, carga académica, general |
| Docente | Mis cursos, calificaciones, asistencia, estudiantes inscritos |
| Estudiante | Mis cursos, mi carga, mis calificaciones, mi asistencia, resumen académico |

---

## Despliegue en Streamlit Cloud

1. Conectar el repositorio en [share.streamlit.io](https://share.streamlit.io).
2. **Main file path:** `interfaz/app.py`
3. Configurar **Secrets** con la sección `[database]` (requiere SQL Server accesible en la nube).
4. El archivo `packages.txt` instala `unixODBC` en el entorno Linux de Streamlit Cloud.

Sin SQL en la nube, la app funciona en modo demo en memoria.

---

## Escala académica

- Calificaciones en escala **0 a 10**.
- Aprobación con promedio final **≥ 7.0**.

---

## Institución

**Universidad Laica Eloy Alfaro de Manabí (ULEAM)**  
Facultad de Ingeniería Informática y Ciencias Computacionales  
Asignatura: Programación Orientada a Objetos

---

## Licencia

Proyecto académico desarrollado con fines educativos en el marco del curso de POO en ULEAM.
