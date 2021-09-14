import sys
import time

from status import Status

from .modules import api, reader, writer


def run(_):
    start = time.time()
    PROJECT = "Devolución Masiva Mercado Pago"
    VERSION = "V1.2"
    _.log(f"Corriendo versión {VERSION}\n")
    try:
        approved = 0
        errors = []
        data = reader.read_csv(_)
        for tid in data:
            amount = data[tid]
            status, error = api.refund(_, tid, amount)
            approved += status
            errors.append(error)
        _.warning(f"\n\n{approved}/{len(data)} devoluciones aprobadas.")

        if errors:
            _.warning("ALERTA: Se creó archivo con errores.")
            _.status = Status.WARNING
            header = "TID, MONTO\n"
            writer.write_csv(_, header, errors)
        else:
            pass
            # writer.erase_results(_)

    except FileNotFoundError as err:
        _.status = Status.CLIENT_ERROR
        _.warning(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        _.status = Status.CLIENT_ERROR
        _.warning(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    pass
