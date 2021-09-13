import time
from status import Status
from .modules import build_cruce, compare, reader, writer


def read_files(_):
    stock = reader.read_stock(_)
    estoque = reader.read_estoque(_)
    maestro = reader.read_maestro(_)
    exportacion = reader.read_exportacion(_)
    atrapero = reader.read_atrapero(_)

    return stock, estoque, maestro, exportacion, atrapero


def run(_):
    start = time.time()
    PROJECT = "Cruce Pagina E-Commerce"
    VERSION = "V1.1"
    _.log(f"Corriendo versión {VERSION}")
    try:
        stock, estoque, maestro, exportacion, atrapero = read_files(_)
        header, data = build_cruce.build_cruce(
            _, estoque, stock, maestro, exportacion, atrapero
        )
        compare.compare(_, header, data)
        writer.write_excel(_, header, data, "cruce")
    # except KeyError:
    #     pass
    except FileNotFoundError as err:
        _.warning(f"No se encontró una carpeta con el nombre {err}")
        _.status = Status.CLIENT_ERROR
    except UnboundLocalError as err:
        _.warning(f"No se encontró la página {err} en los archivos de ")
        _.status = Status.CLIENT_ERROR
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    pass
