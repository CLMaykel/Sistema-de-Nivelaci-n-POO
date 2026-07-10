import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import intro_modulo, tabla_o_vacio
from interfaz.idioma import t
from modelos.admin import Administrador
from servicios.importador_csv import (
    CONFIG_TIPOS,
    importar_filas,
    leer_csv,
    listar_tipos_entidad,
    obtener_config_tipo,
    obtener_plantilla_csv,
    validar_columnas,
)


def _etiqueta_tipo(tipo: str) -> str:
    return t(f"import.tipo.{tipo}")


def _resumen_tipos():
    filas = []
    for tipo in listar_tipos_entidad():
        config = CONFIG_TIPOS[tipo]
        columnas = ", ".join(config["columnas_requeridas"])
        filas.append(
            {
                "Orden": config["orden"],
                "Tipo": _etiqueta_tipo(tipo),
                "Columnas requeridas": columnas,
                "Descripcion": t(f"import.desc.{tipo}"),
            }
        )
    return filas


def _mostrar_resultado(resultado):
    if resultado.hubo_exito:
        st.success(
            t(
                "import.resultado_ok",
                importadas=resultado.importadas,
                total=resultado.total_filas,
            )
        )
    else:
        st.error(t("import.resultado_vacio"))

    if resultado.omitidas:
        st.warning(t("import.resultado_omitidas", omitidas=resultado.omitidas))

    if resultado.errores:
        st.markdown(f"**{t('import.errores_titulo')}**")
        for error in resultado.errores:
            st.markdown(f"- {error}")


def _tab_guia():
    intro_modulo(t("import.intro_guia"), "📋")
    st.markdown(t("import.orden_recomendado"))
    tabla_o_vacio(_resumen_tipos(), t("import.sin_tipos"))

    st.divider()
    st.markdown(f"**{t('import.notas_titulo')}**")
    st.markdown(t("import.nota_persistencia"))
    st.markdown(t("import.nota_referencias"))
    st.markdown(t("import.nota_duplicados"))


def _tab_importar(sistema):
    intro_modulo(t("import.intro_importar"), "📥")

    tipos = listar_tipos_entidad()
    etiquetas = {_etiqueta_tipo(t): t for t in tipos}
    etiqueta_sel = st.selectbox(t("import.seleccion_tipo"), list(etiquetas.keys()))
    tipo = etiquetas[etiqueta_sel]
    config = obtener_config_tipo(tipo)

    st.caption(t(f"import.desc.{tipo}"))
    st.markdown(
        f"**{t('import.columnas_requeridas')}:** `{', '.join(config['columnas_requeridas'])}`"
    )
    if config["columnas_opcionales"]:
        st.markdown(
            f"**{t('import.columnas_opcionales')}:** `{', '.join(config['columnas_opcionales'])}`"
        )

    st.download_button(
        t("import.descargar_plantilla"),
        data=obtener_plantilla_csv(tipo),
        file_name=f"plantilla_{tipo}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    archivo = st.file_uploader(t("import.subir_csv"), type=["csv"], key=f"csv_{tipo}")

    if not archivo:
        return

    filas = leer_csv(archivo.getvalue())
    if not filas:
        st.warning(t("import.archivo_vacio"))
        return

    errores = validar_columnas(filas, tipo)
    if errores:
        for error in errores:
            st.error(error)
        return

    preview = [{k: v for k, v in fila.items() if k != "_fila_csv"} for fila in filas[:5]]
    st.markdown(f"**{t('import.vista_previa')}** ({min(len(filas), 5)} / {len(filas)})")
    st.dataframe(preview, use_container_width=True, hide_index=True)

    if st.button(t("import.ejecutar"), type="primary", use_container_width=True):
        resultado = importar_filas(sistema, tipo, filas)
        _mostrar_resultado(resultado)


def mostrar_importar_datos(sistema):
    encabezado_pagina(t("import.titulo"), periodo=sistema.periodo_actual)

    administrador = obtener_usuario_actual(sistema)
    if not isinstance(administrador, Administrador):
        st.error(t("import.solo_admin"))
        return

    if not st.session_state.get("db_cargada"):
        st.info(t("import.modo_demo"))

    tab_guia, tab_importar = st.tabs([t("import.tab_guia"), t("import.tab_importar")])

    with tab_guia:
        _tab_guia()

    with tab_importar:
        _tab_importar(sistema)
