import time
from .modules import reader
from .modules import compare
from .modules import build_cruce
from .modules import writer


def read_files(fs):
    stock = reader.read_stock(fs)
    estoque = reader.read_estoque(fs)
    maestro = reader.read_maestro(fs)
    exportacion = reader.read_exportacion(fs)
    atrapero = reader.read_atrapero(fs)

    return stock, estoque, maestro, exportacion, atrapero


def run(fs):
    start = time.time()
    PROJECT = 'Cruce Pagina E-Commerce'
    VERSION = 'V1.1'
    print(f"Corriendo versión {VERSION}")
    try:
        pass
        stock, estoque, maestro, exportacion, atrapero = read_files(fs)
        header, data = build_cruce.build_cruce(estoque, stock, maestro, exportacion, atrapero)
        compare.compare(fs, header, data)
        writer.write_excel(fs, header, data, 'cruce')
    except KeyError:
        pass
    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        print(f"No se encontró la página {err} en los archivos de ")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")

if __name__ == "__main__":
    pass
