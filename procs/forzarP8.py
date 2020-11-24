import pandas as pd
from procs.logger import log,logB

def go(engine, ui):
    """
    [Forzar_P8]
    
    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]
    """
    form = ui.fp8Form.text()
    tipo = ui.fp8Tipo.currentText()
    if form in ['','0'] : return logB(ui,"Forzar P8","El campo formulario no peude estar vacio.",3)

    try:
        with engine.begin() as connection:
            connection.execute(
                f"""
                    declare @lote int
                    set @lote = (select max(lote) from [{tipo}s_Paquete_8] where tmov='B')
                    INSERT INTO [adm_efectores].[dbo].[{tipo}s_Paquete_8]
                        ([NroREDLES]
                        ,[fecha]
                        ,[Lote]
                        ,[Tmov])
                    VALUES
                        ({form}
                        ,getdate()
                        ,@lote
                        ,'B')
                """
            )
        return logB(ui,"Forzar P8","Se inserto el P8.",1)
    except Exception as e:
        return logB(ui,"Forzar P8",f"Hubo un error: {str(e)}",3)
