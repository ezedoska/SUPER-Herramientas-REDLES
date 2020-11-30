import pandas as pd
import glob
import os
import shutil
import tarfile
from sqlalchemy import create_engine, exc
import csv
from paquetes.DictsAndLists import lista, listaTCA
from procs.logger import log, logB
from procs.db import engine


def Paquete_3_Subida(ui):
    # Buscamos archivos que terminen en GZ.
    logB(ui, "Buscando paquete...")
    paquete = glob.glob("*.gz")

    # Abrimos el GZ en python para manosearlo por dentro.
    if paquete and len(paquete) == 1:
        try:
            TarP3 = tarfile.open(paquete[0], "r:gz")
        except:
            return logB(ui, "Hubo un error leyendo el archivo de vuelta.", 3)

        logB(ui, f"Encontrado: {paquete[0]}", 1, 0)
    else:
        # Si no hay nada, termina el proceso, lo mismo si encuentra mas de un paquete.
        logB(
            ui,
            """
            No se proceso por una de dos razones:\n
            1- No habia archivo para procesar.\n
            2- Habia mas de un archivo para procesar.\n
        """,
            3,
            0,
        )
        input("\nPresione [ENTER] para volver al menu.")
        return 0
    logB(ui, "Listo.", 1, 0)

    # Buscamos los archivos dentro del GZ y los subimos a la DB.
    logB(ui, "Subiendo vuelta SyNTIS.")
    for file in lista:
        with engine.begin() as connection:
            connection.execute(f"DELETE FROM DTS_EntradaSintys_{file['Nombre']}_2019")
        try:
            filename = [name for name in TarP3.getnames() if file["Nombre"] in name]

            # En el caso de B00 hay chances de que venga un archivo VARIOS.B00, asi q lo filtramos.
            if file["Nombre"] == "B00":
                filename = [k for k in filename if not "VARIOS" in k]

            txt = TarP3.extractfile(filename[0])
            df = pd.read_csv(txt, sep="\t", encoding="ansi", dtype=file["dtype"])
            logB(ui, f"Subiendo {file['Nombre']}", 0, 0)
            df.to_sql(
                f"DTS_EntradaSintys_{file['Nombre']}_2019",
                con=engine,
                if_exists="append",
                index=False,
                schema="dbo",
            )
        except exc.SQLAlchemyError as e:
            TarP3.close()
            return logB(ui, f"Hubo un error procesando {file['Nombre']}:\n{str(e)}", 3)
        except IndexError:
            logB(ui, f"'\n{file['Nombre']} no esta en la vuelta.")
            continue
        # logB(ui, f"{file['Nombre']}...OK")
    with engine.begin() as connection:
        connection.execute(f"DELETE FROM DTS_EntradaSintys_TCA_2019")

    for file in listaTCA:
        try:
            filename = [name for name in TarP3.getnames() if file["Nombre"] in name]
            txt = TarP3.extractfile(filename[0])
            df = pd.read_csv(txt, sep="\t", encoding="ansi", dtype=file["dtype"])
            logB(ui, f"Subiendo {file['Nombre']}", 0, 0)

            df.insert(loc=0, column="tabla", value=file["Nombre"])
            df.to_sql(
                f"DTS_EntradaSintys_TCA_2019",
                con=engine,
                if_exists="append",
                index=False,
                schema="dbo",
            )
        except exc.SQLAlchemyError as e:
            TarP3.close()
            return logB(
                ui, f"Hubo un error procesando {file['Nombre']}:\n{str(e)}", 3, 0
            )
        except IndexError:
            logB(ui, f"\n{file['Nombre']} no esta en la vuelta.\n", 2, 0)
            continue

    # Cerramos el GZ para que no haya error al moverlo.
    TarP3.close()
    return logB(ui, "Subida Paquete 3 completada", 1, 0)


def Paquete_3_Entrada(ui):
    # Ejecutamos el proceso de p3 de entrada con SQLACHEMY.
    logB(ui, "Ejecutando store ENTRADA P3.")
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P3_02_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando la entrada:\n{str(e)}", 3, 0)

    return logB(ui, "Entrada del P3 completada.", 1, 0)


def Paquete_3_Proceso(ui):
    # Ejecutamos el proceso de p3 con SQLACHEMY.
    logB(ui, "Ejecutando store PROCESO P3.")
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_P3_03_2019")
    except Exception as e:
        return logB(ui, f"Hubo un error procesando el paquete:\n{str(e)}", 3, 0)

    logB(ui, "Procesamiento del P3 completado.", 1, 0)


def Paquete_3_Archivo(ui):
    logB(ui, "Archivando.")
    # Buscamos el numero de paquete 3 para crear la carpeta.
    num = pd.read_sql_query(
        "SELECT [numero]  FROM [adm_efectores].[dbo].[Numeracion_Paquetes]  where paquete='p3-2019'",
        con=engine,
    )
    nlote = str(num.iloc[0]["numero"])

    # Creamos el path.
    lote = "P:\\sintys\\Paquete_03\\Lote_" + nlote

    # Creamos las carpetas, si ya existian avisa y sigue.
    try:
        os.mkdir(f"{lote}")
        logB(ui, f"Se creo la carpeta {lote}.", 1, 0)
    except:
        logB(ui, "La carpeta del P3 este lote ya existia.", 2, 0)

    # Movemos los archivos de vuelta de SiNTYS.
    gz = glob.glob("*.gz")
    pgp = glob.glob("*.pgp")
    try:
        shutil.move(gz[0], f"{lote}\\{nlote}.tar.gz")
    except:
        logB(ui, "tar no encontrado", 2, 0)
        pass
    try:
        shutil.move(pgp[0], f"{lote}\\{nlote}.pgp")
    except:
        logB(ui, "pgp no encontrado", 2, 0)
        pass
    logB(ui, "Todos los archivos fueron archivados(lol).", 1, 0)
    # Creamos la salida con los errores SINTYS.
    try:
        errores1 = pd.read_sql_table(
            "DTS_ErroresSintys_B00_2019", con=engine, schema="dbo"
        )
        errores1.to_csv(
            f"{lote}\\{nlote}-errores-SINTYS.csv",
            header=True,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
    except:
        logB(ui, "Hubo un problema bajando el archivo de error.", 2, 0)
    # Creamos la salida con los errores.
    try:
        errores2 = pd.read_sql_table(
            "DTS_ErroresPaquete03_2019", con=engine, schema="dbo"
        )
        errores2.to_csv(
            f"{lote}\\{nlote}-errores.csv",
            header=True,
            index=None,
            sep="|",
            encoding="ansi",
            line_terminator="",
            quoting=csv.QUOTE_NONE,
            escapechar='"',
        )
    except:
        logB(ui, "Hubo un problema generando el archivo de error.", 2, 0)
    return logB(ui, "Proceos de archivo y generacion de errores terminado.", 1, 0)
