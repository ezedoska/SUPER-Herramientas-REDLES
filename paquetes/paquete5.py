import glob
import os
import re
import shutil
import pandas as pd
from sqlalchemy import types
from procs.logger import log, logB
from procs.db import engine


def Paquete_5(ui):
    logB(ui, "Buscando paquete")
    paquete = glob.glob("*Cuitificacion*")

    # Si lo encuentra lo guarda en un daataframe
    if paquete and len(paquete) == 1:
        logB(ui, f"Encontrado...'{paquete[0]}'...leyendo.", 1, 0)
        df = pd.read_csv(paquete[0], names=["text"])
    else:
        # Si no hay nada, termina el proceso, lo mismo si encuentra mas de un paquete.
        return logB(
            ui,
            """
            No se proceso por una de dos razones:\n
            1- No habia archivo para procesar\n
            2- Habia mas de un archivo para procesar\n
        """,
            3,
            0,
        )

    logB(ui, "Listo.", 1, 0)

    logB(ui, "Subiendo el paquete a la DB.", 0, 0)
    try:
        with engine.begin() as connection:
            connection.execute("DELETE FROM DTS_EntradaPaquete05_2019")
            df.to_sql(
                "DTS_EntradaPaquete05_2019",
                con=engine,
                if_exists="append",
                index=False,
                schema="dbo",
                dtype={"text": types.VARCHAR(length=252)},
            )
    except Exception as e:
        return logB(ui, f"hubo un error subiendo el paquete:\n{str(e)}", 3, 0)

    # Si todo salio bien
    logB(ui, "El paquete subio sin errores.", 1, 0)

    # Ejecutamos el proceso de p5 con SQLACHEMY.
    logB(ui, "Ejecutando store p5.", 0, 0)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P5_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)
    logB(ui, "Procesamiento del p5 completado.", 1, 0)

    # Encontramos el numero de lote en el nombre del archivo para crear la carpeta.
    lote = "P:\\AFIP\\Paquete_05_2038\\Lote_" + re.findall(r"\d+", paquete[0])[0]

    # Creamos la carpeta, si ya existia avisa y sigue.
    try:
        os.mkdir(f"{lote}")
    except:
        logB(ui, "La carpeta de este lote ya existia.", 2, 0)

    # Muevo el paquete a la locacion.
    shutil.move(paquete[0], f"{lote}\\{paquete[0]}")

    # Aviso donde se movio el archivo.
    logB(ui, f"Lote guardado en {lote}", 1, 0)

    # Leemos la tabla de errores y lo guardamos en un dataframe.
    errores = pd.read_sql_table("DTS_ErroresPaquete05_2019", con=engine, schema="dbo")

    # Volcamos el dataframe a un txt.
    errores.to_csv(
        f"{lote}\\errores.txt",
        header=True,
        index=None,
        mode="a",
        sep=" ",
    )
    logB(ui, "Errores guardados.", 1, 0)

    # Terminamos.
    return 0
