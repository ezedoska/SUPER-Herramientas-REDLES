from procs.logger import logB, log
import pandas as pd
from dateutil import parser
from procs.db import engine


def Forzar_p3(ui):
    # Meto todas las variables de los cuadritos
    tipo = ui.FP3Tipo.currentText()
    form = ui.FP3Form.text()
    lote = ui.FP3Lote.text()
    ndoc = ui.FP3Dni.text()
    tipoDict = {"Persona": 1, "Asociado": 3, "Integrante": 5}
    userdni = ui.loginUsrBox.text()
    if form in ["", "0"]:
        return logB(ui, f"El campo FORMULARIO no peude estar vacio.", 3)
    if lote in ["", "0"]:
        return logB(ui, f"El campo LOTE no peude estar vacio.", 3)
    if ndoc in ["", "0"]:
        return logB(ui, f"El campo NRODOCUMENTO no peude estar vacio.", 3)
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""EXEC [SQLemore].[forzar_p3] 
                    @tipo={tipoDict[tipo]},
                    @form={form},
                    @lote={lote},
                    @ndoc={ndoc}"""
            )
            log(ui, form)
            return logB(ui, f"[{form}] Se cargo exitosamente el P3", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
