from procs.memes import redlestips
import random
import inspect
import types
from typing import cast
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
import pandas as pd


def copiar_tabla(table):
    col_count = table.columnCount()
    row_count = table.rowCount()
    headers = [
        str(table.horizontalHeaderItem(i).text()) for i in range(col_count)
    ]

    # df indexing is slow, so use lists
    df_list = []
    for row in range(row_count):
        df_list2 = []
        for col in range(col_count):
            table_item = table.item(row, col)
            df_list2.append(
                "" if table_item is None else str(table_item.text()))
        df_list.append(df_list2)

    df = pd.DataFrame(df_list, columns=headers)

    return df.to_clipboard(sep="\t", index=False)


def MostrarEnTabla(df, table, orientacion=1):
    headers = list(df)
    if orientacion == 1:
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.horizontalHeader().setVisible(True)
        table.setHorizontalHeaderLabels(headers)
        # getting data from df is computationally costly so convert it to array first
        df_array = df.values
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                table.setItem(
                    row, col,
                    QtWidgets.QTableWidgetItem(str(df_array[row, col])))
        return 0
    table.horizontalHeader().setVisible(False)
    header = table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
    table.setRowCount(df.shape[1])
    table.setColumnCount(df.shape[0])
    table.setVerticalHeaderLabels(headers)
    # getting data from df is computationally costly so convert it to array first
    df_array = df.values
    for col in range(df.shape[1]):
        for row in range(df.shape[0]):
            table.setItem(row, col,
                          QtWidgets.QTableWidgetItem(str(df_array[row, col])))
    return 0


def log(ui, formusado=""):
    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943
    procname = inspect.stack()[1][3]
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""INSERT INTO [adm_efectores].[SQLemore].[ExeStats] 
                                    (funcion,fecha,usuario, formusado) 
                                    VALUES ('{procname}',getdate(),'{userdni}','{formusado}')"""
            )
    except Exception as e:
        return logB(ui, f"Ocurrio un error logeando a la DB: {str(e)}", 3)
    ui.quoteLabel.setText(random.choice(redlestips))
    return 0


def logB(ui, mensaje, tipo=0, contitulo=1, size=4):
    if tipo == 1:
        icono = "✔"
    elif tipo == 2:
        icono = "✘"
    elif tipo == 3:
        icono = "⚠"
    else:
        icono = ""
    procname = inspect.stack()[1][3]
    if contitulo == 1:
        return ui.log.append(
            f"<h{size}>{icono} {procname}:</h{size}>  {icono} {mensaje}")
    return ui.log.append(f"{icono} {mensaje}")
