from PyQt5 import QtWidgets, QtGui
from procs.logger import log
from procs.memes import redleshello
from procs.db import engine
import random
import pandas as pd
import os

# from robobrowser import RoboBrowser
import urllib3
from procs.logger import log, logB
from procs.console import console

urllib3.disable_warnings()


def Login(ui, version, MainWindow):
    # """
    # Logueo web, si está todo ok guarda un pickle para logueo offline
    # """
    # try:
    #     versionEXE = pd.read_sql_query(
    #         f"""SELECT ultimaversion
    #             FROM [adm_efectores].[SQLemore].[ultimaversionExe]""",
    #         con=engine,
    #     )
    # except Exception as e:
    #     return logB(ui, f"Error leyendo version en la base: {str(e)}", 3)
    # if versionEXE["ultimaversion"].iloc[0] != version:
    #     alert = QtWidgets.QMessageBox()
    #     alert.setWindowTitle("ERROR")
    #     alert.setText(
    #         f"Estas usando una version vieja de este aplicativo,"
    #         + f"por favor actualizar a la version {versionEXE['ultimaversion'].iloc[0]}."
    #     )
    #     return alert.exec_()
    # usr = ui.loginUsrBox.text()
    # pwd = ui.loginPwBox.text()
    # browser = RoboBrowser(parser="html.parser")
    # browser.open(
    #     "https://registroefectores.desarrollosocial.gov.ar/logueo.asp", verify=False
    # )
    # login_form = browser.get_forms()
    # login_form[0]["operador"].value = usr
    # login_form[0]["clave"].value = pwd
    # login_form[0].serialize()
    # browser.submit_form(login_form[0])
    # aspx_session_form = browser.get_forms()
    # browser.submit_form(aspx_session_form[0])
    # if browser.find(string="cerrar sesión usuario"):
    #     try:
    #         usr = pd.read_sql_query(
    #             f"""SELECT nombres
    #                                     FROM operadores
    #                                     WHERE ndocumento={usr}""",
    #             con=engine,
    #         )
    #     except Exception as e:
    #         return logB(ui, f"Log in error: {str(e)}", 3)
    #     ui.mainGroup.setEnabled(True)
    #     ui.loginGBox.setEnabled(False)
    #     log(ui)
    #     return MainWindow.setWindowTitle(
    #         f"[ SUPER Herramientas REDLES - v.{version} ] - "
    #         + f"Bienvenide {usr['nombres'].iloc[0]}.{random.choice(redleshello)}"
    #     )
    # else:
    #     return MainWindow.setWindowTitle(
    #         f"[ SUPER Herramientas REDLES - v.{version} ] - LOGIN INCORRECTO."
    #     )
    computer = os.environ["COMPUTERNAME"]

    if "VDM" or "vdm" in computer:
        Ip = "192.168.1.40,21433"
    else:
        # Ip = "localhost,21433"
        Ip = "127.0.0.1,21433"

    usr = ui.loginUsrBox.text()
    pwd = ui.loginPwBox.text()
    try:
        versionEXE = pd.read_sql_query(
            f"""SELECT ultimaversion
                FROM [adm_efectores].[SQLemore].[ultimaversionExe]""",
            con=engine,
        )
    except Exception as e:

        return logB(ui, f"Error leyendo version en la base{Ip}: {str(e)}", 3)
    if versionEXE["ultimaversion"].iloc[0] != version:
        alert = QtWidgets.QMessageBox()
        alert.setWindowTitle("ERROR")
        alert.setText(
            f"Estas usando una version vieja de este aplicativo,"
            + f"por favor actualizar a la version {versionEXE['ultimaversion'].iloc[0]}."
        )
        return alert.exec_()
    try:
        usrLog = pd.read_sql_query(
            f"""SELECT nombres,observaciones
                                         FROM operadores
                                         WHERE ndocumento={usr} and palabraclave='{pwd}'""",
            con=engine,
        )
    except:
        console.print_exception(show_locals=True)
        e = console.print_exception(show_locals=True)
        logB(ui, f"Error leyendo usuario en la base: {str(e)}", 3)
        return logB(ui, console.print_exception(show_locals=True), 3)
    if usrLog.empty == False:
        ui.mainGroup.setEnabled(True)
        ui.loginGBox.setEnabled(False)
        # print(str(usrLog['Observaciones'].iloc[0]))
        if "(SHR)" in str(usrLog["observaciones"].iloc[0]):
            ui.tabPaquetes.setEnabled(True)
        else:
            ui.tabPaquetes.setEnabled(False)
        log(ui)
        return MainWindow.setWindowTitle(
            f"[ SUPER Herramientas REDLES - v.{version} ] - "
            + f"Bienvenide {usrLog['nombres'].iloc[0]}.{random.choice(redleshello)}"
        )
    else:
        return MainWindow.setWindowTitle(
            f"[ SUPER Herramientas REDLES - v.{version} ] - LOGIN INCORRECTO."
        )
