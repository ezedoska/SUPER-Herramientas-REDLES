from sqlalchemy import create_engine
import urllib

Ip = "192.168.1.40,21433"
# Ip = "localhost,21433"
server = (
    r"Driver={SQL Server};"
    + f"Server={Ip};"
    + f"Database=adm_efectores;UID=sqlemore;PWD=Eze2kftw!;"
)
# parseamos para que lo pueda leer bien sqlalchemy
urlserver = urllib.parse.quote_plus(server)

# creamos el motor de sqlengine dandole el parametro de urlserver
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(urlserver))
