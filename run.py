import sys
import os
import datetime
import random
import urllib
import pandas as pd
from sqlalchemy import create_engine
from dateutil import parser
from PyQt5 import QtWidgets, QtGui
import pyodbc
from ui.gui import Ui_MainWindow as Uimw
from PyQt5.QtGui import QPalette, QColor
from procs import login,error9,reevaluar,reenviarP0,forzarBaja


if __name__ == "__main__":
    """[summary]
    """

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    MainWindow = QtWidgets.QMainWindow()
    ui = Uimw()
    ui.setupUi(MainWindow)

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)
    app.setStyleSheet(
        "QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }"
    )

    MainWindow.show()
    ui.tabMain.setEnabled(True)
    # MainWindow.setWindowIcon(QtGui.QIcon('icon.ico'))
    MainWindow.setWindowTitle(f'[ Herramientas REDLES 2 - v. ]')
    server = (r"Driver={SQL Server};" + "Server=localhost,21433;" +
                  f"Database=adm_efectores;UID=sqlemore;PWD=Eze2kftw!;")
    # parseamos para que lo pueda leer bien sqlalchemy
    urlserver = urllib.parse.quote_plus(server)

    # creamos el motor de sqlengine dandole el parametro de urlserver
    engine = create_engine(
        "mssql+pyodbc:///?odbc_connect={}".format(urlserver))
    version = '1.10102020'

    # ui.quoteLabel.setText(random.choice(redlestips))
    ui.loginButton.clicked.connect(lambda: login.go(engine,ui,version,MainWindow))
    ui.E9Boton.clicked.connect(lambda: error9.go(engine,ui))
    # ui.menuButtonCU.clicked.connect(ChangeUser)
    ui.reevBoton.clicked.connect(lambda: reevaluar.go(engine,ui))
    ui.reevUndo.clicked.connect(lambda: reevaluar.undo(engine,ui))
    ui.rp0Boton.clicked.connect(lambda: reenviarP0.go(engine,ui))
    ui.fbajaBoton.clicked.connect(lambda: forzarBaja.go(engine,ui))
    # ui.ansesButton.clicked.connect(GetEstadoANSES)
    # ui.paquetesButton.clicked.connect(GetPaquetes)
    # ui.asigexpefButtonCE.clicked.connect(UploadExcel)
    # ui.redlesButtonCE.clicked.connect(GetEstadoREDLES)
    # ui.redlesANSESButtonCE.clicked.connect(GetEstadoANSES2)
    # ui.redlesAnexoButton.clicked.connect(GetAnexos)
    # ui.redlesCoopMatriculaButton.clicked.connect(GetCoopesPorMatricula)
    # ui.adhButton.clicked.connect(SearchADH)
    ui.menuButtonSalir.clicked.connect(MainWindow.close)

    sys.exit(app.exec_())
