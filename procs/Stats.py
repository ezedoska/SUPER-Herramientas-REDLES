from procs.logger import logB, log, MostrarEnTabla
import pandas as pd
from dateutil import parser
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
from rich import console
from procs.console import console


def get_stats(ui):
    ui.statsTable.setRowCount(0)
    stat = ui.statsBox.currentText()
    try:
        if stat == "Altas por año/mes":
            df = pd.read_sql_query(
                """
                    select 
                    datepart(year, fechap5) as Año,
                    datepart(month, fechap5) as Mes, 
                    count(cuit) as Altas 
                    from padronefectores 
                    where fechap5 is not null
                    group by 
                    datepart(year, fechap5),
                    datepart(month, fechap5) 
                    order by año,mes
                """,
                con=engine,
            )
        if stat == "Bajas por año/mes":
            df = pd.read_sql_query(
                """
                    select 
                    datepart(year, fechabaja) as Año,
                    datepart(month, fechabaja) as Mes, 
                    count(cuit) as Bajas 
                    from padronefectores 
                    where fechabaja is not null
                    group by 
                    datepart(year, fechabaja),
                    datepart(month, fechabaja) 
                    order by año,mes
                """,
                con=engine,
            )
        if stat == "Stats por provincia":
            with engine.begin() as connection:
                connection.execute(f"""exec gen_statsxprovincia""")
            df = pd.read_sql_query(
                """
                    SELECT *
                    FROM [adm_efectores].[SQLemore].[statsxprovincia]
                    """,
                con=engine,
            )
    except Exception as e:
        return logB(ui, f"Hubo un error al crear la tabla: {str(e)}", 3)
    return MostrarEnTabla(df, ui.statsTable)
