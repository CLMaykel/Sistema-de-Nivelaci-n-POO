import streamlit as st

from interfaz.components.tables import usuario_to_dict


def _formulario_estudiante(sistema):
    st.subheader("Registrar estudiante")

    with st.form("form_estudiante"):
        cedula = st.text_input("Cedula")
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
        correo = st.text_input("Correo")
        contrasena = st.text_input("Contrasena", type="password")
        telefono = st.text_input("Telefono")
        tipo_documento = st.selectbox("Tipo de documento", ["Cedula", "Pasaporte"])
        fecha_nacimiento = st.text_input("Fecha de nacimiento (AAAA-MM-DD)")
        discapacidad = st.checkbox("Discapacidad")

        enviado = st.form_submit_button("Registrar estudiante")

    if enviado:
        try:
            if not all([cedula, nombres, apellidos, correo, contrasena, telefono, fecha_nacimiento]):
                raise ValueError("Complete todos los campos obligatorios")

            estudiante = sistema.registrar_usuario(
                "Estudiante",
                cedula.strip(),
                nombres.strip(),
                apellidos.strip(),
                correo.strip(),
                contrasena.strip(),
                telefono.strip(),
                tipo_documento=tipo_documento,
                fecha_nacimiento=fecha_nacimiento.strip(),
                discapacidad=discapacidad,
            )
            st.success(
                f"Estudiante registrado: {estudiante.nombres} {estudiante.apellidos}. "
                f"Estado de nivelacion: {estudiante.estado_nivelacion}"
            )
        except Exception as error:
            st.error(str(error))


def mostrar_usuarios(sistema):
    st.title("Usuarios")

    _formulario_estudiante(sistema)

    st.divider()
    st.subheader("Usuarios registrados")

    if not sistema.usuarios:
        st.warning("No hay usuarios registrados.")
        return

    filas = [usuario_to_dict(usuario) for usuario in sistema.usuarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
