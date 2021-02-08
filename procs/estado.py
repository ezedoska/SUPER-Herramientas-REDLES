from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui


def Estado(ui):
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
        script = f"""select * 
                    from [adm_efectores].[SQLemore].[ExeStats]
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
        ui.estadoTabla.setItem(7, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(7, 0).setBackground(QtGui.QColor(65, 65, 65))
        ui.estadoTabla.setItem(17, 0, QtWidgets.QTableWidgetItem())
        ui.estadoTabla.item(17, 0).setBackground(QtGui.QColor(65, 65, 65))
    elif tipoForm == "Movimientos HR":
        MostrarEnTabla(estado, ui.estadoTabla)
    else:
        logB(ui, f"No se encontro el ID {Id} en la base de {tipoForm}", 3)
        pass
    return 0
