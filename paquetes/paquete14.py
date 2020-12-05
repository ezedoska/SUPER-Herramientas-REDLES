import os
import shutil
import pandas as pd
from sqlalchemy import types
from procs.logger import log, logB
from procs.db import engine
from datetime import datetime


def Paquete_14(ui):
    """
    [PROCESA EL P14 Y ARMA LOS ARCHIVOS EN SUS CARPETAS]

    Arguments:
        conn {[sqlalchemy]} -- [conneccion de sqlalchemy]
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]

    Returns:
        [0] -- [Salida al menu]
    """
    logB(ui, "Procesando Paquete 14.", 0, 1)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P14_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)

    logB(ui, "Procesamiento del p14 completado.", 1, 0)

    # Buscamos el numero de paquete 14 para crear la carpeta.
    num = pd.read_sql_query(
        "SELECT [numero]  FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  where paquete='p14'",
        con=engine,
    )
    fecha = datetime.today().strftime("%Y%m%d")
    nlote = str(num.iloc[0]["numero"])
    lote = "P:\\AFIP\\Paquete_14_Abm_(adh)\\Lote_" + nlote + "_" + fecha

    # Creamos la carpeta, si ya existia avisa y sigue.
    try:
        os.mkdir(f"{lote}")
    except:
        logB(ui, "La carpeta de este lote ya existia.", 2, 0)

    # Leemos la tabla de salida y lo guardamos en un dataframe.
    salida = pd.read_sql_query(
        "select * from DTS_SalidaPaquete14_2019 order by text",
        con=engine,
    )
    salida.dropna(inplace=True)
    try:
        # Volcamos el dataframe a un txt.
        path = f"{lote}\\F01253.cuit.30707046399.fecha.{fecha}.txt"
        # Creamos la direccion de destino del TXT
        salida.to_csv(
            path,
            header=False,
            index=None,
            encoding="ansi",
            line_terminator="",
            quoting=3,
            quotechar="",
            escapechar="\\",
        )
    except Exception as e:
        logB(ui, f"Hubo un error generando los archivos:\n{str(e)}", 3, 0)
    try:
        with open(path) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace("\r", "").replace("\n", "")
        with open(path, "w") as wr:
            wr.writelines(lines)
        logB(ui, "Paquete 14 generado con exito.", 1, 0)
    except Exception as e:
        logB(
            ui,
            f"Paquete 14: generado con errores," + f" revisar archivo:\n{str(e)}",
            2,
            0,
        )

    return 0