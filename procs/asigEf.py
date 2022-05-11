from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
from rich import console
from procs.console import console


def Subir_Excel_Asignacion(ui):
    ui.asigEfTabla.setRowCount(0)

    df1 = pd.read_excel("asignacion.xlsx", engine='openpyxl')
    df = df1.dropna(how='any', axis=0, subset=['Form', 'TipoEf', 'Expediente', 'Dependencia',
                    'Caja'])

    if df.empty:
        return logB(ui, "El excel esta vacio", 2)

    if len(df.Expediente.unique()) > 1:
        return logB(ui,
                    "Hay mas de un n° de expediente en la columna Expediente",
                    2)
    if len(df.Dependencia.unique()) > 1:
        return logB(ui, "Hay mas de una dependencia en la columna Dependencia",
                    2)
    if len(df.Caja.unique()) > 1:
        return logB(ui, "Hay mas de un n° de caja en la columna Caja", 2)

    exp = df.iloc[0, 2]
    console.log("Locals", log_locals=True)
    try:
        with engine.begin() as connection:
            connection.execute("DELETE FROM Asignacion")
        df.to_sql("Asignacion",
                  con=engine,
                  if_exists="append",
                  index=False,
                  schema="dbo")
        ui.asigEfTipo.setEnabled(True)
        ui.asigEfBoton.setEnabled(True)
        ui.asigEfExcel.setEnabled(False)
        return logB(ui, f"[{exp}]El excel se cargo correctamente.", 1)
    except Exception as e:
        return logB(ui, f"[{exp}]Hubo un error: {str(e)}", 3)


def Asignado_Efectores(ui):
    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943
    tipoasignacion = ui.asigEfTipo.currentText()

    tipo = tipoasignacion[0] + tipoasignacion[1]
    tipoexp = tipoasignacion[2]
    console.log("Locals", log_locals=True)
    try:
        with engine.begin() as connection:
            connection.execute(f"""EXEC  [AsignarExpedientesGDE]
                @tipo = {tipo},
                @tipoexp = {tipoexp},
                @user = {userdni}""")
    except Exception as e:
        return logB(ui, f"Hubo un error en la asignacion: {str(e)}", 3)

    log(ui)

    ui.asigEfTipo.setEnabled(False)
    ui.asigEfBoton.setEnabled(False)
    ui.asigEfExcel.setEnabled(True)
    try:
        result = pd.read_sql_query(
            """SELECT * 
               FROM [adm_efectores].dbo.[temp_Noasignados]""",
            con=engine,
        )
    except Exception as e:
        return logB(ui, f"Hubo un error buscando no asignados: {str(e)}", 3)

    if result.empty:
        return logB(ui, f"El asignado termino sin errores.", 1)
    MostrarEnTabla(result, ui.asigEfTabla)
    ui.asigEfTabla.horizontalHeader().setSectionResizeMode(
        QtWidgets.QHeaderView.ResizeToContents)
    return logB(ui, f"El asignado termino con errores.", 1)
