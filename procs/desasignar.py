from procs.logger import logB, log
from procs.db import engine


def Desasignado(ui):
    tipoForm = ui.desaTipoForm.currentText()
    form = ui.desaForm.text()
    tipoExp = ui.desaTipoExp.currentText()
    exp = ui.desaExp.text()
    teDict = {"Persona": 1, "Asociado": 3, "Integrante": 5}

    if form in ["", "0"]:
        return logB(ui, f"El campo FORMULARIO no peude estar vacio.", 3)
    if exp in ["", "0"] or len(exp) < 11:
        return logB(ui, f"Campo EXPEDIENTE son al menos 12 digitos.", 3)

    delete1 = f"""DELETE 
                  FROM {tipoForm}sExp{tipoExp}
                  WHERE id_{tipoForm} = {form} and nroExpediente= {exp} """
    delete2 = f"""SELECT 
                  FROM cajasArchivo
                  WHERE nroRedles = {form} 
                  and nroExpediente= {exp} 
                  and tipoRedles={teDict[tipoForm]}"""
    try:
        with engine.begin() as connection:
            result1 = connection.execute(delete1)
        if result1.rowcount == 0:
            return logB(ui, f"No se encontro formulario con ese expediente.", 2)
        logB(ui, f"Expediente desasignado.", 1)

        with engine.begin() as connection:
            result2 = connection.execute(delete2)
        if result2.rowcount == 0:
            return logB(
                ui, f"No se encontro caja con ese form/expediente, verificar.", 2, 0
            )
        logB(ui, f"Caja desasignada.", 1, 0)
        log(ui)
        return logB(ui, f"Se desasigno correctamente E:{exp} del F:{exp}.", 1, 0)
    except Exception as e:
        return logB(ui, f"Error desasignando el formulario: {str(e)}", 3)