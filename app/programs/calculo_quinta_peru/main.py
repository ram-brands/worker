import sys
import time

from .modules import processor, reader, writer


def run(fs):
    start = time.time()
    PROJECT = "Impuestos Quinta Perú"
    VERSION = "V1.1"
    print(f"Corriendo versión {VERSION}")
    try:
        base_pay = reader.read_base_pay(fs=fs)
        total_pay = reader.read_total_pay(fs=fs)
        variable_pay = processor.get_variable_pay(base_pay, total_pay)
        taxes = processor.get_taxes(total_pay, base_pay, variable_pay)
        header, formatted_taxes = processor.format_taxes(taxes)
        writer.write_csv(header, formatted_taxes)

    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    start = time.time()
    PROJECT = "Impuestos Quinta Perú"
    VERSION = "V1.1"
    print(f"Corriendo versión {VERSION}")
    try:
        pass
        base_pay = reader.read_base_pay()
        total_pay = reader.read_total_pay()
        variable_pay = processor.get_variable_pay(base_pay, total_pay)
        # print(variable_pay)
        taxes = processor.get_taxes(total_pay, base_pay, variable_pay)
        header, formatted_taxes = processor.format_taxes(taxes)
        writer.write_csv(header, formatted_taxes)

    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")

# PRIVATE WORK LOGGER

# logger.start_work(PROJECT)
# logger.stop_work(PROJECT)
# logger.add_time(PROJECT, MINUTES, COMMENT)
