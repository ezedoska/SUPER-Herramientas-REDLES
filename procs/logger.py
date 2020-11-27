from procs.memes import redlestips
import random
import inspect
import types
from typing import cast
from procs.db import engine


def log(ui, formusado=""):
    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943
    procname = inspect.stack()[1][3]
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""INSERT INTO [adm_efectores].[SQLemore].[ExeStats] 
                                    (funcion,fecha,usuario, formusado) 
                                    VALUES ('{procname}',getdate(),'{userdni}','{formusado}')"""
            )
    except Exception as e:
        return logB(ui, f"Ocurrio un error logeando a la DB: {str(e)}", 3)
    ui.quoteLabel.setText(random.choice(redlestips))
    return 0


def logB(ui, mensaje, tipo=0, size=4):
    if tipo == 1:
        icono = "✔"
    elif tipo == 2:
        icono = "✘"
    elif tipo == 3:
        icono = "⚠"
    else:
        icono = ""
    procname = inspect.stack()[1][3]
    ui.log.append(f"<h{size}>{icono} {procname}:</h{size}>  {mensaje}")
    return 0