import glob
import os
import re
import shutil
import pandas as pd
from datetime import datetime
from sqlalchemy import types
from procs.logger import log, logB
from procs.db import engine


def Paquete_1(ui):

    # Buscamos el archivo de paquete
    logB(ui, "Buscando paquetes...")
    paquete = glob.glob("*AFIP_MDS_F01252.cuit.30707046399*")

    # Borramos la tabla de subida
    logB(ui, "Limpiando tabla destino P1.", 0, 0)
    with engine.begin() as connection:
        connection.execute("DELETE FROM DTS_EntradaPaquete01_2019")
    logB(ui, "Hecho.", 1, 0)

    # Subiendo el P1
    logB(ui, "Subiendo P1.", 0, 0)
    for txt in paquete:
        logB(ui, f"Encontrado...'{txt}'...leyendo.", 0, 0)
        df = pd.read_csv(txt, names=["text"])
        df.to_sql(
            "DTS_EntradaPaquete01_2019",
            con=engine,
            if_exists="append",
            index=False,
            schema="dbo",
            dtype={"text": types.VARCHAR(length=252)},
        )
        logB(ui, "Hecho.", 1, 0)

    # Ejecutamos el proceso de p1 con SQLACHEMY.
    logB(ui, "Ejecutando store P1.", 0, 0)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P1_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)
    logB(ui, "Procesamiento del P1 completado.", 1, 0)

    # Buscamos el numero de paquete 1 para crear la carpeta.
    num = pd.read_sql_query(
        """SELECT [numero]  
           FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  
           WHERE paquete='p1-2019'""",
        con=engine,
    )
    nlote = str(num.iloc[0]["numero"])

    # Guardamos el formato para la fecha.
    fecha = datetime.today().strftime("%Y%m%d")

    # Creamos los paths
    lote = "P:\\AFIP\\Paquete_01\\Lote_5" + nlote + "_" + fecha

    # Creamos la carpeta, si ya existia avisa y sigue.
    try:
        os.mkdir(f"{lote}")
    except:
        logB(ui, "La carpeta de este lote ya existia.", 2, 0)

    # Muevo los paquetes a la locacion.
    try:
        for file in paquete:
            shutil.move(file, f"{lote}\\{file}")
            logB(ui, f"{file} guardado con exito en {lote}", 1, 0)
    except Exception as e:
        logB(ui, f"Hubo un problema moviendo los archivos:\n{str(e)}", 2, 0)

    # Aviso donde se movio el archivo.
    return logB(ui, f"Lote {nlote} procesado exitosamente", 1, 0)
