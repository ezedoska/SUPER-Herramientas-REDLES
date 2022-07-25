from procs.logger import logB, log
import pandas as pd
from dateutil import parser
from procs.db import engine


def Anexo(ui):
    try:
        df1 = pd.read_excel("anexo_PP.xlsx", engine="openpyxl", dtype=str)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)

    # borramos las rows vacias
    df = df1.dropna(
        how="any",
        axis=0,
        subset=[
            "nroformulario",
            "referente",
            "Codigo_Postal_fiscal",
            "Codigo_Postal_legal",
            "domfiscal_domlegal",
            "Tipo_mail",
            "tipo_telefono",
            "tipo_linea",
            "cod_area",
            "tel_PP",
            "compania_tel",
        ],
    )

    if df.empty:
        return logB(
            ui,
            "El excel esta vacio, puede ocurrir que se esten borrando lineas por contener errores, revisar documento",
            2,
        )

    try:
        df.to_sql(
            "Proyectos11_anexo_2020",
            con=engine,
            if_exists="append",
            index=False,
            schema="dbo",
        )
        return logB(ui, f"El PP se cargo correctamente.", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)


def Int(ui):

    try:
        df1 = pd.read_excel("IPP.xlsx", engine="openpyxl", dtype=str)
        df = df1.dropna(
            how="any",
            axis=0,
            subset=[
                "apellidos",
                "nombres",
                "tipo_doc",
                "nrodocumento",
                "cuit",
                "id_proyecto",
                "categoria",
                "nroformulario",
                "fecha_carga",
                "operador",
            ],
        )

        if df.empty:
            return logB(
                ui,
                "El excel esta vacio, puede ocurrir que se esten borrando lineas por contener errores, revisar documento",
                2,
            )
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
    try:
        df.to_sql(
            "ProyectosIntegrantes",
            con=engine,
            if_exists="append",
            index=False,
            schema="dbo",
        )
        return logB(ui, f"El IPP se cargo correctamente.", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
