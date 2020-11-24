import pandas as pd
from procs.logger import log,logB

def go(engine,ui):
    form = ui.reevForm.text()
    tipo = ui.reevTipo.currentText()
    userdni = ui.loginUsrBox.text()
    tipoDict = {'Persona':1,'Asociado':3,'Integrante':5}
    if form in ['','0'] : return logB(ui,'Reevaluar','El campo formulario no puede estar vacio.',3)
    try:
        check = pd.read_sql_query(
            f"""SELECT evaluado 
                FROM [adm_efectores].[dbo].[PadronEfectores] 
                WHERE nroformulario={form} and tipoef={tipoDict[tipo]}"""
            ,con=engine
        )
        if check.empty:
            return logB(ui,'Reevaluar',f'[{form}] Formulario inexistente.',2)
        elif check['evaluado'].iloc[0] == 2:
            try:
                with engine.begin() as connection:
                    connection.execute(
                    f"""exec [dbo].[ReevaluarEXE] 
                        @tipo={tipoDict[tipo]},@formulario={form},@operador={userdni}"""
                )
            except Exception as e:
                return logB(ui,'Reevaluar',f'[{form}] Hubo un error al reevaluar: {str(e)}',3)
            log(engine,ui,'Reevaluacion', form)
            return logB(ui,'Reevaluar',f'[{form}] Fue evaluado a positivo.',1)
        else:
            return logB(ui,'Reevaluar',f'[{form}] No tiene evaluacion negativa.',2)
    except Exception as e:
        return logB(ui,'Reevaluar',f'[{form}] Hubo un error chequeando estado: {str(e)}',3)

def undo(engine,ui):
    form = ui.reevForm.text()
    tipo = ui.reevTipo.currentText()
    tipoDict = {'Persona':1,'Asociado':3,'Integrante':5}
    userdni = ui.loginUsrBox.text()
    if form in ['','0'] : return logB(ui,'Deshacer Reevaluar','El campo formulario no peude estar vacio.',3)

    try:
        check = pd.read_sql_query(
            f"""SELECT nroredles 
                FROM [adm_efectores].[dbo].[Reevaluados] 
                WHERE nroredles={form} and tiporedles={tipoDict[tipo]}""",
            con=engine
        )
        if check.empty:
            return logB(ui,'Deshacer Reevaluar',f'[{form}] El formulario ingresado no tiene evaluacion a revertir.',2)
        else:
            try:
                with engine.begin() as connection:
                    connection.execute(
                        f"""exec [dbo].[UndoReevaluarEXE] 
                        @tipo={tipoDict[tipo]},@formulario={form},@operador={userdni}"""
                    )
            except Exception as e:
                return logB(ui,'Reevaluar',f'[{form}] Hubo un error reevaluando: {str(e)}',3)
            log(engine,ui,'undoReevaluacion', form)
            return logB(ui,'Deshacer Reevaluar',f'[{form}] Se revirtio la evaluacion.',1)
    except Exception as e:
        return logB(ui,'Deshacer Reevaluar',f'[{form}] Hubo un error chequeando estado: {str(e)}',3)
