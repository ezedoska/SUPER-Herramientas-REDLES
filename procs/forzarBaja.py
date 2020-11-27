import pandas as pd
from procs.logger import log, logB
from procs.db import engine


def Forzar_Baja(ui):
    """
    [Reenviar P0]

    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]
    """
    form = ui.fbajaForm.text()
    tipo = ui.fbajaTipo.currentText()
    tipoDict = {
        "persona": "personasfisicas",
        "asociado": "asociados",
        "integrante": "integrantes",
    }
    if form in ["", "0"]:
        return logB(ui, "El campo FORMULARIO no peude estar vacio.", 3)
    try:
        check = pd.read_sql_query(
            f"""SELECT * 
                FROM [adm_efectores].[dbo].[bajas{tipoDict[tipo]}] 
                WHERE form_{tipo}={form}""",
            con=engine,
        )

        if check.empty:
            try:
                with engine.begin() as connection:
                    connection.execute(
                        f"""INSERT INTO [adm_efectores].[dbo].[bajas{tipoDict[tipo]}]
                                    ([form_{tipo}]
                                    ,[denegatoria]
                                    ,[fecha_denegatoria]
                                    ,[motivo_baja]
                                    ,[fecha_baja]
                                    ,[operador]
                                    ,[detallebaja]
                                    ,[idMotivoRenuncia])
                                VALUES
                                    ({form}
                                    ,null
                                    ,null
                                    ,2
                                    ,getdate()
                                    ,32737943
                                    ,'renuncia'
                                    ,2)
                        """
                    )
                return logB(ui, f"[{form}] Baja insertada con exito", 1)
            except Exception as e:
                return logB(
                    ui,
                    "Forzar Baja",
                    f"[{form}] Hubo un error en la insercion de la baja : {str(e)}",
                    3,
                )
        else:
            return logB(ui, f"[{form}] Ya tiene una baja.", 2)
    except Exception as e:
        return logB(ui, f"[{form}] Error chequeando estado.", 3)
