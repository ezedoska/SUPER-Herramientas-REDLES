import pandas as pd
from procs.logger import log,logB
def go(engine,ui):
    form = ui.rp0Form.text()
    tipo = ui.rp0Tipo.currentText()
    tipoDict = {'Persona':1,'Asociado':3,'Integrante':5}
    if form in ['','0'] : return logB(ui,"Reenviar P0","El campo formulario no peude estar vacio.",3)
    try:
        # Checkeamos que el form no tenga otros paquetes.
        check = pd.read_sql_query(f"""SELECT estado 
                                      FROM padronefectores 
                                      WHERE tipoef={tipoDict[tipo]} and nroformulario={form}""",
                                    con=engine)
        if check.empty:
            return logB(ui,"Reenviar P0",f"[{form}] El formulario no existe.",2)
        elif check['estado'].iloc[0] != 4: 
            return logB(ui,"Reenviar P0",f"[{form}] El formulario cuenta con otros paquetes, verificar.",2)

        # Si esta en tramite todo ok y borramos.
        try:
            with engine.begin() as connection:
                connection.execute(f"""DELETE 
                                    FROM [adm_efectores].[dbo].[{tipo}s_paquete_0] 
                                    WHERE nroredles={form}""")
        except Exception as e:
            return logB(ui,"Reenviar P0",f"[{form}] Ocurrio un error al borrar el paquete 0: {str(e)}",3)
        return logB(ui,"Reenviar P0",f"[{form}] Se borro el paquete 0.",1)
    except Exception as e:
        return logB(ui,"Reenviar P0",f"[{form}] Ocurrio un error chequeando estado: {str(e)}",3)
