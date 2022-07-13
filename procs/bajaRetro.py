import pandas as pd
from procs.logger import log, logB
from procs.db import engine


def Baja_Retro(ui):
    """
    [Reenviar P0]

    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]
    """
    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943
    form = ui.fbajaForm.text()
    tipo = ui.fbajaTipo.currentText()
    fecha = ui.fbajaFecha.date().toPyDate()
    fechaBaja = fecha.strftime("%Y-%d-%m 00:00:00")
    tipoDict = {
        "Persona": 1,
        "Asociado": 2,
        "Integrante": 3,
    }

    if form in ["", "0"]:
        return logB(ui, "El campo FORMULARIO no peude estar vacio.", 3)

    # usamos el store de bajas retro
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""EXEC [dbo].[HacerBajaRetro]
                        @Formulario = {form},
                        @TipoEfector = {tipoDict[tipo]},
                        @Motivo = 2,
                        @DetalleMotivo = N'Baja Retroactiva',
                        @ope = {userdni},
                        @fecha = '{fechaBaja}'
                    """
            )
        log(ui, form)
        return logB(
            ui, f"[{form}] Baja insertada con exito para la fecha {fechaBaja}", 1
        )
    except Exception as e:
        return logB(
            ui,
            f"[{form}] Hubo un error en store de baja retro : {str(e)}",
            3,
        )
