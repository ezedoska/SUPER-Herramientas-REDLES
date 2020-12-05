import glob
import os
import re
import shutil
import pandas as pd
from sqlalchemy import types
from procs.logger import log, logB
from procs.db import engine
from zipfile import ZipFile
import io


def Paquete_15(ui):
    """
    [PROCESA EL P15 Y GUARDA LOS ARCHIVOS EN SUS CARPETAS]

    Arguments:
        conn {[sqlalchemy]} -- [conneccion de sqlalchemy]
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]

    Returns:
        [0] -- [Salida al menu]
    """
    logB(ui, "Procesando Paquete 15", 0, 1)
    logB(ui, "Buscando paquetes...", 0, 0)
    paquete = glob.glob("*adh*")

    if len(paquete) == 2:
        try:
            zip0 = ZipFile(paquete[0], "r")
            zip1 = ZipFile(paquete[1], "r")
        except:
            return logB(ui, "Hubo un problema leyendo los paquetes.", 3, 0)

        file0 = [name for name in zip0.namelist() if name.endswith(".txt")]
        txt0 = str(zip0.read(file0[0]), "UTF-8")

        file1 = [name for name in zip1.namelist() if name.endswith(".txt")]
        txt1 = str(zip1.read(file1[0]), "UTF-8")
        logB(ui, "Uniendo paquetes...", 0, 0)
        txtF = txt0 + txt1
        df = pd.read_csv(
            io.StringIO(txtF), names=["text"], engine="python", index_col=None
        )
        zip0.close()
        zip1.close()
    elif len(paquete) == 1:
        try:
            zip0 = ZipFile(paquete[0], "r")
        except:
            return logB(ui, "Hubo un problema leyendo el paquete.", 3, 0)

        file0 = [name for name in zip0.namelist() if name.endswith(".txt")]
        txt0 = str(zip0.read(file0[0]), "UTF-8")

        txtF = txt0
        df = pd.read_csv(
            io.StringIO(txtF), names=["text"], engine="python", index_col=None
        )
        zip0.close()
    else:
        return logB(ui, "No se encontro ningun paquete.", 3, 0)

    logB(ui, "Subiendo a la tabla...", 0, 0)
    try:

        with engine.begin() as connection:
            connection.execute("DELETE FROM DTS_EntradaPaquete15_2019")
            df.to_sql(
                "DTS_EntradaPaquete15_2019",
                con=engine,
                if_exists="append",
                index=False,
                schema="dbo",
                dtype={"text": types.VARCHAR(length=252)},
            )
    except Exception as e:
        return logB(ui, f"hubo un error subiendo el paquete:\n{str(e)}", 3, 0)

    logB(ui, "Subida sin errores.", 1, 0)

    # Ejecutamos el proceso de p5 con SQLACHEMY.

    logB(ui, "Ejecutando store P15.", 0, 0)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P15_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)
    logB(ui, "Procesamiento del P15 completado.", 1, 0)

    # Buscamos el numero de paquete 14 para crear la carpeta.
    num = pd.read_sql_query(
        "SELECT [numero]  FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  where paquete='p14'",
        con=engine,
    )

    lote = "P:\\AFIP\\Paquete_15\\Lote_" + str(num.iloc[0]["numero"])

    # Creamos la carpeta, si ya existia avisa y sigue.
    try:
        os.mkdir(f"{lote}")
    except:
        logB(ui, "La carpeta de este lote ya existia.", 2, 0)

    # Muevo el paquete a la locacion.
    try:
        shutil.move(paquete[0], f"{lote}\\{paquete[0]}")
        if len(paquete) == 2:
            shutil.move(paquete[1], f"{lote}\\{paquete[1]}")
    except:
        logB(ui, "Hubo un problema moviendo los archivos.", 2, 0)

    # Aviso donde se movio el archivo.
    logB(ui, f"Lote guardado en {lote}", 1, 0)

    # Leemos la tabla de errores y lo guardamos en un dataframe.
    errores = pd.read_sql_table("DTS_ErroresPaquete15_2019", con=engine, schema="dbo")

    # Volcamos el dataframe a un txt.
    errores.to_csv(
        f"{lote}\\errores.txt",
        header=True,
        index=None,
        mode="a",
        sep=" ",
    )
    logB(ui, "Errores guardados.", 1, 0)

    return 0
