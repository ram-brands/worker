import sys
import time

from status import Status

from .modules import consolidate, reader, writer


def run(_):
    start = time.time()
    PROJECT = "Recepción Mercadería Discrepancias"
    VERSION = "V1.1"
    _.log(f"Corriendo {PROJECT} versión {VERSION}")
    try:
        data = reader.read_all_files(_)
        header, data, summary = consolidate.consolidate(data)
        # writer.write_csv(_, header, data, name="consolidado")
        writer.write_excel(_, header, data, name="consolidado")
        summary_header = ["Tienda", "Faltantes", "Sobrantes"]
        writer.write_excel(_, summary_header, summary, name="resumen")

    except Exception as err:
        _.log(f"Error ocurred: {err}")
        _.warning("Ocurrió un error, problemente con el formato.")
        _.status = Status.CLIENT_ERROR
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    pass
