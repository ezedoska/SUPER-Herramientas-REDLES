import pandas as pd
from procs.logger import log,logB
def go(engine,ui):
    tipoEf = ui.E9Tipo.currentText()
    form = ui.E9Form.text()
    if form in ['','0'] : return logB(ui,"Error 9",f"El campo formulario no peude estar vacio.",3)
    userdni = ui.loginUsrBox.text()
    try:
        checkE9  = pd.read_sql_query(
            f"""SELECT id_{tipoEf} 
                FROM {tipoEf}s_paquete_4 
                WHERE id_{tipoEf}={form} and cod_error=9""",
            con=engine
        )
        if checkE9.empty:
            return logB(ui,"Error 9",f"[{form}] El formulario no tiene error 9.",2)
        else:
            with engine.begin() as connection:
                try:
                    connection.execute(
                        f"""INSERT 
                            INTO Paquete_4_error9_Log (TipoEf, NroFormulario, Fecha, Usuario) 
                            VALUES('{tipoEf}',{form},getdate(),{userdni})""")
                except Exception as e:
                    return logB(ui,"Error 9",f"[{form}] Ocurrio un error insertando el log: {str(e)}",3)
                try:
                    connection.execute(f"""DELETE 
                                        FROM {tipoEf}s_paquete_4 
                                        WHERE id_{tipoEf}={form} and cod_error=9""")
                except Exception as e:
                    return logB(ui,"Error 9",f"[{form}] Ocurrio un error borrando el paquete 4: {str(e)}",3)
            log(engine,ui,'Borrado error 9', form)
            return logB(ui,"Error 9",f"[{form}] El error fue borrado.",1)
    except Exception as e:
        return logB(ui,"Error 9",f"[{form}] Ocurrio un error chequeando el estado: {str(e)}",3)