import sys
import time

from status import Status

from .modules import processor, reader, writer


def run(_):
    start = time.time()
    PROJECT = "Impuestos Quinta Perú"
    VERSION = "V1.1"
    _.log(f"Corriendo versión {VERSION}")
    try:
        base_pay = reader.read_base_pay(_=_)
        total_pay = reader.read_total_pay(_=_)
        variable_pay = processor.get_variable_pay(base_pay, total_pay)
        taxes = processor.get_taxes(_, total_pay, base_pay, variable_pay)
        header, formatted_taxes = processor.format_taxes(taxes)
        writer.write_csv(_, header, formatted_taxes)

    except UnboundLocalError as err:
        _.warning(f"No se encontró la página {err} en los archivos de ")
        _.status = Status.CLIENT_ERROR
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")
