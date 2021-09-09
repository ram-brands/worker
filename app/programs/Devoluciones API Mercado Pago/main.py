import time
import sys
from .modules import reader, api, writer


def run(fs):
    start = time.time()
    PROJECT = 'Devolución Masiva Mercado Pago'
    VERSION = 'V1.2'
    print(f"Corriendo versión {VERSION}\n")
    try:
        approved = 0
        errors = []
        data = reader.read_csv(fs)
        for tid in data:
            amount = data[tid]
            status, error = api.refund(tid, amount)
            approved += status
            errors.append(error)
        print(f"\n\n{approved}/{len(data)} devoluciones aprobadas.")

        if errors:
            print("ALERTA: Se creó archivo con errores.")
            header = 'TID, MONTO\n'
            writer.write_csv(fs, header, errors)
        else:
            writer.erase_results(fs)

    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    except UnboundLocalError as err:
        print(f"No se encontró la página {err} en los archivos de ")
    # except Exception as err:
    #     print(f"Ocurrio un error: {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")

if __name__ == "__main__":
    pass