import sys
import os
import datetime
import random
import pandas as pd
from dateutil import parser
from PyQt5 import QtWidgets, QtGui
from ui.gui import Ui_MainWindow as Uimw
from PyQt5.QtGui import QPalette, QColor
from procs.memes import redlestips
from paquetes import paquete0, paquete1, paquete2, paquete3, paquete5
from procs import (
    login,
    error9,
    reevaluar,
    reenviarP0,
    forzarBaja,
    forzarP8,
    cargarADH,
    asigReso,
    asigEf,
    logger,
    cruces,
)


if __name__ == "__main__":
    """[summary]"""

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
    ui.mainGroup.setEnabled(True)
    MainWindow.setWindowIcon(QtGui.QIcon("icon.ico"))
    ui.Main.setPixmap(QtGui.QPixmap("Main.png"))
    pixmap = QtGui.QPixmap("Main.png")
    pixmap2 = pixmap.scaledToWidth(16)
    pixmap3 = pixmap.scaledToHeight(16)

    MainWindow.setWindowTitle(f"[ SUPER Herramientas REDLES - v. ]")

    version = "1.10102020"

    ui.quoteLabel.setText(random.choice(redlestips))
    ui.loginButton.clicked.connect(lambda: login.Login(ui, version, MainWindow))
    ui.E9Boton.clicked.connect(lambda: error9.Error_9(ui))
    ui.reevBoton.clicked.connect(lambda: reevaluar.Reevaluar(ui))
    ui.reevUndo.clicked.connect(lambda: reevaluar.Deshacer_Reevaluar(ui))
    ui.rp0Boton.clicked.connect(lambda: reenviarP0.Reenviar_P0(ui))
    ui.fbajaBoton.clicked.connect(lambda: forzarBaja.Forzar_Baja(ui))
    ui.fp8Boton.clicked.connect(lambda: forzarP8.Forzar_P8(ui))
    ui.cadhBoton.clicked.connect(lambda: cargarADH.Cargar_ADH(ui))
    ui.asigReBoton.clicked.connect(lambda: asigReso.Asignar_Resolucion(ui))
    ui.asigEfCopiar.clicked.connect(lambda: logger.copiar_tabla(ui.asigEfTabla))
    ui.asigEfExcel.clicked.connect(lambda: asigEf.Subir_Excel_Asignacion(ui))
    ui.asigEfBoton.clicked.connect(lambda: asigEf.Asignado_Efectores(ui))
    ui.cruceEstadoBoton.clicked.connect(lambda: cruces.Cruce_Estado_DNI(ui))
    ui.paquete0BotonS.clicked.connect(lambda: paquete0.Paquete_0_Proceso(ui))
    ui.paquete0BotonP.clicked.connect(lambda: paquete0.Paquete_0_Salida(ui))
    ui.paquete2BotonP.clicked.connect(lambda: paquete2.Paquete_2_Proceso(ui))
    ui.paquete2BotonS.clicked.connect(lambda: paquete2.Paquete_2_Salida(ui))
    ui.paquete1Boton.clicked.connect(lambda: paquete1.Paquete_1(ui))
    ui.paquete3BotonS.clicked.connect(lambda: paquete3.Paquete_3_Subida(ui))
    ui.paquete3BotonE.clicked.connect(lambda: paquete3.Paquete_3_Entrada(ui))
    ui.paquete3BotonP.clicked.connect(lambda: paquete3.Paquete_3_Proceso(ui))
    ui.paquete3BotonA.clicked.connect(lambda: paquete3.Paquete_3_Archivo(ui))
    ui.paquete5Boton.clicked.connect(lambda: paquete5.Paquete_5(ui))

    ui.menuButtonSalir.clicked.connect(MainWindow.close)

    sys.exit(app.exec_())
