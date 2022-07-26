import pandas as pd
from procs.logger import log, logB
from procs.db import engine


def Subir_Cambio_CUIT(ui):
    """
    [Subir Cambio CUIT]
    Arguments:
        engine {[sqlalchemy]} -- [engine creado por sqlalchemy]
        f {[figlet]} -- [toma el tipo de letra para marquee]
    """
    form = ui.ccForm.text()
    tipo = ui.ccTipo.currentText()
    cuitN = ui.ccNuevo.text()
    cuitV = ui.ccViejo.text()
    tipoDict = {
        "Persona": 1,
        "Asociado": 3,
        "Integrante": 5,
    }
    if form in ["", "0"]:
        return logB(ui, "El campo FORMULARIO no peude estar vacio.", 3)
    if cuitN in ["", "0"] or len(cuitN) != 11:
        return logB(ui, "El campo CUIT NUEVO debe tener 11 digitos.", 3)
    if cuitV in ["", "0"] or len(cuitV) != 11:
        return logB(ui, "El campo CUIT VIEJO debe tener 11 digitos.", 3)

    try:
        with engine.begin() as connection:
            connection.execute(
                f"""INSERT INTO [adm_efectores].[dbo].[CambioCUIT]
                        ([tiporedles]
                        ,[nroredles]
                        ,[CUITv]
                        ,[CUITn]
                        ,[estado]
                        ,[fecha])
                    VALUES
                        ({tipoDict[tipo]}
                        ,{form}
                        ,'{cuitV}'
                        ,'{cuitN}'
                        ,'CC'
                        ,getdate())
                """
            )
        log(ui, form)
        return logB(ui, f"[{form}] Cambio insertado con exito", 1)
    except Exception as e:
        return logB(
            ui,
            "Cambio CUIT",
            f"[{form}] Hubo un error en la insercion del cambio : {str(e)}",
            3,
        )
    return 0


def Generar_P0(ui):
    try:
        result = pd.read_sql_query(
            """SELECT 
                    CAST([CLAVE]AS CHAR(17)) +
                    CAST([TDOC]AS CHAR(2)) + 
                    CAST([NroDocumento]AS CHAR(10)) +
                    CAST([SEXO]AS CHAR(1))+
                    CAST([FNAC]AS CHAR(8)) +
                    CAST([Apellido]AS CHAR(50)) +
                    CAST([Nombres]AS CHAR(50))+
                    CAST([CodPaisOrigen]AS CHAR(3)) + 
                    CAST([PaisOrigen]AS CHAR(30)) +
                    CAST([CodActividad]AS CHAR(6)) +  
                    CAST([calle]AS CHAR(40)) +
                    CAST([numero]AS CHAR(6)) +
                    CAST([piso]AS CHAR(5)) +
                    CAST([depto]AS CHAR(5)) +
                    CAST([manzana]AS CHAR(5)) +
                    CAST([sector]AS CHAR(5)) +
                    CAST([torre]AS CHAR(5)) +
                    CAST([TipodatoAdic]AS CHAR(2)) +
                    CAST([DatoAdicional]AS CHAR(20)) +
                    CAST([CodProvincia]AS CHAR(2)) +
                    CAST([CPostal]AS CHAR(8))+
                    cast([Localidad] as char(15)) +
                    CASE WHEN nrofiscal=numero then '1' else '0' END +
                    CASE WHEN nrofiscal=numero then replicate(' ',40)else cast([calleFiscal] AS CHAR(40)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',6) else cast([NroFiscal]AS CHAR(6))end +
                    CASE WHEN nrofiscal=numero then replicate(' ',5) else cast([PisoFiscal]AS CHAR(5)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',5) else cast([DeptoFiscal]AS CHAR(5))end +
                    CASE WHEN nrofiscal=numero then replicate(' ',5) else cast([ManzanaFiscal]AS CHAR(5)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',5) else cast([SectorFiscal]AS CHAR(5)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',5) else cast([TorreFiscal]AS CHAR(5)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',2) else cast([TipodatoAdicFiscal]AS CHAR(2)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',20)else cast([DatoAdicionalFiscal]AS CHAR(20)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',2) else cast([CodProvinciaFiscal]AS CHAR(2)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',8) else cast([CPostalFiscal]AS CHAR(8)) end+
                    CASE WHEN nrofiscal=numero then replicate(' ',15)else cast([LocalidadFiscal] as char(15)) end+
                    cast([VencimientoCermi]AS CHAR(8)) + 
                    cast([CUIT]AS CHAR(11)) + 
                    cast([TipoResidencia]AS CHAR(1)) + 
                    cast([Email]AS CHAR(60)) + 
                    cast([TipoEmail]AS CHAR(2)) 
                    AS [text]
                FROM [dbo].[Envio_p0_CAMBIOCUIT] """,
            con=engine,
        )
        if result.empty:
            return logB(ui, f"No habia lineas que generar.", 2)
    except Exception as e:
        return logB(ui, f"Hubo un error bajando p0: {str(e)}", 3)
    return ui.ccp0Text.append(
        f"{result.to_string(index=False,header=False,index_names=False)}"
    )


