import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from modelos.admin import Administrador
from modelos.aula import Aula
from modelos.curso_nivelacion import CursoNivelacion
from modelos.docente import Docente
from modelos.estudiante import Estudiante
from servicios.sistema_nivelacion import SistemaNivelacion


class VentanaLogin(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Login - Sistema de Nivelacion")
        self.geometry("400x300")
        self.minsize(400, 300)
        self.resizable(False, False)
        self.admin_autenticado = None
        self.sistema = SistemaNivelacion()
        self.sistema.cargar_datos_demo()
        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        self.configure(bg="#f4f6f8")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f8")
        self.style.configure("Form.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        self.style.configure("TLabel", background="#f4f6f8", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 18, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=40, style="Form.TFrame")
        contenedor.pack(fill="both", expand=True)

        titulo = ttk.Label(contenedor, text="Iniciar Sesión", style="Title.TLabel")
        titulo.pack(pady=(0, 30))

        ttk.Label(contenedor, text="Cédula", style="TLabel").pack(anchor="w", pady=(0, 5))
        self.entrada_cedula = ttk.Entry(contenedor, width=30)
        self.entrada_cedula.pack(fill="x", pady=(0, 20))

        ttk.Label(contenedor, text="Contraseña", style="TLabel").pack(anchor="w", pady=(0, 5))
        self.entrada_contraseña = ttk.Entry(contenedor, width=30, show="*")
        self.entrada_contraseña.pack(fill="x", pady=(0, 30))

        ttk.Button(contenedor, text="Ingresar", command=self._autenticar).pack(fill="x", pady=5)
        
        self.entrada_cedula.bind("<Return>", lambda _: self._autenticar())
        self.entrada_contraseña.bind("<Return>", lambda _: self._autenticar())

    def _autenticar(self):
        cedula = self.entrada_cedula.get().strip()
        contraseña = self.entrada_contraseña.get().strip()

        if not cedula or not contraseña:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        admin_encontrado = None
        for usuario in self.sistema.usuarios:
            if isinstance(usuario, Administrador) and usuario.cedula == cedula:
                admin_encontrado = usuario
                break

        if admin_encontrado is None:
            messagebox.showerror("Error", "Administrador no encontrado")
            return

        if admin_encontrado.iniciar_sesion(contraseña):
            self.admin_autenticado = admin_encontrado
            self.destroy()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta o usuario inactivo")


class VentanaPrincipal(tk.Tk):

    def __init__(self, admin):
        super().__init__()
        self.admin = admin
        self.title(f"Bienvenido admin: {admin.nombres} {admin.apellidos}")
        self.geometry("1080x680")
        self.minsize(960, 620)
        self.sistema = SistemaNivelacion()
        self.sistema.usuarios = [admin]
        self.reporte_activo_id = None
        self._configurar_estilos()
        self._crear_interfaz()
        self._actualizar_todo()

    def _configurar_estilos(self):
        self.configure(bg="#f4f6f8")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f4f6f8")
        self.style.configure("Panel.TFrame", background="#ffffff", relief="solid", borderwidth=1)
        self.style.configure("Form.TFrame", background="#ffffff", relief="flat", borderwidth=0)
        self.style.configure("TLabel", background="#f4f6f8", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 18, "bold"))
        self.style.configure("Panel.TLabel", background="#ffffff", foreground="#1f2937", font=("Segoe UI", 10))
        self.style.configure("Metric.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 22, "bold"))
        self.style.configure("TButton", font=("Segoe UI", 10), padding=8)
        self.style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _crear_interfaz(self):
        contenedor = ttk.Frame(self, padding=18)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 14))
        ttk.Label(encabezado, text=f"Bienvenido admin: {self.admin.nombres} {self.admin.apellidos}", style="Title.TLabel").pack(side="left")
        ttk.Button(encabezado, text="Cargar datos demo", command=self._cargar_demo).pack(side="right")

        self.tabs = ttk.Notebook(contenedor)
        self.tabs.pack(fill="both", expand=True)

        self.tab_inicio = ttk.Frame(self.tabs, padding=14)
        self.tab_cursos = ttk.Frame(self.tabs, padding=14)
        self.tab_carga = ttk.Frame(self.tabs, padding=14)
        self.tab_reportes = ttk.Frame(self.tabs, padding=14)

        self.tabs.add(self.tab_inicio, text="Inicio")
        self.tabs.add(self.tab_cursos, text="Cursos")
        self.tabs.add(self.tab_carga, text="Carga academica")
        self.tabs.add(self.tab_reportes, text="Reportes")

        self._crear_tab_inicio()
        self._crear_tab_cursos()
        self._crear_tab_carga()
        self._crear_tab_reportes()

    def _crear_tab_inicio(self):
        self.metricas = {}
        grilla = ttk.Frame(self.tab_inicio)
        grilla.pack(fill="x")

        for indice, clave in enumerate(["usuarios", "docentes", "estudiantes", "cursos", "aulas", "cargas", "reportes"]):
            panel = ttk.Frame(grilla, style="Panel.TFrame", padding=14)
            panel.grid(row=indice // 4, column=indice % 4, sticky="nsew", padx=6, pady=6)
            ttk.Label(panel, text=clave.capitalize(), style="Panel.TLabel").pack(anchor="w")
            valor = ttk.Label(panel, text="0", style="Metric.TLabel")
            valor.pack(anchor="w", pady=(8, 0))
            self.metricas[clave] = valor

        for columna in range(4):
            grilla.columnconfigure(columna, weight=1)

        acciones = ttk.Frame(self.tab_inicio)
        acciones.pack(fill="x", pady=18)
        ttk.Button(acciones, text="Crear curso", command=lambda: self.tabs.select(self.tab_cursos)).pack(side="left", padx=(0, 8))
        ttk.Button(acciones, text="Generar reporte", command=lambda: self.tabs.select(self.tab_reportes)).pack(side="left")

    def _crear_tab_cursos(self):
        contenido = ttk.Frame(self.tab_cursos)
        contenido.pack(fill="both", expand=True)
        formularios = ttk.Frame(contenido, width=280)
        formularios.pack(side="left", fill="y", padx=(0, 12))
        formularios.pack_propagate(False)
        registros = ttk.LabelFrame(contenido, text="Registros", padding=10)
        registros.pack(side="left", fill="both", expand=True)

        gestor_formularios = ttk.Notebook(formularios)
        gestor_formularios.pack(fill="both", expand=True)

        aula_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        curso_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        horario_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")
        inscripcion_panel = ttk.Frame(gestor_formularios, padding=12, style="Form.TFrame")

        gestor_formularios.add(aula_panel, text="Aula")
        gestor_formularios.add(curso_panel, text="Curso")
        gestor_formularios.add(horario_panel, text="Horario")
        gestor_formularios.add(inscripcion_panel, text="Inscripcion")

        self.campos_aula = self._crear_campos(aula_panel, ["Codigo", "Nombre", "Capacidad", "Piso", "Edificio"])
        ttk.Button(aula_panel, text="Guardar aula", command=self._registrar_aula).pack(fill="x", pady=(8, 0))

        self.campos_curso = self._crear_campos(curso_panel, ["Codigo", "Nombre", "Nivel", "Paralelo", "Cupo maximo"])
        self.combo_docente = self._crear_combo(curso_panel, "Docente")
        self.combo_aula = self._crear_combo(curso_panel, "Aula")

        self.campos_horario = self._crear_campos(horario_panel, ["Dia", "Hora inicio", "Hora fin", "Modalidad", "Grupo"])
        ttk.Button(horario_panel, text="Guardar curso", command=self._registrar_curso).pack(fill="x", pady=(8, 0))

        self.combo_curso = self._crear_combo(inscripcion_panel, "Curso")
        self.combo_estudiante = self._crear_combo(inscripcion_panel, "Estudiante")
        ttk.Button(inscripcion_panel, text="Inscribir estudiante", command=self._inscribir_estudiante).pack(fill="x", pady=(8, 0))

        registros_tabs = ttk.Notebook(registros)
        registros_tabs.pack(fill="both", expand=True)
        panel_aulas = ttk.Frame(registros_tabs, padding=8)
        panel_cursos = ttk.Frame(registros_tabs, padding=8)
        registros_tabs.add(panel_aulas, text="Aulas")
        registros_tabs.add(panel_cursos, text="Cursos")

        self.tabla_aulas = self._crear_tabla(
            panel_aulas,
            ("codigo", "nombre", "capacidad", "edificio"),
            ("Codigo", "Nombre", "Capacidad", "Edificio"),
        )
        self.tabla_aulas.bind("<Double-1>", self._mostrar_detalle_aula_seleccionada)
        ttk.Button(panel_aulas, text="Ver detalle", command=self._mostrar_detalle_aula_seleccionada).pack(anchor="e")

        self.tabla_cursos = self._crear_tabla(
            panel_cursos,
            ("codigo", "nombre", "docente", "cupo"),
            ("Codigo", "Nombre", "Docente", "Cupo"),
        )
        self.tabla_cursos.bind("<Double-1>", self._mostrar_detalle_curso_seleccionado)
        ttk.Button(panel_cursos, text="Ver detalle", command=self._mostrar_detalle_curso_seleccionado).pack(anchor="e")

    def _crear_tab_carga(self):
        contenido = ttk.Frame(self.tab_carga)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        self.combo_estudiante_carga = self._crear_combo(formulario, "Estudiante")
        ttk.Label(formulario, text="Periodo actual", style="Panel.TLabel").pack(anchor="w")
        ttk.Label(formulario, text=self.sistema.periodo_actual, style="Panel.TLabel").pack(anchor="w", pady=(2, 12))
        ttk.Button(formulario, text="Generar carga", command=self._registrar_carga).pack(fill="x", pady=(8, 0))

        panel_cargas = ttk.Frame(contenido)
        panel_cargas.pack(side="left", fill="both", expand=True)
        self.tabla_cargas = self._crear_tabla(
            panel_cargas,
            ("id", "estudiante", "periodo", "asignaturas", "creditos", "estado"),
            ("ID", "Estudiante", "Periodo", "Asignaturas", "Creditos", "Estado"),
        )
        self.tabla_cargas.bind("<Double-1>", self._mostrar_detalle_carga_seleccionada)
        ttk.Button(panel_cargas, text="Ver detalle", command=self._mostrar_detalle_carga_seleccionada).pack(anchor="e")

    def _crear_tab_reportes(self):
        contenido = ttk.Frame(self.tab_reportes)
        contenido.pack(fill="both", expand=True)
        formulario = ttk.Frame(contenido, style="Panel.TFrame", padding=14)
        formulario.pack(side="left", fill="y", padx=(0, 12))
        ttk.Label(formulario, text="Fecha generacion", style="Panel.TLabel").pack(anchor="w")
        ttk.Label(formulario, text=date.today().isoformat(), style="Panel.TLabel").pack(anchor="w", pady=(2, 12))
        self.campos_reporte = self._crear_campos(formulario, ["Tipo reporte", "Descripcion"])
        self.combo_periodo_reporte = self._crear_combo(formulario, "Periodo")
        self.formato_reporte = tk.StringVar(value="PDF")
        ttk.Label(formulario, text="Formato", style="Panel.TLabel").pack(anchor="w")
        ttk.Combobox(formulario, textvariable=self.formato_reporte, values=["PDF", "Excel"], state="readonly").pack(fill="x", pady=(2, 8))
        ttk.Button(formulario, text="Generar reporte", command=self._generar_reporte).pack(fill="x", pady=(8, 0))

        panel_salida = ttk.Frame(contenido)
        panel_salida.pack(side="left", fill="both", expand=True)
        self.tabla_reportes = self._crear_tabla(panel_salida, ("id", "tipo", "fecha", "periodo", "formato"), ("ID", "Tipo", "Fecha", "Periodo", "Formato"))
        self.tabla_reportes.bind("<<TreeviewSelect>>", self._mostrar_reporte_seleccionado)
        self.salida_reporte = tk.Text(panel_salida, height=8, wrap="word", font=("Segoe UI", 10))
        self.salida_reporte.pack(fill="x", pady=(10, 0))
        self._renderizar_reporte(None)

    # Método auxiliar que crea dinámicamente campos de entrada (Entry) con etiquetas en un formulario
    # Recorre cada etiqueta, crea una Label y su correspondiente Entry, almacenando referencias en un diccionario
    def _crear_campos(self, padre, etiquetas):
        campos = {}
        for etiqueta in etiquetas:
            ttk.Label(padre, text=etiqueta, style="Panel.TLabel").pack(anchor="w")
            entrada = ttk.Entry(padre, width=30)
            entrada.pack(fill="x", pady=(2, 8))
            campos[etiqueta] = entrada
        return campos

    def _crear_combo(self, padre, etiqueta):
        ttk.Label(padre, text=etiqueta, style="Panel.TLabel").pack(anchor="w")
        variable = tk.StringVar()
        combo = ttk.Combobox(padre, textvariable=variable, state="readonly", width=28)
        combo.pack(fill="x", pady=(2, 8))
        combo.variable = variable
        return combo

    def _crear_tabla(self, padre, columnas, encabezados):
        frame = ttk.Frame(padre)
        frame.pack(fill="both", expand=True, pady=(0, 8))
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")
        barra = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=barra.set)
        for columna, encabezado in zip(columnas, encabezados):
            tabla.heading(columna, text=encabezado)
            tabla.column(columna, width=130, anchor="w")
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        return tabla

    def _registrar_aula(self):
        try:
            self.sistema.registrar_aula(
                self._valor(self.campos_aula["Codigo"]),
                self._valor(self.campos_aula["Nombre"]),
                self._valor(self.campos_aula["Capacidad"]),
                self._valor(self.campos_aula["Piso"]),
                self._valor(self.campos_aula["Edificio"]),
            )
            self._limpiar_campos(self.campos_aula)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Aula", str(error))

    def _registrar_curso(self):
        try:
            docente = self._objeto_seleccionado(self.combo_docente, self.sistema.listar_docentes())
            aula = self._objeto_seleccionado(self.combo_aula, self.sistema.aulas)
            horario = self.sistema.registrar_horario(
                self._valor(self.campos_horario["Dia"]),
                self._valor(self.campos_horario["Hora inicio"]),
                self._valor(self.campos_horario["Hora fin"]),
                self._valor(self.campos_horario["Modalidad"]),
                self._valor(self.campos_horario["Grupo"]),
                aula,
            )
            self.sistema.registrar_curso(
                self._valor(self.campos_curso["Codigo"]),
                self._valor(self.campos_curso["Nombre"]),
                self._valor(self.campos_curso["Nivel"]),
                self._valor(self.campos_curso["Paralelo"]),
                self._valor(self.campos_curso["Cupo maximo"]),
                docente,
                horario,
                aula,
            )
            self._limpiar_campos(self.campos_curso)
            self._limpiar_campos(self.campos_horario)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Curso", str(error))

    def _inscribir_estudiante(self):
        try:
            curso = self._objeto_seleccionado(self.combo_curso, self.sistema.cursos)
            estudiante = self._objeto_seleccionado(self.combo_estudiante, self.sistema.listar_estudiantes())
            self.sistema.inscribir_estudiante(curso, estudiante)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Inscripcion", str(error))

    def _registrar_carga(self):
        try:
            estudiante = self._objeto_seleccionado(self.combo_estudiante_carga, self.sistema.listar_estudiantes())
            self.sistema.registrar_carga_academica(estudiante)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Carga academica", str(error))

    def _generar_reporte(self):
        try:
            reporte = self.sistema.generar_reporte(
                self._valor(self.campos_reporte["Tipo reporte"]),
                self.combo_periodo_reporte.get(),
                self._valor(self.campos_reporte["Descripcion"]),
                self.formato_reporte.get(),
            )
            self.reporte_activo_id = reporte.id_reporte
            self._limpiar_campos(self.campos_reporte)
            self._actualizar_todo()
        except Exception as error:
            messagebox.showerror("Reporte", str(error))

    def _cargar_demo(self):
        self.sistema.cargar_datos_demo()
        self._actualizar_todo()

    def _actualizar_todo(self):
        self._actualizar_metricas()
        self._actualizar_registros_cursos()
        self._actualizar_cargas()
        self._actualizar_reportes()
        self._actualizar_combos()

    def _actualizar_metricas(self):
        for clave, valor in self.sistema.resumen().items():
            self.metricas[clave].configure(text=str(valor))

    def _actualizar_registros_cursos(self):
        self._vaciar_tabla(self.tabla_aulas)
        self._vaciar_tabla(self.tabla_cursos)
        self.objetos_aulas = {}
        self.objetos_cursos = {}

        for aula in self.sistema.aulas:
            item = self.tabla_aulas.insert("", "end", values=(aula.codigo, aula.nombre, aula.capacidad, aula.edificio))
            self.objetos_aulas[item] = aula

        for curso in self.sistema.cursos:
            docente = curso.docente.nombres + " " + curso.docente.apellidos
            cupo = str(curso.cupo_actual) + "/" + str(curso.cupo_maximo)
            item = self.tabla_cursos.insert("", "end", values=(curso.codigo, curso.nombre, docente, cupo))
            self.objetos_cursos[item] = curso

    def _mostrar_detalle_curso_seleccionado(self, _event=None):
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            return

        curso = self.objetos_cursos.get(seleccion[0])
        if curso is not None:
            self._mostrar_detalle_curso(curso)

    def _mostrar_detalle_aula_seleccionada(self, _event=None):
        seleccion = self.tabla_aulas.selection()
        if not seleccion:
            return

        aula = self.objetos_aulas.get(seleccion[0])
        if aula is not None:
            self._mostrar_detalle_aula(aula)

    def _mostrar_detalle_curso(self, curso):
        ventana = self._crear_ventana_detalle("Detalle del curso")
        horario = curso.horario
        aula = curso.aula
        docente = curso.docente.nombres + " " + curso.docente.apellidos
        estudiantes = ", ".join([est.nombres + " " + est.apellidos for est in curso.lista_estudiantes])
        if not estudiantes:
            estudiantes = "Sin estudiantes inscritos"

        datos = [
            ("Codigo", curso.codigo),
            ("Nombre", curso.nombre),
            ("Nivel", curso.nivel),
            ("Paralelo", curso.paralelo),
            ("Cupo", str(curso.cupo_actual) + "/" + str(curso.cupo_maximo)),
            ("Estado", "Abierto" if curso.estado else "Cerrado"),
            ("Docente", docente),
            ("Aula", aula.nombre + " - " + aula.edificio),
            ("Horario", horario.dia + " de " + horario.hora_inicio + " a " + horario.hora_fin),
            ("Modalidad", horario.modalidad),
            ("Grupo", horario.grupo),
            ("Estudiantes", estudiantes),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_aula(self, aula):
        ventana = self._crear_ventana_detalle("Detalle del aula")
        datos = [
            ("Codigo", aula.codigo),
            ("Nombre", aula.nombre),
            ("Capacidad", aula.capacidad),
            ("Piso", aula.piso),
            ("Edificio", aula.edificio),
            ("Estado", "Disponible" if aula.estado else "No disponible"),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_detalle_carga_seleccionada(self, _event=None):
        seleccion = self.tabla_cargas.selection()
        if not seleccion:
            return

        carga = self.objetos_cargas.get(seleccion[0])
        if carga is not None:
            self._mostrar_detalle_carga(carga)

    def _mostrar_detalle_carga(self, carga):
        ventana = self._crear_ventana_detalle("Detalle de carga academica")
        estudiante = carga.estudiante.nombres + " " + carga.estudiante.apellidos
        datos = [
            ("ID", carga.id_carga),
            ("Estudiante", estudiante),
            ("Cedula", carga.estudiante.cedula),
            ("Periodo", carga.periodo),
            ("Asignaturas", carga.total_asignaturas),
            ("Creditos", carga.total_creditos),
            ("Estado", "Activa" if carga.estado else "Inactiva"),
        ]
        self._llenar_detalle(ventana, datos)

    def _mostrar_reporte_seleccionado(self, _event=None):
        seleccion = self.tabla_reportes.selection()
        if not seleccion:
            return

        reporte = self.objetos_reportes.get(seleccion[0])
        if reporte is not None:
            self.reporte_activo_id = reporte.id_reporte
            self._renderizar_reporte(reporte)

    def _renderizar_reporte(self, reporte):
        self.salida_reporte.configure(state="normal")
        self.salida_reporte.delete("1.0", "end")

        if reporte is None:
            self.salida_reporte.insert("end", "Seleccione un reporte para ver su detalle.")
        else:
            self.salida_reporte.insert("end", "Reporte: " + reporte.tipo_reporte + "\n")
            self.salida_reporte.insert("end", "Fecha de generacion: " + reporte.fecha_generacion + "\n")
            self.salida_reporte.insert("end", "Periodo: " + reporte.periodo + "\n")
            self.salida_reporte.insert("end", "Descripcion: " + reporte.descripcion + "\n")
            self.salida_reporte.insert("end", "Formato: " + reporte.formato)

        self.salida_reporte.configure(state="disabled")

    def _crear_ventana_detalle(self, titulo):
        ventana = tk.Toplevel(self)
        ventana.title(titulo)
        ventana.geometry("460x360")
        ventana.minsize(420, 300)
        ventana.configure(bg="#f4f6f8")
        return ventana

    def _llenar_detalle(self, ventana, datos):
        contenedor = ttk.Frame(ventana, padding=16, style="Form.TFrame")
        contenedor.pack(fill="both", expand=True)

        for fila, (etiqueta, valor) in enumerate(datos):
            ttk.Label(contenedor, text=etiqueta + ":", style="Panel.TLabel").grid(row=fila, column=0, sticky="nw", padx=(0, 10), pady=4)
            ttk.Label(contenedor, text=str(valor), style="Panel.TLabel", wraplength=300).grid(row=fila, column=1, sticky="nw", pady=4)

        contenedor.columnconfigure(1, weight=1)

    def _actualizar_cargas(self):
        self._vaciar_tabla(self.tabla_cargas)
        self.objetos_cargas = {}
        for carga in self.sistema.cargas_academicas:
            estudiante = carga.estudiante.nombres + " " + carga.estudiante.apellidos
            item = self.tabla_cargas.insert(
                "",
                "end",
                values=(
                    carga.id_carga,
                    estudiante,
                    carga.periodo,
                    carga.total_asignaturas,
                    carga.total_creditos,
                    "Activa" if carga.estado else "Inactiva",
                ),
            )
            self.objetos_cargas[item] = carga

    def _actualizar_reportes(self):
        self._vaciar_tabla(self.tabla_reportes)
        self.objetos_reportes = {}
        item_activo = None

        for reporte in self.sistema.reportes:
            item = self.tabla_reportes.insert("", "end", values=(reporte.id_reporte, reporte.tipo_reporte, reporte.fecha_generacion, reporte.periodo, reporte.formato))
            self.objetos_reportes[item] = reporte
            if reporte.id_reporte == self.reporte_activo_id:
                item_activo = item

        if item_activo is not None:
            self.tabla_reportes.selection_set(item_activo)
            self.tabla_reportes.focus(item_activo)
            self.tabla_reportes.see(item_activo)
            self._renderizar_reporte(self.objetos_reportes[item_activo])
        elif self.reporte_activo_id is not None:
            self.reporte_activo_id = None
            self._renderizar_reporte(None)

    # Método que llena los ComboBox con objetos del sistema o valores de texto
    # Almacena los objetos en el combo para poder recuperarlos después al seleccionar una opción
    def _actualizar_combos(self):
        self._llenar_combo(self.combo_docente, self.sistema.listar_docentes())
        self._llenar_combo(self.combo_estudiante, self.sistema.listar_estudiantes())
        self._llenar_combo(self.combo_estudiante_carga, self.sistema.listar_estudiantes())
        self._llenar_combo(self.combo_aula, self.sistema.aulas)
        self._llenar_combo(self.combo_curso, self.sistema.cursos)
        self._llenar_combo_texto(self.combo_periodo_reporte, self.sistema.listar_periodos())

    def _llenar_combo(self, combo, objetos):
        combo.objetos = objetos
        combo["values"] = [self._texto_objeto(objeto) for objeto in objetos]
        if objetos and not combo.get():
            combo.current(0)
        if not objetos:
            combo.set("")

    def _llenar_combo_texto(self, combo, valores):
        combo["values"] = valores
        if valores and not combo.get():
            combo.current(0)
        if not valores:
            combo.set("")

    def _objeto_seleccionado(self, combo, objetos):
        indice = combo.current()
        if indice < 0 or indice >= len(objetos):
            raise ValueError("Seleccione una opcion valida")
        return objetos[indice]

    def _texto_objeto(self, objeto):
        if isinstance(objeto, (Docente, Estudiante, Administrador)):
            return str(objeto.id_usuario) + " - " + objeto.nombres + " " + objeto.apellidos
        if hasattr(objeto, "codigo") and hasattr(objeto, "nombre"):
            return objeto.codigo + " - " + objeto.nombre
        if hasattr(objeto, "nombre"):
            return objeto.nombre
        return str(objeto)

    def _valor(self, entrada):
        valor = entrada.get().strip()
        if not valor:
            raise ValueError("Complete todos los campos requeridos")
        return valor

    def _limpiar_campos(self, campos):
        for entrada in campos.values():
            entrada.delete(0, "end")

    def _vaciar_tabla(self, tabla):
        for item in tabla.get_children():
            tabla.delete(item)


def iniciar_interfaz():
    login = VentanaLogin()
    login.mainloop()
    
    if login.admin_autenticado:
        # Copiar los datos del sistema del login a la ventana principal
        app = VentanaPrincipal(login.admin_autenticado)
        # Copiar todos los datos cargados en el demo al nuevo sistema
        app.sistema.usuarios = login.sistema.usuarios
        app.sistema.aulas = login.sistema.aulas
        app.sistema.horarios = login.sistema.horarios
        app.sistema.cursos = login.sistema.cursos
        app.sistema.cargas_academicas = login.sistema.cargas_academicas
        app.sistema.reportes = login.sistema.reportes
        app._actualizar_todo()
        app.mainloop()
