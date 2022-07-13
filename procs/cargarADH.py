from procs.logger import logB, log
from procs.db import engine


def Cargar_ADH(ui):
    """
    [EJECUTA EL STORE DE CARGAR ADH]

    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[sqlalchemy]} -- [toma el tipo de letra para marquee]

    Returns:
        [0] -- [Salida al menu]
    """
    cuit = ui.cadhCUIT.text()
    mov = ui.cadhMov.currentText()
    apellido = ui.cadhApellido.text()
    nombre = ui.cadhNombre.text()
    dni = ui.cadhDNI.text()
    parentezco = ui.cadhParentezco.currentText()
    parent = {"Hijo": 3, "Conyugue": 2}

    if cuit in ["", "0"] or len(cuit) < 11:
        return logB(ui, f"Campo CUIT son 11 digitos.", 3)
    if apellido in ["", "0"]:
        return logB(ui, f"El campo APELLIDO no peude estar vacio.", 3)
    if nombre in ["", "0"]:
        return logB(ui, f"El campo NOMBRE no peude estar vacio.", 3)
    if dni in ["", "0"] or len(dni) < 8:
        return logB(ui, f"Campo DNI son 8 digitos.{len(dni)}", 3)

    try:
        with engine.begin() as connection:
            connection.execute(
                f"""
                    EXEC [dbo].[proc_P14_03_ADHReclamos]
                    @CUITTitular = '{cuit}',
                    @Movimiento_A_B ='{mov}',
                    @Apellido_y_nombre = '{apellido} {nombre}',
                    @Ndoc = {dni},
                    @Parentesco_2C_3H = '{parent[parentezco]}',
                    @Periodo_opcional = NULL,
                    @Duplicado_1Sí_0No_opcional = NULL,
                    @Operador_opcional = NULL,
                    @Ticket_opcional = 0"""
            )
        log(ui)
        return logB(ui, f"Adherente cargado.", 1)
    except Exception as e:
        return logB(ui, f"Error cargando el adherente: {str(e)}", 3)
