import pandas as pd
from procs.logger import log, logB
from procs.db import engine


def Forzar_P8(ui):
    """
    [Forzar_P8]

    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]
    """
    form = ui.fp8Form.text()
    tipo = ui.fp8Tipo.currentText()
    fecha = ui.fp8Fecha.date().toPyDate()
    fechaBaja = fecha.strftime("%Y-%d-%m 00:00:00")
    if form in ["", "0"]:
        return logB(ui, "El campo FORMULARIO no peude estar vacio.", 3)

    try:
        with engine.begin() as connection:
            connection.execute(f"""
                    declare @lote int
                    set @lote = (select max(lote) from [{tipo}s_Paquete_8] where tmov='B')
                    INSERT INTO [adm_efectores].[dbo].[{tipo}s_Paquete_8]
                        ([NroREDLES]
                        ,[fecha]
                        ,[Lote]
                        ,[Tmov])
                    VALUES
                        ({form}
                        ,'{fechaBaja}'
                        ,@lote
                        ,'B')
                """)
        return logB(ui, f"[{form}] Se inserto el P8.", 1)
    except Exception as e:
        return logB(ui, f"[{form}] Hubo un error: {str(e)}", 3)
