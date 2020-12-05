from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui


def Estado(ui):
    form = ui.estadoID.text()

    if form in ["", "0"]:
        return logB(ui, f"El campo FORMULARIO no peude estar vacio.", 3)
    script = f"""select * 
                 from estadorapido
                 where formulario={form}"""
    try:
        estado = pd.read_sql_query(script, con=engine)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
    MostrarEnTabla(estado, ui.estadoTabla, 0)
    ui.estadoTabla.setItem(0, 0, QtWidgets.QTableWidgetItem())
    ui.estadoTabla.item(0, 0).setBackground(QtGui.QColor(65, 65, 65))
    ui.estadoTabla.setItem(7, 0, QtWidgets.QTableWidgetItem())
    ui.estadoTabla.item(7, 0).setBackground(QtGui.QColor(65, 65, 65))
    ui.estadoTabla.setItem(17, 0, QtWidgets.QTableWidgetItem())
    ui.estadoTabla.item(17, 0).setBackground(QtGui.QColor(65, 65, 65))
    return 0
