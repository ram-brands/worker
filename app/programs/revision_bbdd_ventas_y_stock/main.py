import time

from . import modules


def run(_):
    DIRECTORY_MATRIZ = "data"

    PVD_PATH = "data/ProcesoVentasDiarias.xlsx"
    PARAMETERS_PATH = "data/Parametros.xlsx"
    OUTPUT_FILE_NAME = "BBDD Ventas y Stock"
    LOG_PATH = "logs/log"
    PROJECT = "BBDD Ventas y Stock"
    start = time.time()
    v = "V1.8"
    print(f"Corriendo versión {v}")
    # log(0, v, PROJECT)
    try:
        header, data = modules.read_PVD(_, PVD_PATH)
        param = modules.read_param(_, PARAMETERS_PATH)
        header, data = modules.create_macro(header, data, param)
        modules.write(_, header, data, OUTPUT_FILE_NAME)
        # log(1, v, PROJECT)
    except FileNotFoundError as err:
        print(err)
        print(f"No se encontró una carpeta con el nombre {DIRECTORY_MATRIZ}")
        # log(2, v, PROJECT)
    end = time.time()
    total_time = round(end - start, 2)
    print(
        f"Programa Finalizado en {int(total_time//60)}:{f'{round(total_time%60):02}'} minutos"
    )


if __name__ == "__main__":
    pass
