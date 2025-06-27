
import pyodbc

def conectar_bd():
    try:
        conexion = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=localhost;'
            'DATABASE=AlbergueFrontera;'
            'UID=sa;'
            'PWD=1234;'
            'TrustServerCertificate=yes;'
        )
        return conexion
    except Exception as e:
        print("Error al conectar con la base de datos:", e)
        return None
