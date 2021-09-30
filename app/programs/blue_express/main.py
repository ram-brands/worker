import sys
import time

from status import Status

from .modules import compare, key_builder, paths, reader, ref_builder

# def read_files():
#     vol_weight = reader.read_BBDD_Peso_Vol(paths.BBDD_Peso_Vol)
#     tarrifs_path = reader.read_BBDD_Tarifario(paths.BBDD_TARIFARIOS)
#     bill = reader.read_ECOMSUR(paths.ECOMSUR)
#     orders = reader.read_BBDD_Blue_Analisis(paths.BBDD_BLUE_ANALISIS)
#     return vol_weight, tarrifs_path, bill, orders


def write_differences(_, data, name="diferencias", type_="diff"):
    if type_ == "diff":
        # header = "Referencia, Volumen, Peso, Cobro\n"
        header = "Referencia, Volumen, Vol Análisis, Peso, Peso Análsis, Cobro, Cobro Análisis\n"
    else:
        header = "Referencia, Key\n"

    path = f"results/{name}.xlsx"
    _.makedirs(path)

    with open(_.get_path(path), "w") as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + "\n")
        print(f"Se creó el archivo {name} exitosamente")


def run(_):
    start = time.time()
    PROJECT = "Blue Express"
    VERSION = "V1.1"
    print(f"Corriendo versión {VERSION}")
    try:
        bill = reader.read_ECOMSUR(_)
        vol_weight = reader.read_BBDD_Peso_Vol(_)
        tariffs, dest_code = reader.read_BBDD_Tarifario(_)
        (
            ref_order,
            order_sku,
            basecodes,
            store_city,
            city_zone,
            initials_region_code,
            initials_to_zone,
        ) = reader.read_BBDD_Blue_Analisis(_)
        ref_sku = ref_builder.build_ref_sku(
            _, bill, ref_order, order_sku
        )  # dict: {reference: [sku, sku, ...]}
        ref_vol_weight = ref_builder.build_ref_vol_weight(_, ref_sku, vol_weight)
        ref_key = key_builder.build_key2(
            bill,
            ref_order,
            order_sku,
            store_city,
            basecodes,
            ref_vol_weight,
            initials_region_code,
            initials_to_zone,
        )
        differences, ref_errors = compare.compare_vol_weight(
            _, bill, tariffs, ref_key, ref_vol_weight
        )
        write_differences(_, differences)
        write_differences(_, ref_errors, "errores_ref", "error")

    except FileNotFoundError as err:
        _.warning(f"No se encontró una carpeta con el nombre {err}")
        _.status.CLIENT_ERROR
    end = time.time()
    _.log(f"Programa Finalizado en {round(end - start, 2)} segundos")


if __name__ == "__main__":
    pass
