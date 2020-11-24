from procs.memes import redlestips
import random
def log(engine,ui,funcion='debug', formusado=''):
    userdni = ui.loginUsrBox.text()
    try:
        with engine.begin() as connection:
            connection.execute(f"""INSERT INTO [adm_efectores].[SQLemore].[ExeStats] 
                                    (funcion,fecha,usuario, formusado) 
                                    VALUES ('{funcion}',getdate(),'{userdni}','{formusado}')"""
            )
    except Exception as e:
        return logB(ui,"Log",f"Ocurrio un error logeando a la DB: {str(e)}",3)
    ui.quoteLabel.setText(random.choice(redlestips))
    return 0

def logB(ui,proc,mensaje,tipo=0):
    if tipo==1: icono='✔'
    elif tipo==2: icono='✘'
    elif tipo==3: icono='⚠'
    else: icono=''
    ui.log.append(f"<h4>{icono} {proc}:</h4>  {mensaje} ")
    return 0