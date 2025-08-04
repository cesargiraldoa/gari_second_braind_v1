import pyodbc
import pandas as pd

def ejecutar_sql(query):
    """
    Ejecuta una consulta SQL y retorna un DataFrame con los resultados.
    """
    try:
        # Credenciales reales (ajusta si cambian)
        server = "dentisalud-srv.database.windows.net"
        database = "core_dentisalud"
        username = "GariAdmin"
        password = "GariM1nd.2025"

        connection_string = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
        )

        conn = pyodbc.connect(connection_string)
        df = pd.read_sql(query, conn)
        conn.close()
        return df

    except Exception as e:
        print(f"❌ Error al ejecutar la consulta SQL: {e}")
        return pd.DataFrame()

def consultar_ventas(nombre_tabla="dbo.Prestaciones_Temporal", cantidad=10000):
    """
    Ejecuta una consulta SELECT TOP N desde la tabla especificada.
    """
    query = f"SELECT TOP {cantidad} * FROM {nombre_tabla}"
    return ejecutar_sql(query)
