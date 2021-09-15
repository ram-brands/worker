import sys
import time

from .modules import cross, reader, writer

from status import Status


def run(_):
    start = time.time()
    PROJECT = "Reporte Inventario"
    VERSION = "V1.1"
    _.log(f"Corriendo {PROJECT} versión {VERSION}")
    try:
        physical = reader.read_physical(_)
        sap = reader.read_sap(_)
        categories = cross.cross(physical, sap)
        x = 1
        header = ["SKU", "Cantidad"]
        for c in categories:
            writer.write_excel(_, header, c, f"categoria_{x}")
            x += 1
        summary = cross.get_summary(categories)
        header = ["Etiqueta de fila", "Suma de brecha"]
        writer.write_excel(_, header, summary, "resumen")

    except FileNotFoundError as err:
        _.status = Status.CLIENT_ERROR
        _.warning(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        _.status = Status.CLIENT_ERROR
        _.warning(f"No se encontró la página {err} en los archivos de ")
    except Exception as err:
        _.status = Status.CLIENT_ERROR
        _.warning(f"Error: {err}")
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")
