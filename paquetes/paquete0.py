import os
import pandas as pd
from sqlalchemy import types
from datetime import datetime
import csv
from procs.logger import log, logB
from procs.db import engine


def Paquete_0_Proceso(ui):
    logB(ui, "Ejecutando store P0.")
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P0_02_2019")
    except Exception as e:
        return logB(ui, f"Error procesando el paquete: {str(e)}", 3, 0)
    return logB(ui, "Procesamiento del P0 completado.", 1, 0)


def Paquete_0_Salida(ui):
    logB(ui, "Ejecutando salida P0.")
    # Guardamos el formato para la fecha que se va usar para todo.
    fecha = datetime.today().strftime("%Y%m%d")
    # Buscamos el numero de paquete 0 para crear la carpeta.
    num0 = pd.read_sql_query(
        """SELECT [numero]  
           FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  
           WHERE paquete='p0-2019'""",
        con=engine,
    )
    nlote0 = str(num0.iloc[0]["numero"])

    # Preparamos la ruta para los archivos de salida.
    lote0 = "P:\\SINTyS\\Paquete_00\\Lote_" + nlote0 + "_" + fecha

    # Creamos la carpeta, si ya existian avisa y sigue.
    try:
        os.mkdir(f"{lote0}")
        logB(ui, f"Se creo la carpeta {lote0}.", 1, 0)
    except:
        logB(ui, "La carpeta del P0 este lote ya existia.", 2, 0)

    # Leemos la tabla de SALIDA P0 y lo guardamos en un dataframe.
    logB(ui, "Leyendo tabla DTS_SalidaPaquete00_2019.", 0, 0)
    df0 = pd.read_sql_table("DTS_SalidaPaquete00_2019", con=engine, schema="dbo")
    df0.dropna(inplace=True)
    logB(ui, "Hecho.", 1, 0)

    # Leemos la tabla de ERRORES P0 y lo guardamos en un dataframe.
    logB(ui, "Leyendo tabla DTS_ErroresPaquete00_2019.", 0, 0)
    df0e = pd.read_sql_table("DTS_ErroresPaquete00_2019", con=engine, schema="dbo")
    logB(ui, "Hecho.", 1, 0)

    # Comenzamos la creacion los archivos de SALIDA del P0.
    try:
        # marcamos el limite de lineas por archivo.
        size = 499

        # Separamos en partes el DF y los ponemos en una lista.
        list_of_dfs = [df0.loc[i : i + size - 1, :] for i in range(0, len(df0), size)]

        # Tomamos el numero de archivos que se crearon para poder armar el nombre del archivo.
        Nfiles = len(list_of_dfs)

        # Inicicalizamos la variable en 1 para enumerar los archivos.
        begin = 1

        # Por cada DF en la lista se llevan a cabo los siguientes pasos
        for file in list_of_dfs:
            # Contamos los rows del DF.
            rows = file.shape[0]

            # Creamos la direccion de destino del TXT.
            path = f"{lote0}\\F01252.cuit.30707046399.fecha.{fecha}.nro.00{begin}de00{Nfiles}.txt"

            # Armamos la cabecera.
            zerosC = "0" * (
                5 - len(str(rows))
            )  # Para saber cuantos zeros van antes del numero.
            # CABECERA 1.0
            file.columns = [f"0130707046399125200100{nlote0}{zerosC}{rows+1}"]
            # CABECERA 2.0
            # file.columns = [f"01307070463991252002000{nlote0}{fecha}{zerosC}{rows+1}"]

            try:
                # Lo convertimos en txt,
                file.to_csv(
                    path,
                    header=True,
                    index=None,
                    sep="|",
                    encoding="ansi",
                    line_terminator="",
                    quoting=csv.QUOTE_NONE,
                    escapechar='"',
                )
                logB(ui, f"{begin} de {Nfiles} hecho.", 1, 0)
            except Exception as e:
                logB(
                    ui,
                    f"{begin} de {Nfiles} no se pudo generar."
                    + f" revisar salida:\n{str(e)}",
                    3,
                    0,
                )
                begin = begin + 1
                continue
            try:
                with open(path) as f:
                    lines = f.readlines()
                    last = len(lines) - 1
                    lines[last] = lines[last].replace("\r", "").replace("\n", "")
                with open(path, "w") as wr:
                    wr.writelines(lines)
                begin = begin + 1
            except Exception as e:
                logB(
                    ui,
                    f"{begin} de {Nfiles} generado con errores."
                    + f" revisar salida:\n{str(e)}",
                    3,
                    0,
                )
                continue
        logB(ui, f"Lote 0 n°{nlote0} generado en {lote0}.", 1, 0)

        # Creamos el archivo de LOTE del P0.
        df0.to_csv(
            f"{lote0}\\Paquete_0_Lote{nlote0}.txt",
            header=False,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
        logB(ui, "Paquete 0 generado con exito.", 1, 0)
    except Exception as e:
        logB(ui, f"Hubo un error creando los txt del p0:\n{str(e)}", 3, 0)
        pass

    # Creamos el archivo de errores del P0
    try:
        df0e.to_csv(
            f"{lote0}\\No-enviados-paquete-0-lote{nlote0}.txt",
            header=True,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
        logB(ui, "ERRORES PAQUETE 0 generado con exito.", 1, 0)
    except Exception as e:
        logB(ui, f"Hubo un error creando los txt de error del p0:\n{str(e)}", 2, 0)
    return 0
