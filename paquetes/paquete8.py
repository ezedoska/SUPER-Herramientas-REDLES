import os
import shutil
import pandas as pd
from sqlalchemy import types
from procs.logger import log, logB
from procs.db import engine
from datetime import datetime


def Paquete_8(ui):
    """
    [PROCESA EL P8 Y ARMA LOS ARCHIVOS EN SUS CARPETAS]

    Arguments:
        conn {[sqlalchemy]} -- [conneccion de sqlalchemy]
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]

    Returns:
        [0] -- [Salida al menu]
    """
    logB(ui, f"Procesando Paquete 8", 0, 1)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P8_03_temp_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)
    logB(ui, "Procesamiento del p8 completado.", 1, 0)

    logB(ui, "Armando la salida.", 0, 0)
    # Buscamos el numero de paquete 8 para crear la carpeta.
    num = pd.read_sql_query(
        "SELECT [numero]  FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  where paquete='p8'",
        con=engine,
    )
    fecha = datetime.today().strftime("%Y%m%d")
    lote = (
        "P:\\AFIP\\Paquete_08\\EnvioPaquete8_Lote"
        + str(num.iloc[0]["numero"])
        + "_"
        + fecha
    )

    # Creamos la carpeta, si ya existia avisa y sigue.
    try:
        os.mkdir(f"{lote}")
    except:
        logB(ui, "La carpeta de este lote ya existia.", 2, 0)

    # Leemos la tabla de salida y lo guardamos en un dataframe.
    salida1 = pd.read_sql_table("DTS_SalidaPaquete08_2019", con=engine, schema="dbo")
    salida1.dropna(inplace=True)
    # Ordenamos el archivo de mayor a menor.
    salida1.sort_values(by=["text"])
    # Volcamos el dataframe a un txt.
    try:
        salida1.to_csv(
            f"{lote}\\F01258.cuit.30707046399.fecha.{fecha}.txt",
            header=False,
            index=None,
            encoding="ANSI",
            mode="a",
            sep=" ",
        )
        logB(ui, "Paquete 8 generado con exito.", 1, 0)
    except Exception as e:
        logB(
            ui,
            f"Error generando la salida:\n{str(e)}",
            3,
            0,
        )

    # Leemos la tabla de salida manual y lo guardamos en un dataframe.
    salida2 = pd.read_sql_table(
        "DTS_SalidaPaquete08_Manual_2019", con=engine, schema="dbo"
    )
    salida2.dropna(inplace=True)
    # Ordenamos el archivo de mayor a menor.
    # salida2.sort_values(by=['text'])
    # Volcamos el dataframe a un txt.
    try:
        salida2.to_csv(
            f"{lote}\\Paquete8_Lote{str(num.iloc[0]['numero'])}.txt",
            header=True,
            index=None,
            encoding="ANSI",
            mode="a",
            sep=";",
        )
        logB(ui, "Salida manual guardada.", 1, 0)
    except Exception as e:
        logB(
            ui,
            f"Error generando salida Manual:\n{str(e)}",
            3,
            0,
        )

    # Leemos la tabla de ERRORES y lo guardamos en un dataframe.
    errores = pd.read_sql_table("DTS_ErroresPaquete08_2019", con=engine, schema="dbo")

    # Volcamos el dataframe a un txt.
    try:
        errores.to_csv(
            f"{lote}\\errores.txt",
            header=True,
            index=None,
            encoding="ANSI",
            mode="a",
            sep=" ",
        )
        logB(ui, "Errores guardados.")
    except Exception as e:
        logB(ui, f"Hubo un error generando errores.txt:\n{str(e)},3,0")
    return 0
