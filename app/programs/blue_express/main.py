import time
import sys
from .modules import reader
from .modules import paths
from .modules import ref_builder
from .modules import compare
from .modules import key_builder


# def read_files():
#     vol_weight = reader.read_BBDD_Peso_Vol(paths.BBDD_Peso_Vol)
#     tarrifs_path = reader.read_BBDD_Tarifario(paths.BBDD_TARIFARIOS)
#     bill = reader.read_ECOMSUR(paths.ECOMSUR)
#     orders = reader.read_BBDD_Blue_Analisis(paths.BBDD_BLUE_ANALISIS)
#     return vol_weight, tarrifs_path, bill, orders


def write_differences(fs, data, name="diferencias.csv", type_='diff'):
    if type_ == 'diff':
        # header = "Referencia, Volumen, Peso, Cobro\n"
        header = "Referencia, Volumen, Vol Análisis, Peso, Peso Análsis, Cobro, Cobro Análisis\n"
    else:
        header = "Referencia, Key\n"
    with open(fs.get_path(f"results/{name}"), 'w') as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + '\n')
        print(f"Se creó el archivo {name} exitosamente")


def run(fs):
    start = time.time()
    PROJECT = 'Blue Express'
    VERSION = 'V1.1'
    print(f"Corriendo versión {VERSION}")
    try:
        bill = reader.read_ECOMSUR(fs)
        vol_weight = reader.read_BBDD_Peso_Vol(fs)
        tariffs, dest_code = reader.read_BBDD_Tarifario(fs)
        ref_order, order_sku, basecodes, store_city, city_zone, initials_region_code, initials_to_zone = reader.read_BBDD_Blue_Analisis(fs)
        ref_sku = ref_builder.build_ref_sku(bill, ref_order, order_sku)  # dict: {reference: [sku, sku, ...]}
        ref_vol_weight = ref_builder.build_ref_vol_weight(ref_sku, vol_weight)
        ref_key = key_builder.build_key2(bill, ref_order, order_sku, store_city, basecodes, ref_vol_weight, initials_region_code, initials_to_zone)
        differences, ref_errors = compare.compare_vol_weight(bill, tariffs, ref_key, ref_vol_weight)
        write_differences(fs, differences)
        write_differences(fs, ref_errors, 'errores_ref.csv', 'error')

    except FileNotFoundError as err:
        print(f"No se encontró una carpeta con el nombre {err}")
    end = time.time()
    print(f"Programa Finalizado en {round(end - start, 2)} segundos")

if __name__ == "__main__":
    pass
