from procs.logger import logB,log
import pandas as pd
from dateutil import parser

def go(engine,ui):
    # Meto todas las variables de los cuadritos
    reso = ui.asigReReso.text()
    exp = ui.asigReExp.text()
    depReso = ui.asigReDependenciaR.currentText()
    depExp = ui.asigReDependenciaE.currentText()
    gestion = ui.asigReGestion.currentText()
    fechaReso = ui.asigReFecha.date().toPyDate()
    anioreso = fechaReso.strftime('%y')
    fechaReso = fechaReso.strftime('%Y-%m-%d 00:00:00')
    operador=32737943
    # operador = ui.loginUsrBox.text()
    gestionDict = {'ALTA':1,'RENUNCIA':2,'DENEGATORIA':3,'BAJA DE OFICIO':7}

    if reso in ['','0'] : return logB(ui,"CargarADH",f"El campo RESOLUCION no peude estar vacio.",3)
    if exp in ['','0'] or len(exp)<11 : return logB(ui,"CargarADH",f"Campo EXPEDIENTE son al menos 12 digitos.",3)

    resoexp = reso + ' ' + exp
    try:
        # Chekeo que el expediente exista.
        checkExp = pd.read_sql_query(f"""SELECT NroExpediente 
                                         FROM ExpedientesGde 
                                         WHERE NroExpediente={exp}""",
                                         con=engine)
        if checkExp.empty: return logB(ui,"Asignar Resolucion",f"[{exp}] El expediente no existe.",2)

        # Checkeo q no tenga otra reso asignada.
        checkReso = pd.read_sql_query(f"""SELECT NroExpediente,NroResolucion 
                                          FROM ResolucionExpedientesGDE 
                                          WHERE NroExpediente={exp}""",
                                          con=engine)
        if checkReso.empty==False: return logB(
            ui,"Asignar Resolucion",f"[{exp}] tiene otra reso asignada : {checkReso['NroResolucion'].iloc[0]}.",2)
    except Exception as e:
        return logB(ui,"Asignar Resolucion",f"Hubo un error: {str(e)}",3) 
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""EXEC AsignarResoEXE 
                    @reso={reso}{anioreso},
                    @exp={exp},
                    @fechareso='{fechaReso}',
                    @dependenciareso={depReso},
                    @dependenciaexp={depExp},
                    @gestion={gestionDict[gestion]},
                    @operador={operador}"""
            )
            log(engine,ui,'Asignacion RESO', resoexp)
            return logB(ui,"Asignar Resolucion",f"[{resoexp}] Se asigno exitosamente",1) 
    except Exception as e:
        return logB(ui,"Asignar Resolucion",f"Hubo un error: {str(e)}",3) 