def Generar_P4(ui):
    try:
        result = pd.read_sql_query(
            """                     
                SELECT cast('02' as char(2)),CAST(CUIT as char (11)) as CUIT,             
                RIGHT('000' + Ltrim(Rtrim(X.caracterizacion)),3) as caracterizacion,             
                ---CAST(X.caracterizacion as char (3) ) as caracterizacion ,                       
                CONVERT(char(8), getdate(), 112) as fecha_carac ,            
                CONVERT(char(8), getdate(), 112) as fecha_info                        
                FROM dbo.Personas_Paquete_4 X                        
                where x.CUIT in (select CUITn from cambioCUIT where estado = '1253')

                union
                            
                SELECT   cast('02' as char(2)),
                CAST(x.CUIT as char (11)) as CUIT,       
                RIGHT('000' + Ltrim(Rtrim(X.caracterizacion)),3) as caracterizacion,            
                CONVERT(char(8), getdate(), 112) as fecha_carac ,              
                CONVERT(char(8), getdate(), 112) as fecha_info              
                FROM dbo.Asociados_Paquete_4 X              
                inner join dbo.Asociados_Paquete_4 XX              
                on XX.id_asociado=X.id_asociado               
                where X.CUIT  in (select CUITn from cambioCUIT where estado = '1253')

                union
                            
                SELECT   cast('02' as char(2)),
                CAST(x.CUIT as char (11)) as CUIT,       
                RIGHT('000' + Ltrim(Rtrim(X.caracterizacion)),3) as caracterizacion,            
                CONVERT(char(8), getdate(), 112) as fecha_carac ,              
                CONVERT(char(8), getdate(), 112) as fecha_info              
                FROM dbo.Integrantes_Paquete_4 X              
                inner join dbo.Integrantes_Paquete_4 XX              
                on XX.id_integrante=X.id_integrante
                where X.CUIT  in (select CUITn from cambioCUIT where estado = '1253')


                SELECT     TOP 100 PERCENT CAST('03' AS char(2)) AS cab3, CAST(CUIT AS char(11)) AS CUIT, CAST(esSumatoria AS char(1)) AS esSumatoria, 
                                    RIGHT('000000' + CAST(cod_OSocial AS nvarchar), 6) AS cod_OSocial, COALESCE (CAST(tipo_doc AS char(2)), CAST('' AS char(2))) AS tipo_doc, 
                                    COALESCE (CAST(nro_doc AS char(11)), CAST('' AS char(11))) AS nro_doc, CAST(COALESCE (apell_nomb, '') AS char(50)) AS apell_nomb, 
                                    COALESCE (CAST(parentesco AS char(1)), CAST('' AS char(1))) AS parentesco, CAST('A' AS char(1)) AS tipoope, CONVERT(char(8), GETDATE(), 112) AS fecha_info
                FROM         dbo.Anexo_Paquete_4_OS AS X
                where X.CUIT  in (select CUITn from cambioCUIT where estado = '1253' or estado <> 'OK')
                group by cuit,cod_OSocial,tipo_doc,nro_doc,apell_nomb,parentesco,esSumatoria
                order by parentesco """,
            con=engine,
        )
        if result.empty:
            return logB(ui, f"No habia lineas que generar.", 2)
    except Exception as e:
        return logB(ui, f"Hubo un error bajando p0: {str(e)}", 3)
    return ui.ccp4Text.append(
        f"{result.to_string(index=False,header=False,index_names=False)}"
    )
