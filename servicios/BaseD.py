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
        self.ultimo_error = None
        self._cargar_configuracion()

    # Carga la configuración de la base de datos desde secrets.toml
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

    # Establece la conexión a SQL Server
    def conectar(self, silencioso=True):
        self.ultimo_error = None
        try:
            if self.use_trusted_connection:
                conexion_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    "Trusted_Connection=yes;"
                    "TrustServerCertificate=yes;"
                    "Connection Timeout=8;"
                )
            else:
                conexion_str = (
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password};"
                    "TrustServerCertificate=yes;"
                    "Connection Timeout=8;"
                )

            self.conn = pyodbc.connect(conexion_str)
            self.cursor = self.conn.cursor()
            return self.conn

        except Exception as e:
            self.ultimo_error = str(e)
            if not silencioso and _HAS_STREAMLIT:
                st.error("No se pudo conectar a la base de datos.")
            elif not silencioso:
                print(f"No se pudo conectar a la base de datos. {e}")
            return None

    # Ejecuta una consulta SQL de modificación (INSERT, UPDATE, DELETE)
    def ejecutar(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    # Ejecuta una consulta SQL y retorna un único registro
    def consultar_uno(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

    # Ejecuta una consulta SQL y retorna todos los registros
    def consultar_todos(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    # Obtiene el siguiente ID disponible para una tabla
    def siguiente_id(self, tabla, columna):
        fila = self.consultar_uno(f"SELECT ISNULL(MAX({columna}), 0) + 1 FROM {tabla}")
        return fila[0] if fila else 1

    # Cierra la conexión y el cursor
    def cerrar(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None
        if self.conn:
            self.conn.close()
            self.conn = None

    # Context manager: abre la conexión al entrar
    def __enter__(self):
        self.conectar()
        return self

    # Context manager: cierra la conexión al salir
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and self.conn:
            self.conn.rollback()
        self.cerrar()
        return False
