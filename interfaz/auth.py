import base64

import streamlit as st

from interfaz.branding import RUTA_LOGO, RUTA_LOGO_VERTICAL, SIGLAS
from interfaz.idioma import obtener_gestor_idioma, selector_idioma, t
from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante


def inicializar_sesion():
    # Inicializa el estado de sesión con variables de autenticación y navegación
    obtener_gestor_idioma().obtener_idioma()
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if "rol_actual" not in st.session_state:
        st.session_state.rol_actual = None
    if "usuario_actual_id" not in st.session_state:
        st.session_state.usuario_actual_id = None
    if "usuario_actual" not in st.session_state:
        st.session_state.usuario_actual = None
    if "nav_seleccion" not in st.session_state:
        st.session_state.nav_seleccion = None


def cerrar_sesion():
    # Limpia el estado de sesión y cierra la sesión del usuario
    st.session_state.autenticado = False
    st.session_state.rol_actual = None
    st.session_state.usuario_actual_id = None
    st.session_state.usuario_actual = None
    st.session_state.nav_seleccion = None
    st.rerun()


def esta_autenticado():
    # Verifica si el usuario tiene una sesión autenticada con rol asignado
    return bool(st.session_state.get("autenticado") and st.session_state.get("rol_actual"))


def obtener_rol_actual():
    # Retorna el rol del usuario autenticado actual
    return st.session_state.get("rol_actual")


def obtener_usuario_actual(sistema):
    # Retorna el objeto de usuario desde el sistema si está autenticado
    if not esta_autenticado():
        return None

    usuario_id = st.session_state.get("usuario_actual_id")
    if usuario_id is None:
        return None

    return sistema.usuarios.get(usuario_id)


def _rol_desde_usuario(usuario):
    # Determina el rol del usuario según su tipo de clase
    if isinstance(usuario, Administrador):
        return "Administrador"
    if isinstance(usuario, Docente):
        return "Docente"
    if isinstance(usuario, Estudiante):
        return "Estudiante"
    return None


def _dashboard_por_rol(rol):
    # Retorna el dashboard inicial según el rol del usuario
    return {
        "Administrador": "Dashboard",
        "Docente": "Dashboard Docente",
        "Estudiante": "Dashboard Estudiante",
    }.get(rol)


def autenticar_usuario(sistema, identificador, contrasena):
    # Autentica un usuario verificando credenciales y asigna rol y datos de sesión
    usuario = sistema.buscar_usuario_por_identificador(identificador)
    if not usuario:
        return False, t("login.error_usuario")

    if not usuario.iniciar_sesion(contrasena):
        return False, t("login.error_contrasena")

    rol = _rol_desde_usuario(usuario)
    if not rol:
        return False, t("login.error_rol")

    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    st.session_state.autenticado = True
    st.session_state.rol_actual = rol
    st.session_state.usuario_actual_id = usuario.id_usuario
    st.session_state.usuario_actual = nombre_completo
    st.session_state.nav_seleccion = _dashboard_por_rol(rol)
    return True, t("login.bienvenida", nombre=nombre_completo)


def _logo_base64(ruta):
    # Convierte una imagen de logo a formato base64 para incrustar en HTML
    if not ruta.exists():
        return None
    mime = "image/png" if ruta.suffix.lower() == ".png" else "image/jpeg"
    contenido = base64.b64encode(ruta.read_bytes()).decode()
    return f"data:{mime};base64,{contenido}"


def _render_hero_login():
    logo_src = _logo_base64(RUTA_LOGO_VERTICAL) or _logo_base64(RUTA_LOGO)
    logo_html = ""
    if logo_src:
        logo_html = f'<img class="login-hero-logo" src="{logo_src}" alt="{SIGLAS}">'

    st.markdown(
        f"""
        <div class="login-hero">
            {logo_html}
            <p class="login-hero-siglas">{SIGLAS}</p>
            <p class="login-hero-title">{t("app.titulo_sistema")}</p>
            <p class="login-hero-subtitle">{t("app.universidad")}</p>
            <div class="login-hero-band">
                <span class="rojo"></span>
                <span class="blanco"></span>
                <span class="verde"></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pantalla_login(sistema):
    # Renderiza la pantalla de login con formulario de autenticación y credenciales demo
    from interfaz.styles import aplicar_estilos_login

    aplicar_estilos_login()

    col_espacio, col_lang = st.columns([5, 1])
    with col_lang:
        selector_idioma(ubicacion="main")

    if not st.session_state.get("db_cargada"):
        st.warning(st.session_state.get("db_mensaje", t("app.demo_sql")))

    _render_hero_login()

    with st.form("form_login_institucional", clear_on_submit=False):
        usuario = st.text_input(
            t("login.usuario"),
            placeholder=t("login.placeholder_usuario"),
        )
        contrasena = st.text_input(
            t("login.contrasena"),
            type="password",
            placeholder=t("login.placeholder_contrasena"),
        )
        enviar = st.form_submit_button(
            t("login.acceder"),
            use_container_width=True,
            type="primary",
        )

        if enviar:
            if not usuario.strip() or not contrasena:
                st.error(t("login.error_campos"))
            else:
                ok, mensaje = autenticar_usuario(sistema, usuario, contrasena)
                if ok:
                    st.rerun()
                else:
                    st.error(mensaje)

    with st.expander(t("login.credenciales_titulo")):
        gestor = obtener_gestor_idioma()
        st.markdown(
            f"""
            | {t("login.tabla_rol")} | {t("login.tabla_usuario")} | {t("login.tabla_contrasena")} |
            |-----|------------------|------------|
            | {gestor.traducir_rol("Administrador")} | 1300004444 | adm123 |
            | {gestor.traducir_rol("Docente")} | 1300001111 | doc123 |
            | {gestor.traducir_rol("Estudiante")} | 1300002222 | est123 |
            """
        )


def pantalla_seleccion_rol(sistema):
    # Muestra la pantalla de login (alias para pantalla_login)
    pantalla_login(sistema)
