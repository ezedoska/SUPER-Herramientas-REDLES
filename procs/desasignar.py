from procs.logger import logB, log
from procs.db import engine


def Desasignado(ui):
    tipoForm = ui.desaTipoForm.currentText()
    form = ui.desaForm.text()
    tipoExp = ui.desaTipoExp.currentText()
    exp = ui.desaExp.text()
    efDict = {
        "Persona": 1,
        "Cooperativa": 2,
        "Asociado": 3,
        "Proyecto": 4,
        "Integrante": 5,
    }
    expDict = {
        "GDE": 1,
        "SISEX": 2,
    }
    # Validamos los casilleros
    if form in ["", "0"]:
        return logB(ui, f"El campo FORMULARIO no peude estar vacio.", 3)
    if exp in ["", "0"] or len(exp) < 11:
        return logB(ui, f"Campo EXPEDIENTE son al menos 12 digitos.", 3)
    # Ejecutamos el store
    try:
        with engine.begin() as connection:
            connection.execute(
                f"""EXEC [SQLemore].[SHR_Desasignar]   
                @form={form},
                @tipoform={efDict[tipoForm]},
                @exp={exp},
                @tipoexp={expDict[tipoExp]}"""
            )
    except Exception as e:
        return logB(ui, f"Error desasignando: {str(e)}", 3, 0)
    # logueamos y terminamos
    log(ui)
    return logB(ui, f"Se desasigno correctamente E:{exp} del F:{form}.", 1, 0)
