import pandas as pd
from procs.logger import log, logB
from procs.db import engine


def Error_9(ui):
    tipo = ui.E9Tipo.currentText()
    form = ui.E9Form.text()
    if form in ["", "0"]:
        return logB(ui, f"El campo FORMULARIO no peude estar vacio.", 3)
    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943
    try:
        checkE9 = pd.read_sql_query(
            f"""SELECT id_{tipo} 
                FROM {tipo}s_paquete_4 
                WHERE id_{tipo}={form} and cod_error=9""",
            con=engine,
        )
        if checkE9.empty:
            return logB(ui, f"[{form}] El formulario no tiene error 9.", 2)
        else:
            with engine.begin() as connection:
                try:
                    connection.execute(
                        f"""INSERT 
                            INTO Paquete_4_error9_Log (TipoEf, NroFormulario, Fecha, Usuario) 
                            VALUES('{tipo}',{form},getdate(),{userdni})"""
                    )
                except Exception as e:
                    return logB(
                        ui,
                        f"[{form}] Error insertando el log: {str(e)}",
                        3,
                    )
                try:
                    connection.execute(
                        f"""DELETE 
                            FROM {tipo}s_paquete_4 
                            WHERE id_{tipo}={form} and cod_error=9"""
                    )
                except Exception as e:
                    return logB(
                        ui,
                        f"[{form}] Ocurrio un error borrando el paquete 4: {str(e)}",
                        3,
                    )
            log(ui, form)
            return logB(ui, f"[{form}] El error fue borrado.", 1)
    except Exception as e:
        return logB(
            ui,
            f"[{form}] Ocurrio un error chequeando el estado: {str(e)}",
            3,
        )
