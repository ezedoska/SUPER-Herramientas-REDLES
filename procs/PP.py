from procs.logger import logB, log
import pandas as pd
from dateutil import parser
from procs.db import engine


def Anexo(ui):
    try:
        df = pd.read_excel("anexo_PP.xlsx", engine='openpyxl')
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)

    if df.empty:
        return logB(ui, "El excel esta vacio", 2)

    try:
        df.to_sql("Proyectos11_anexo_2020",
                  con=engine,
                  if_exists="append",
                  index=False,
                  schema="dbo")
        return logB(ui, f"El PP se cargo correctamente.", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)


def Int(ui):

    try:
        df = pd.read_excel("IPP.xlsx", engine='openpyxl')
        if df.empty:
            return logB(ui, "El excel esta vacio", 2)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
    try:
        df.to_sql("ProyectosIntegrantes",
                  con=engine,
                  if_exists="append",
                  index=False,
                  schema="dbo")
        return logB(ui, f"El IPP se cargo correctamente.", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)


def AsigPP(ui):
    form = ui.PPForm.text()
    exp = ui.PPExp.text()
    caja = ui.PPCaja.text()
    dep = ui.PPDepExp.currentText()
    try:
        with engine.begin() as connection:
            connection.execute(f"""exec [dbo].[asignarexpPP] 
                @form={form},
                @exp={exp},
                @caja={caja},
                @dep='{dep}'""")
        return logB(ui, f"El PP se asigno correctamente.", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
