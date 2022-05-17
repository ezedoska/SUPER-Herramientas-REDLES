from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
import random
from procs import memes


def Estado(ui):
    ui.estadoTabla.clear()
    Id = ui.estadoID.text()
    tipoForm = ui.estadoTipo.currentText()
    tipoDict = {
        "DNI": "DNI",
        "Persona Fisica": "Formulario",
        "Asociado": "Formulario",
        "Integrante": "Formulario",
        "Movimientos HR": "Movimientos HR",
    }
    andDict = {
        "DNI": "",
        "Persona Fisica": f"and [Tipo de Efector]='{tipoForm}'",
        "Asociado": f"and [Tipo de Efector]='{tipoForm}'",
        "Integrante": f"and [Tipo de Efector]='{tipoForm}'",
    }
    if Id in ["", "0"]:
        return logB(ui, f"El campo ID no peude estar vacio.", 3)
    if tipoForm == "Movimientos HR":
        script = f"""select apellidos,funcion,fecha 
                    from [VWExeStats]
                    where formusado='{Id}' order by fecha"""
    else:
        script = f"""select * 
                    from estadorapido
                    where {tipoDict[tipoForm]}={Id} {andDict[tipoForm]}"""
    try:
        estado = pd.read_sql_query(script, con=engine)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
    if estado.empty == False and tipoForm != "Movimientos HR":
        MostrarEnTabla(estado, ui.estadoTabla, 0)
        ui.estadoTabla.setItem(0, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(0, 0).setBackground(QtGui.QColor(65, 65, 65))
        ui.estadoTabla.setItem(10, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(10, 0).setBackground(QtGui.QColor(65, 65, 65))
        ui.estadoTabla.setItem(20, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(20, 0).setBackground(QtGui.QColor(65, 65, 65))
        ui.estadoTabla.setItem(28, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(28, 0).setBackground(QtGui.QColor(65, 65, 65))
    elif tipoForm == "Movimientos HR":
        MostrarEnTabla(estado, ui.estadoTabla)
        ui.estadoTabla.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
    else:
        logB(ui, f"No se encontro el ID {Id} en la base de {tipoForm}", 3)
        pass
    ui.quoteLabel.setText(random.choice(memes.redlestips))
    return 0


def Paquetes(ui):
    script = """SELECT *
               FROM PaquetesEnviados
               order by envio"""
    estado = pd.read_sql_query(script, con=engine)
    script2 = """SELECT *
               FROM estadopaquetes
               """
    estado2 = pd.read_sql_query(script2, con=engine)
    mensaje = estado2.iloc[0, 0]
    MostrarEnTabla(estado, ui.paquetesTabla)
    ui.paquetesTabla.horizontalHeader().setSectionResizeMode(
        QtWidgets.QHeaderView.ResizeToContents
    )
    logB(ui, mensaje)
    return 0
