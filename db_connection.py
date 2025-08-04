import os
import pyodbc
import pandas as pd

def ejecutar_sql(query):
    """
    Ejecuta una consulta SQL y retorna un DataFrame con los resultados.
    """
    try:
        # Puedes parametrizar esto con variables de entorno si prefieres
        server = os.getenv("SQL_SERVER", "tu_servidor.database.windows.net")
        database = os.getenv("SQL_DATABASE", "tu_base_datos")
        username = os.getenv("SQL_USER", "tu_usuario")
        password = os.getenv("SQL_PASSWORD", "tu_contraseña")

        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt=no;"
            f"TrustServerCertificate=yes;"
        )

        conn = pyodbc.connect(connection_string)
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        print(f"❌ Error al ejecutar la consulta SQL: {e}")
        return pd.DataFrame()
