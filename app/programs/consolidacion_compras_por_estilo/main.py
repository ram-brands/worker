import sys
import time
from status import Status
from .modules import processer, reader, writer


def run(_):
    start = time.time()
    PROJECT = "Claudia / consolidacion_compras_por_estilo"
    VERSION = "V1.1"
    _.log(f"Corriendo {PROJECT} versión {VERSION}")
    try:
        origin_header = reader.read_origin_header(_)
        final_header = reader.read_final_header(_)
        data_header, data, stores = reader.consolidate_data(_, origin_header)
        parameters = reader.read_parameters(_)
        final_header, data = processer.process(_, final_header, data_header, data, stores)
        data = processer.add_parameters(_, final_header, data_header, data, parameters)
        # writer.write_csv(_, final_header, data)
        writer.write_excel(_, final_header, data)

    except FileNotFoundError as err:
        _.log(err)
        _.warning(f"No se encontró una carpeta con el nombre {err}")
        _.status = Status.CLIENT_ERROR
    # except UnboundLocalError as err:
    #     print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")
