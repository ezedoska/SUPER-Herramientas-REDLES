from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
import datetime
import os


def Cermi_Subida(ui):
    ui.cermiTabla.setRowCount(0)
    ui.estadoTabla.clear()

    df = pd.read_excel("cermi.xlsx")

    # if len(df.Expediente.unique()) > 1:
    #     return logB(ui, "Hay mas de un n° de expediente en la columna Expediente", 2)
    # if len(df.Dependencia.unique()) > 1:
    #     return logB(ui, "Hay mas de una dependencia en la columna Dependencia", 2)
    # if len(df.Caja.unique()) > 1:
    #     return logB(ui, "Hay mas de un n° de caja en la columna Caja", 2)

    try:
        with engine.begin() as connection:
            connection.execute("DELETE FROM proc_cermi")
        df.to_sql(
            "proc_cermi", con=engine, if_exists="append", index=False, schema="dbo"
        )
    except Exception as e:
        return logB(ui, f"Hubo un error subiendo el excel: {str(e)}", 3)

    try:
        with engine.begin() as connection:
            connection.execute(f"""EXEC  proc_InsCermi""")
    except Exception as e:
        return logB(ui, f"Hubo un error en la carga CERMI: {str(e)}", 3)
    log(ui)
    try:
        result = pd.read_sql_query(
            """SELECT * 
               FROM [adm_efectores].dbo.[ErroresCermi]""",
            con=engine,
        )
    except Exception as e:
        return logB(ui, f"Hubo un error buscando no cargados: {str(e)}", 3)

    if result.empty:
        return logB(ui, f"La carga CERMI termino sin errores.", 1)
    MostrarEnTabla(result, ui.cermiTabla)
    return logB(ui, f"La carga CERMI termino con errores.", 2)


def Cermi_Listado(ui):
    script = """
                    SELECT * from cruceprecarios order by estado
                """
    df = pd.read_sql_query(script, con=engine)

    fechaexcel = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")
    path = os.path.join(
        os.path.expanduser("~"), "Desktop", f"Cruce_Precarios-{fechaexcel}"
    )
    file_name = QtWidgets.QFileDialog.getSaveFileName(
        ui.tabMain, "Save file", path, ".xlsx"
    )
    if file_name[0]:
        writer = pd.ExcelWriter(file_name[0] + file_name[1], engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Estado precarios", encoding="unicode")
        writer.save()
        log(ui)
        return logB(ui, f"El cruce se genero correctamente", 1)
    else:
        pass
    return 0