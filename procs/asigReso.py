from procs.logger import logB, log
import pandas as pd
from dateutil import parser
from procs.db import engine


def Asignar_Resolucion(ui):
    # Meto todas las variables de los cuadritos
    reso = ui.asigReReso.text()
    exp = ui.asigReExp.text()
    depReso = ui.asigReDependenciaR.currentText()
    depExp = ui.asigReDependenciaE.currentText()
    gestion = ui.asigReGestion.currentText()
    fechaReso = ui.asigReFecha.date().toPyDate()
    anioreso = fechaReso.strftime("%y")
    fechaReso = fechaReso.strftime("%Y-%m-%d 00:00:00")

    userdni = ui.loginUsrBox.text()
    if userdni == "":
        userdni = 32737943

    gestionDict = {"ALTA": 1, "RENUNCIA": 2, "DENEGATORIA": 3, "BAJA DE OFICIO": 7}

    if reso in ["", "0"]:
        return logB(ui, f"El campo RESOLUCION no peude estar vacio.", 3)
    if exp in ["", "0"] or len(exp) < 11:
        return logB(ui, f"Campo EXPEDIENTE son al menos 12 digitos.", 3)

    resoexp = reso + " " + exp
    try:
        # Chekeo que el expediente exista.
        checkExp = pd.read_sql_query(
            f"""SELECT NroExpediente 
                                         FROM ExpedientesGde 
                                         WHERE NroExpediente={exp}""",
            con=engine,
        )
        if checkExp.empty:
            return logB(ui, f"[{exp}] El expediente no existe.", 2)

        # Checkeo q no tenga otra reso asignada.
        checkReso = pd.read_sql_query(
            f"""SELECT NroExpediente,NroResolucion 
                                          FROM ResolucionExpedientesGDE 
                                          WHERE NroExpediente={exp}""",
            con=engine,
        )
        if checkReso.empty == False:
            return logB(
                ui,
                f"[{exp}] tiene otra reso asignada : {checkReso['NroResolucion'].iloc[0]}.",
                2,
            )
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""EXEC [SQLemore].[SHR_AsignarResoEXE]   
                    @reso={reso}{anioreso},
                    @exp={exp},
                    @fechareso='{fechaReso}',
                    @dependenciareso={depReso},
                    @dependenciaexp={depExp},
                    @gestion={gestionDict[gestion]},
                    @operador={userdni}"""
            )
            log(ui, resoexp)
            return logB(ui, f"[{resoexp}] Se asigno exitosamente", 1)
    except Exception as e:
        return logB(ui, f"Hubo un error: {str(e)}", 3)
