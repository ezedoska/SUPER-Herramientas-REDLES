import os
import pandas as pd
from sqlalchemy import types
from datetime import datetime
import csv
from procs.logger import log, logB
from procs.db import engine


def Paquete_2_Proceso(ui):
    # PAQUETE 2.
    # Ejecutamos el proceso de p2 con SQLACHEMY.
    logB(ui, "Ejecutando store P2.")
    try:
        with engine.connect() as conn, conn.begin():
            conn.execute("EXEC proc_P2_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)
    return logB(ui, "Procesamiento del P2 completado.", 1, 0)


def Paquete_2_Salida(ui):
    # PAQUETE 2 SALIDA.
    # Guardamos el formato para la fecha que se va usar para todo.
    fecha = datetime.today().strftime("%Y%m%d")
    # Buscamos el numero de paquete 0 para crear la carpeta.
    num2 = pd.read_sql_query(
        """SELECT [numero]  
           FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  
           WHERE paquete='p2-2019'""",
        con=engine,
    )
    nlote2 = str(num2.iloc[0]["numero"])

    # Creamos el path.
    lote2 = "P:\\SINTyS\\Paquete_02\\Lote_" + nlote2 + "_" + fecha

    # Creamos las carpetas, si ya existian avisa y sigue.
    try:
        os.mkdir(f"{lote2}")
        logB(ui, f"Se creo la carpeta {lote2}.", 1, 0)
    except:
        logB(ui, "La carpeta del P2 este lote ya existia.", 2, 0)

    # Leemos la tabla de SALIDA P2 TITULARES y lo guardamos en un dataframe.
    logB(ui, "Leyendo tabla DTS_SalidaPaquete02_Titulares_2019.", 0, 0)
    df2t = pd.read_sql_table(
        "DTS_SalidaPaquete02_Titulares_2019", con=engine, schema="dbo"
    )
    logB(ui, "Hecho.", 1, 0)

    # Leemos la tabla de SALIDA P2 FAMILIARES y lo guardamos en un dataframe.
    logB(ui, "Leyendo tabla DTS_SalidaPaquete02_Familiares_2019.")
    df2f = pd.read_sql_table(
        "DTS_SalidaPaquete02_Familiares_2019", con=engine, schema="dbo"
    )
    logB(ui, "Hecho.", 1, 0)

    # Creamos los archivos de SALIDA del P2
    try:
        # titulares
        path2t = f"{lote2}\\Paquete2Lote{nlote2}.txt"
        df2t.to_csv(
            path2t,
            header=False,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
    except Exception as e:
        logB(ui, f"Hubo un error creando los txt del p2:\n{str(e)}", 3, 0)
        pass
    try:
        with open(path2t) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace("\r", "").replace("\n", "")
        with open(path2t, "w") as wr:
            wr.writelines(lines)
        logB(ui, "PAQUETE 2 TITULARES: generado con exito.", 1, 0)
    except Exception as e:
        logB(
            ui,
            "PAQUETE 2 TITULARES: generado con errores" + f" revisar salida:\n{str(e)}",
            2,
            0,
        )
        pass

    # familiares
    try:
        path2f = f"{lote2}\\Paquete2AnexoLote{nlote2}.txt"
        df2f.to_csv(
            path2f,
            header=False,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
    except Exception as e:
        logB(ui, f"Hubo un error creando los txt del p2:\n{str(e)}", 3, 0)
        pass
    try:
        with open(path2f) as f:
            lines = f.readlines()
            last = len(lines) - 1
            lines[last] = lines[last].replace("\r", "").replace("\n", "")
        with open(path2f, "w") as wr:
            wr.writelines(lines)
        logB(ui, "PAQUETE 2 FAMILIARES: generado con exito.", 1, 0)
    except Exception as e:
        logB(
            ui,
            "PAQUETE 2 FAMILIARES: generado con errores"
            + f" revisar salida:\n{str(e)}",
            2,
            0,
        )
        pass
    return 0
