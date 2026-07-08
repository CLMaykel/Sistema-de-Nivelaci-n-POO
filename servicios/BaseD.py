import pyodbc

try:
    import streamlit as st

    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False


class ConexionDB:
    def __init__(self):
        self.server = "localhost"
        self.database = "PROYECTOPOO"
        self.username = None
        self.password = None
        self.driver = "ODBC Driver 17 for SQL Server"
        self.use_trusted_connection = True
        self.conn = None
        self.cursor = None
        self._cargar_configuracion()

    def _cargar_configuracion(self):
        if not _HAS_STREAMLIT:
            return

        try:
            db = st.secrets["database"]
            self.server = db["server"]
            self.database = db["database"]
            self.username = db.get("username")
            self.password = db.get("password")
            self.driver = db.get("driver", "ODBC Driver 17 for SQL Server")
            self.use_trusted_connection = not (self.username and self.password)
        except (KeyError, FileNotFoundError, AttributeError):
            pass

    def conectar(self):
        try:
            if self.use_trusted_connection:
                conexion_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    "Trusted_Connection=yes;"
                    "TrustServerCertificate=yes;"
                )
            else:
                conexion_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password};"
                    "TrustServerCertificate=yes;"
                )

            self.conn = pyodbc.connect(conexion_str)
            self.cursor = self.conn.cursor()
            return self.conn

        except Exception as e:
            mensaje = "No se pudo conectar a la base de datos."
            if _HAS_STREAMLIT:
                st.error(mensaje)
                st.exception(e)
            else:
                print(f"{mensaje} {e}")
            return None

    def cerrar(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
