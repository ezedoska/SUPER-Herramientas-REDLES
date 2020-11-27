from sqlalchemy import create_engine
import urllib
server = (r"Driver={SQL Server};" + "Server=localhost,21433;" +
                f"Database=adm_efectores;UID=sqlemore;PWD=Eze2kftw!;")
# parseamos para que lo pueda leer bien sqlalchemy
urlserver = urllib.parse.quote_plus(server)

# creamos el motor de sqlengine dandole el parametro de urlserver
engine = create_engine(
    "mssql+pyodbc:///?odbc_connect={}".format(urlserver))