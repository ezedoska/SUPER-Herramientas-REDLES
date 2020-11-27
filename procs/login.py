from PyQt5 import QtWidgets, QtGui
from procs.logger import log
from procs.memes import redleshello
from procs.db import engine
import random
import pandas as pd
from robobrowser import RoboBrowser
import urllib3

urllib3.disable_warnings()


def Login(ui, version, MainWindow):
    """
    Logueo web, si está todo ok guarda un pickle para logueo offline
    """
    versionEXE = pd.read_sql_query(
        f"""SELECT ultimaversion 
            FROM [adm_efectores].[SQLemore].[ultimaversionExe]""",
        con=engine,
    )
    if versionEXE["ultimaversion"].iloc[0] != version:
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("ERROR")
        alert.setText(
            f"Estas usando una version vieja de este aplicativo,"
            + f"por favor actualizar a la version {versionEXE['ultimaversion'].iloc[0]}."
        )
        return alert.exec_()
    usr = ui.loginUsrBox.text()
    pwd = ui.loginPwBox.text()
    browser = RoboBrowser(parser="html.parser")
    browser.open(
        "https://registroefectores.desarrollosocial.gov.ar/logueo.asp", verify=False
    )
    login_form = browser.get_forms()
    login_form[0]["operador"].value = usr
    login_form[0]["clave"].value = pwd
    login_form[0].serialize()
    browser.submit_form(login_form[0])
    aspx_session_form = browser.get_forms()
    browser.submit_form(aspx_session_form[0])
    if browser.find(string="cerrar sesión usuario"):
        usr = pd.read_sql_query(
            f"""SELECT nombres 
                                    FROM operadores 
                                    WHERE ndocumento={usr}""",
            con=engine,
        )
        ui.tabMain.setEnabled(True)
        ui.loginGBox.setEnabled(False)
        log(ui)
        return MainWindow.setWindowTitle(
            f"[ SUPER Herramientas REDLES - v.{version} ] - "
            + f"Bienvenide {usr['nombres'].iloc[0]}.{random.choice(redleshello)}"
        )
    else:
        return MainWindow.setWindowTitle(
            f"[ SUPER Herramientas REDLES - v.{version} ] - LOGIN INCORRECTO."
        )
