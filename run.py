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
from paquetes import (paquete0, paquete1, paquete2, paquete3, paquete5,
                      paquete8, paquete14, paquete15, somoso)
from procs import (login, error9, reevaluar, reenviarP0, bajaRetro, forzarP8,
                   cargarADH, asigReso, asigEf, logger, cruces, desasignar,
                   estado, cermi, PP, ForzarP3)

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
    ui.mainGroup.setEnabled(False)
    MainWindow.setWindowIcon(QtGui.QIcon("icon.ico"))
    ui.Main.setPixmap(QtGui.QPixmap("Main.png"))
    pixmap = QtGui.QPixmap("Main.png")
    pixmap2 = pixmap.scaledToWidth(16)
    pixmap3 = pixmap.scaledToHeight(16)
    version = "2.20220520"
    MainWindow.setWindowTitle(f"[ SUPER Herramientas REDLES - v.{version} ]")

    ui.quoteLabel.setText(random.choice(redlestips))
    ui.loginButton.clicked.connect(
        lambda: login.Login(ui, version, MainWindow))
    ui.E9Boton.clicked.connect(lambda: error9.Error_9(ui))
    ui.reevBoton.clicked.connect(lambda: reevaluar.Reevaluar(ui))
    ui.reevUndo.clicked.connect(lambda: reevaluar.Deshacer_Reevaluar(ui))
    ui.rp0Boton.clicked.connect(lambda: reenviarP0.Reenviar_P0(ui))
    ui.fbajaBoton.clicked.connect(lambda: bajaRetro.Baja_Retro(ui))
    ui.fp8Boton.clicked.connect(lambda: forzarP8.Forzar_P8(ui))
    ui.cadhBoton.clicked.connect(lambda: cargarADH.Cargar_ADH(ui))
    ui.asigReBoton.clicked.connect(lambda: asigReso.Asignar_Resolucion(ui))
    ui.asigEfCopiar.clicked.connect(
        lambda: logger.copiar_tabla(ui.asigEfTabla))
    ui.asigEfExcel.clicked.connect(lambda: asigEf.Subir_Excel_Asignacion(ui))
    ui.asigEfBoton.clicked.connect(lambda: asigEf.Asignado_Efectores(ui))
    ui.cruceEstadoBoton.clicked.connect(lambda: cruces.Cruce_Estado_DNI(ui))
    ui.desaBoton.clicked.connect(lambda: desasignar.Desasignado(ui))
    ui.cermiBoton.clicked.connect(lambda: cermi.Cermi_Subida(ui))
    ui.crucePrecariosBoton.clicked.connect(lambda: cermi.Cermi_Listado(ui))
    ui.estadoBoton.clicked.connect(lambda: estado.Estado(ui))
    ui.paquetesBoton.clicked.connect(lambda: estado.Paquetes(ui))
    ui.FP3Boton.clicked.connect(lambda: ForzarP3.Forzar_p3(ui))
    ui.PPInt.clicked.connect(lambda: PP.Int(ui))
    ui.PPAnexo.clicked.connect(lambda: PP.Anexo(ui))
    ui.PPBoton.clicked.connect(lambda: PP.AsigPP(ui))

    # ui.PPanexo.clicked.connect(lambda: PP.Anexo(ui))
    # ui.PPint.clicked.connect(lambda: PP.Int(ui))
    ui.menuButtonSalir.clicked.connect(MainWindow.close)

    sys.exit(app.exec_())
