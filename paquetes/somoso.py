import pandas as pd
import csv
from paquetes.DictsAndLists import dtypeDictCSV2, dtypeDictSQL2, namesList2
from csvvalidator import CSVValidator
from procs.logger import log, logB
from procs.db import engine


def Subir_Solicitudes(ui):
    """
    [SUBE LAS SOLICITUDES Y LAS POSICIONA PARA PROCESAR]

    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]

    Returns:
        [0] -- [Salida al menu]
    """

    validator = CSVValidator(namesList2)

    # Leemos las solicitudes y salteamos las rows con numero de columnas erroneas.
    try:
        df = pd.read_csv(
            "SOLICITUDES.txt",
            delimiter="|",
            encoding="ansi",
            error_bad_lines=True,
            warn_bad_lines=True,
            names=namesList2,
            dtype=dtypeDictCSV2,
        )

    except Exception as e:
        return logB(
            ui,
            f"No se pudo procesar el archivo SOLICITUDES.txt, FIJATE SI ESTA BIEN NOMBRADO.:\n{str(e)}",
            3,
            1,
        )

    df.loc[
        (df["IdPrograma"].isnull()) & (df["IdTipoSolicitud"].isin([1, 2])), "IdPrograma"
    ] = "5"
    df.loc[
        (df["Telefono"].isnull()) & (df["IdTipoSolicitud"].isin([1, 2])), "Telefono"
    ] = "99999999"
    # df = df.drop(df[(df['ADH_Edad'] > 21))
    validator.add_record_length_check("EX2", "unexpected record length")
    # Subimos el DF limpio a la tabla para procesar.
    logB(ui, "Subiendo Solicitudes.", 0, 1)
    try:
        df.to_sql(
            "DTS_Entrada_SOMOSO_01",
            con=engine,
            if_exists="replace",
            index=False,
            schema="dbo",
            dtype=dtypeDictSQL2,
        )
    except Exception as e:
        logB(ui, f"Hubo un error subiendo las solicitudes:\n{str(e)}", 3, 0)
    return 0


def Insertar_Solicitudes(ui):
    # Ejecutamos la entrada de datos a las tablas.
    logB(ui, "Ejecutando store Solicitudes...", 0, 1)
    try:
        with engine.begin() as connection:
            connection.execute("EXEC proc_INSERT_SOMOSO_04_v2")
    except Exception as e:
        return logB(ui, f"Hubo un error insertando las solicitudes:\n{str(e)}", 3, 0)

    logB(ui, "Solicitudes cargadas con exito.")

    # Guardamos los errores comparando las lines con :
    logB(ui, "Guardando errores.", 0, 0)
    RECOMMENDED = 97
    path = "Z:\\Solicitudes de inscripción MS-ANSES"
    try:
        with open("Solicitudes.txt") as csv_file:
            reader = csv.reader(csv_file, delimiter="|")
            for row in reader:
                if len(row) != RECOMMENDED:
                    with open(f"{path}\\error.txt", "a", encoding="ansi") as file:
                        file.writelines(f"{row}\n")
        logB(ui, "Errores guardados.", 1, 0)
    except Exception as e:
        logB(ui, f"Hubo un error guardando los errores:\n{str(e)}", 2, 0)

    return 0
