import sys
import time

from .modules import processer, reader, writer


def run(_):
    start = time.time()
    PROJECT = "Claudia / consolidacion_compras_por_estilo"
    VERSION = "V1.1"
    print(f"Corriendo versión {VERSION}")
    try:
        origin_header = reader.read_origin_header(_)
        final_header = reader.read_final_header(_)
        data_header, data, stores = reader.consolidate_data(_, origin_header)
        parameters = reader.read_parameters(_)
        final_header, data = processer.process(final_header, data_header, data, stores)
        data = processer.add_parameters(final_header, data_header, data, parameters)
        # writer.write_csv(_, final_header, data)
        writer.write_excel(_, final_header, data)

    except FileNotFoundError as err:
        print(err)
        print(f"No se encontró una carpeta con el nombre {err}")
    # except UnboundLocalError as err:
    #     print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    start = time.time()
    PROJECT = "Claudia"
    VERSION = "V1.1"
    print(f"Corriendo versión {VERSION}")
    try:
        pass
        origin_header = reader.read_origin_header()
        final_header = reader.read_final_header()
        data_header, data, stores = reader.consolidate_data(origin_header)
        parameters = reader.read_parameters()
        final_header, data = processer.process(final_header, data_header, data, stores)
        data = processer.add_parameters(final_header, data_header, data, parameters)
        writer.write_csv(final_header, data)
        writer.write_excel(final_header, data)

    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    # except UnboundLocalError as err:
    #     print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")

# PRIVATE WORK LOGGER

# logger.start_work(PROJECT)
# logger.stop_work(PROJECT)
# logger.add_time(PROJECT, MINUTES, COMMENT)
