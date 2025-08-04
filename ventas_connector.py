import pymssql
import pandas as pd


def get_sqlserver_connection():
    """
    Establece una conexión con la base de datos SQL Server de Dentisalud.
    Asegúrate de tener instalado el ODBC Driver 17 for SQL Server en el entorno.
    """
    conn = pymssql.connect(
    server="147.182.194.168",
    user="sa",
    password="dEVOPS2022a",
    database="DENTISALUD"
)
    # conn = pyodbc.connect(
    # "DRIVER={ODBC Driver 17 for SQL Server};"
    #     "SERVER=147.182.194.168;"
    #     "DATABASE=DENTISALUD;"
    #     "UID=sa;"
    #     "PWD=dEVOPS2022a;"
    # )
    
        # "SERVER=sql8020.site4now.net;"
        # "DATABASE=db_a91131_test;"
        # "UID=db_a91131_test_admin;"
        # "PWD=dEVOPS2022;"
    return conn

def fetch_sample_data(table_name, top_n=10):
    """
    Consulta los primeros N registros de la tabla especificada.
    
    Args:
        table_name (str): Nombre de la tabla a consultar.
        top_n (int): Número de registros a traer (por defecto 10).
    
    Returns:
        pd.DataFrame: DataFrame con los datos consultados.
    """

    conn = get_sqlserver_connection()
    query = f"SELECT TOP {top_n} * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
