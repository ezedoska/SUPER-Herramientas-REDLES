import pandas as pd
from procs.logger import log, logB
from procs.db import engine
from PyQt5 import QtWidgets, QtGui
import datetime
import os


def Cruce_Estado_DNI(ui):
    df = pd.read_excel("cruceDNI.xlsx")
    try:
        df.to_sql(
            "##cruce", con=engine, if_exists="replace", index=False, schema="tempdb"
        )
    except Exception as e:
        return logB(ui, f"Error subiendo a tabla temporal: {str(e)}", 3)
    logB(ui, f"Excel cargado", 1)
    script = """
                    SELECT cr.orden,
                        cr.ndoc,
                        ped.apellidos,
                        ped.nombres,
                        pe.cuit,
                        ped.sexo,
                        pe.fechanacimiento,
                        l.nombrelocalidad                             AS Localidad,
                        prov.nombreprovincia                          AS Provincia,
                        pe.tipoef,
                        pe.nroformulario,
                        CASE pe.estado
                            WHEN 1 THEN 'Efector'
                            WHEN 2 THEN 'Baja'
                            WHEN 3 THEN 'Negativo'
                            WHEN 4 THEN 'En trámite'
                            ELSE 'No en base'
                        END                                           AS Estado,
                        pe.carga,
                        pe.fechap5,
                        pe.fechabaja,
                        pe.idos,
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
    path = os.path.join(
        os.path.expanduser("~"), "Desktop", f"Cruce_REDLES-{fechaexcel}"
    )
    file_name = QtWidgets.QFileDialog.getSaveFileName(
        ui.tabMain, "Save file", path, ".xlsx"
    )
    if file_name[0]:
        writer = pd.ExcelWriter(file_name[0] + file_name[1], engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Estado", encoding="unicode")
        writer.save()
        log(ui)
        return logB(ui, f"El cruce se genero correctamente", 1)
    else:
        pass
    return 0


def Cruce_Precarios(ui):
    script = """
                    SELECT cr.orden,
                        cr.ndoc,
                        ped.apellidos,
                        ped.nombres,
                        pe.cuit,
                        ped.sexo,
                        pe.fechanacimiento,
                        l.nombrelocalidad                             AS Localidad,
                        prov.nombreprovincia                          AS Provincia,
                        pe.tipoef,
                        pe.nroformulario,
                        CASE pe.estado
                            WHEN 1 THEN 'Efector'
                            WHEN 2 THEN 'Baja'
                            WHEN 3 THEN 'Negativo'
                            WHEN 4 THEN 'En trámite'
                            ELSE 'No en base'
                        END                                           AS Estado,
                        pe.carga,
                        pe.fechap5,
                        pe.fechabaja,
                        pe.idos,
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
                    where ndoc between 60000000 and 69999999
                    order by estado 
                """
    df = pd.read_sql_query(script, con=engine)

    df = pd.read_sql_query(script, con=engine)
    path = os.path.join(
        os.path.expanduser("~"), "Desktop", f"Cruce_Precarios-{fechaexcel}"
    )
    file_name = QtWidgets.QFileDialog.getSaveFileName(
        ui.tabMain, "Save file", path, ".xlsx"
    )
    if file_name[0]:
        writer = pd.ExcelWriter(file_name[0] + file_name[1], engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Estado precarios", encoding="unicode")
        writer.save()
        log(ui)
        return logB(ui, f"El cruce se genero correctamente", 1)
    else:
        pass
    return 0