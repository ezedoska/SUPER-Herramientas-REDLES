import pandas as pd
from procs.logger import log, logB
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
import datetime
import os


def Cruce_Estado_DNI(ui):
    df = pd.read_excel("cruceDNI.xlsx", engine='openpyxl')
    try:
        df.to_sql("##cruce",
                  con=engine,
                  if_exists="replace",
                  index=False,
                  schema="tempdb")
    except Exception as e:
        return logB(ui, f"Error subiendo a tabla temporal: {str(e)}", 3)
    logB(ui, f"Excel cargado", 1)
    script = """
                    SELECT cr.orden,
                        cr.ndoc                                       AS Numero_de_Documento,
                        ped.apellidos                                 AS Apellidos,
                        ped.nombres                                   AS Nombres,
                        pe.cuit                                       AS CUIT,
                        ped.sexo                                      AS Sexo,
                        pe.fechanacimiento                            AS Fecha_Nacimiento,
                        l.nombrelocalidad                             AS Localidad,
                        prov.nombreprovincia                          AS Provincia,
                        CASE pe.tipoef
                        WHEN 1 THEN 'Persona Fisica'
                        WHEN 3 THEN 'Asociado'
                        WHEN 5 THEN 'Integrante'      end             AS Tipo_de_Efector,
                        pe.nroformulario,
                        CASE pe.estado
                            WHEN 1 THEN 'Efector'
                            WHEN 2 THEN 'Baja'
                            WHEN 3 THEN 'Negativo'
                            WHEN 4 THEN 'En trámite'
                            ELSE 'No en base'
                        END                                           AS Estado,
                        cast(pe.tipoef as varchar) + '_' +
                        CASE pe.estado
                            WHEN 1 THEN 'Efector'
                            WHEN 2 THEN 'Baja'
                            WHEN 3 THEN 'Negativo'
                            WHEN 4 THEN 'En trámite'
                            ELSE 'No en base'
                        END                                           AS tipoEf_Estado,
                        pe.carga                                      AS Fecha_Carga,
                        pe.fechap5                                    AS Fecha_P5,
                        pe.fechabaja                                  AS Fecha_Baja,
                        pe.idos                                       AS ID_Obrasocial,
                        os.nombrelargoos                              AS ObraSocial,
                        ped.id_actividad                              AS IDActividad,
                        act.descripcioncorta                          AS Actividad,
                        pe.[form_coop-proy],
                        COALESCE(pr.denominacion, c.denominacioncoop) AS Denominacion
                    FROM   ##cruce cr
                        LEFT JOIN padronefectores pe
                                ON pe.ndoc = cr.ndoc
                        LEFT JOIN padronefectoresdato ped
                                ON ped.tipoef = pe.tipoef
                                    AND ped.nroformulario = pe.nroformulario
                        LEFT JOIN obrassocialessullivan os
                                ON os.idos = pe.idos
                        LEFT JOIN proyectos11 pr
                                ON pr.nroformulario = pe.[form_coop-proy]
                        LEFT JOIN cooperativas11 c
                                ON c.nroformulario = pe.[form_coop-proy]
                        LEFT JOIN localidadesafip l
                                ON l.idlocalidad = ped.id_localidadafip
                        LEFT JOIN provincias prov
                                ON prov.codafip = l.id_provincia
                        LEFT JOIN actividades act
                                ON act.idactividad = ped.id_actividad
                                order by orden
                """

    fechaexcel = datetime.datetime.now().strftime("%Y-%m-%d-%H%M")

    df = pd.read_sql_query(script, con=engine)
    path = os.path.join(os.path.expanduser("~"), "Desktop",
                        f"Cruce_REDLES-{fechaexcel}")
    file_name = QtWidgets.QFileDialog.getSaveFileName(ui.tabMain, "Save file",
                                                      path, ".xlsx")
    if file_name[0]:
        writer = pd.ExcelWriter(file_name[0] + file_name[1],
                                engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Estado", encoding="unicode")
        writer.save()
        log(ui)
        return logB(ui, f"El cruce se genero correctamente", 1)
    else:
        pass
    return 0


def Cruce_Bajar_Anexo(ui):
    pass


def Cruce_Generar_Anexo(ui):
    pass
