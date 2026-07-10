import streamlit as st

from interfaz.branding import (
    COLOR_BLANCO,
    COLOR_GRIS_OSCURO,
    COLOR_NEGRO,
    COLOR_NEGRO_SUAVE,
    COLOR_ROJO,
    COLOR_VERDE,
    FACULTAD,
    SIGLAS,
    UNIVERSIDAD,
)


def aplicar_estilos():
    """Aplica los estilos CSS principales a toda la interfaz de la aplicación"""
    st.markdown(
        f"""
        <style>
            .main {{
                background-color: #eceae6;
            }}
            .main .block-container {{
                color: {COLOR_NEGRO};
            }}
            .main h1, .main h2, .main h3, .main h4 {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stCaptionContainer"] p,
            [data-testid="stCaptionContainer"] {{
                color: {COLOR_GRIS_OSCURO} !important;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {COLOR_NEGRO} 0%, {COLOR_NEGRO_SUAVE} 100%);
                border-right: 3px solid {COLOR_ROJO};
            }}
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] .stMarkdown,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stSelectbox label {{
                color: #e8e8e8 !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="select"] {{
                background-color: {COLOR_NEGRO_SUAVE} !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="select"] * {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stRadio label {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stRadio label:hover {{
                color: {COLOR_VERDE} !important;
            }}
            [data-testid="stSidebar"] [data-testid="stAlert"] {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stSidebar"] [data-testid="stAlert"] * {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stMetric"] {{
                background-color: #faf8f5;
                border-left: 4px solid {COLOR_VERDE};
                border-bottom: 2px solid {COLOR_ROJO};
                border-radius: 8px;
                padding: 12px;
                box-shadow: 0 2px 6px rgba(26, 26, 26, 0.06);
            }}
            [data-testid="stMetric"] label {{
                color: {COLOR_GRIS_OSCURO} !important;
            }}
            [data-testid="stMetric"] [data-testid="stMetricValue"] {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stForm"] {{
                background-color: #faf8f5;
                border: 1px solid #d8d2ca;
                border-top: 3px solid {COLOR_ROJO};
                border-radius: 10px;
                padding: 16px;
                box-shadow: 0 1px 4px rgba(26, 26, 26, 0.05);
            }}
            h1 {{
                color: {COLOR_NEGRO};
                border-left: 5px solid {COLOR_VERDE};
                padding-left: 10px;
            }}
            h2, h3 {{
                color: {COLOR_NEGRO_SUAVE};
            }}
            [data-testid="stCaptionContainer"] {{
                color: {COLOR_GRIS_OSCURO};
            }}
            .stButton > button {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border: none;
            }}
            .stButton > button:hover {{
                background-color: {COLOR_NEGRO};
                color: {COLOR_BLANCO};
            }}
            .role-icon-wrap {{
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 90px;
                padding: 8px 4px;
            }}
            .role-icon {{
                font-size: 4rem;
                line-height: 1;
                display: block;
            }}
            .role-desc {{
                color: {COLOR_GRIS_OSCURO};
                font-size: 1rem;
                line-height: 1.5;
                margin: 0;
            }}
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border-top: 4px solid {COLOR_ROJO} !important;
                background: #faf8f5;
                padding: 4px 0;
            }}
            .role-badge {{
                display:inline-block;
                padding:6px 12px;
                border-radius:999px;
                font-weight:600;
                font-size:0.85rem;
                background:{COLOR_NEGRO};
                color:{COLOR_BLANCO};
                margin-bottom:8px;
            }}
            .role-card {{
                background:#faf8f5 !important;
                border:1px solid #d8d2ca;
                border-top:4px solid {COLOR_ROJO};
                border-radius:12px;
                padding:18px;
                box-shadow:0 2px 8px rgba(26,26,26,0.08);
                margin-bottom:14px;
            }}
            .role-card h2 {{
                color:{COLOR_NEGRO} !important;
                margin-bottom:4px;
            }}
            .role-card p {{
                color:{COLOR_GRIS_OSCURO} !important;
                font-size:0.95rem;
            }}
            .readonly-box {{
                background:#f7f7f7 !important;
                border-left:4px solid {COLOR_VERDE};
                padding:12px 14px;
                border-radius:8px;
                margin-bottom:12px;
                color:{COLOR_NEGRO_SUAVE} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def aplicar_estilos_login():
    """Aplica estilos CSS específicos para la página de login"""
    fondo_login = "#dfe4df"
    fondo_suave = "#f3f1ec"
    tarjeta = "#faf7f2"
    tarjeta_alt = "#f0ece6"
    borde = "#d5cec4"
    texto_suave = "#5a5a56"
    st.markdown(
        f"""
        <style>
            section[data-testid="stSidebar"] {{
                display: none !important;
            }}
            header[data-testid="stHeader"] {{
                background: transparent !important;
            }}
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(
                    165deg,
                    {fondo_login} 0%,
                    #d8ddd6 38%,
                    #e4e8e2 72%,
                    #d3d9d2 100%
                ) !important;
            }}
            .main {{
                background: transparent !important;
            }}
            .main .block-container {{
                max-width: 720px !important;
                padding-top: 0.75rem !important;
                padding-bottom: 2rem !important;
            }}
            .login-hero {{
                text-align: center;
                margin: 0.75rem 0 1.35rem 0;
                padding: 1.85rem 1.35rem 1.45rem 1.35rem;
                background: linear-gradient(180deg, {tarjeta} 0%, {tarjeta_alt} 100%);
                border-radius: 20px;
                border: 1px solid {borde};
                box-shadow: 0 12px 28px rgba(45, 45, 45, 0.06);
                position: relative;
                overflow: hidden;
            }}
            .login-hero::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, {COLOR_ROJO} 0%, #e8c4c8 50%, {COLOR_VERDE} 100%);
            }}
            .login-hero-logo {{
                width: min(240px, 72vw);
                height: auto;
                margin: 0.35rem auto 0.9rem auto;
                display: block;
                filter: drop-shadow(0 5px 12px rgba(0, 0, 0, 0.12));
            }}
            .login-hero-siglas {{
                color: {COLOR_VERDE};
                font-size: 1.55rem;
                font-weight: 800;
                letter-spacing: 0.1em;
                margin: 0 0 0.35rem 0;
            }}
            .login-hero-title {{
                color: #2f2f2b;
                font-size: 1.32rem;
                font-weight: 700;
                margin: 0 0 0.45rem 0;
                line-height: 1.35;
            }}
            .login-hero-subtitle {{
                color: {texto_suave};
                font-size: 0.9rem;
                margin: 0;
                line-height: 1.5;
            }}
            .login-hero-band {{
                display: flex;
                justify-content: center;
                gap: 8px;
                margin-top: 1.1rem;
            }}
            .login-hero-band span {{
                display: inline-block;
                width: 42px;
                height: 4px;
                border-radius: 999px;
            }}
            .login-hero-band .rojo {{ background: {COLOR_ROJO}; opacity: 0.85; }}
            .login-hero-band .blanco {{ background: #c8c2b8; }}
            .login-hero-band .verde {{ background: {COLOR_VERDE}; opacity: 0.85; }}
            .main [data-testid="stAlert"] {{
                background: #f8f0d8 !important;
                border: 1px solid #e2d4b2 !important;
                border-radius: 12px !important;
                color: #5c4f32 !important;
            }}
            .main [data-testid="stAlert"] * {{
                color: #5c4f32 !important;
            }}
            .main [data-testid="stForm"] {{
                background: linear-gradient(180deg, {tarjeta} 0%, {fondo_suave} 100%);
                border: 1px solid {borde};
                border-radius: 18px;
                padding: 1.4rem 1.55rem 0.85rem 1.55rem !important;
                box-shadow: 0 8px 20px rgba(45, 45, 45, 0.05);
            }}
            .main [data-testid="stForm"] label {{
                color: {texto_suave} !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
            }}
            .main [data-testid="stTextInput"] input {{
                background: #fffcf8 !important;
                border-radius: 10px !important;
                border: 1px solid #cfc7bc !important;
                color: #33332f !important;
            }}
            .main [data-testid="stTextInput"] input:focus {{
                border-color: {COLOR_VERDE} !important;
                box-shadow: 0 0 0 2px rgba(0, 150, 57, 0.12) !important;
            }}
            .main [data-testid="stFormSubmitButton"] button {{
                background: linear-gradient(90deg, {COLOR_ROJO} 0%, #b31228 100%) !important;
                color: {COLOR_BLANCO} !important;
                border: none !important;
                font-weight: 700 !important;
                letter-spacing: 0.03em;
                padding: 0.68rem 1rem !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 14px rgba(206, 17, 38, 0.2);
            }}
            .main [data-testid="stFormSubmitButton"] button:hover {{
                background: #3a3a36 !important;
                box-shadow: 0 4px 14px rgba(58, 58, 54, 0.22);
            }}
            .main .stButton > button {{
                font-weight: 700 !important;
                border-radius: 8px !important;
                background: #ebe6df !important;
                color: #4a4a46 !important;
                border: 1px solid #cfc7bc !important;
            }}
            .main .stButton > button[kind="primary"] {{
                background: {COLOR_ROJO} !important;
                color: {COLOR_BLANCO} !important;
                border: none !important;
            }}
            .main [data-testid="stExpander"] {{
                background: {tarjeta};
                border: 1px solid {borde};
                border-radius: 14px;
            }}
            .main [data-testid="stExpander"] summary {{
                color: {texto_suave} !important;
            }}
            .main hr {{
                border-color: #c9c2b8 !important;
                opacity: 0.55;
            }}
            [data-testid="stCaptionContainer"] p {{
                color: {texto_suave} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def pie_pagina():
    """Renderiza el pie de página con información de la universidad"""
    st.markdown(
        f'<hr style="border:none;border-top:2px solid {COLOR_VERDE};margin-top:24px;">',
        unsafe_allow_html=True,
    )
    st.caption(f"{SIGLAS} · {UNIVERSIDAD} · {FACULTAD}")
