from collections import namedtuple

import unidecode

from . import weight_code_calculator as wcc


def build_key(ref_origin_dest_zone, basecodes, bill, ref_vol_weight):
    Key = namedtuple("Key", ["origin", "zone", "dest_code", "weight_code"])
    ref_key = {}
    for ref in bill:
        try:
            origin = ref_origin_dest_zone[ref].origin
            zone = ref_origin_dest_zone[ref].zone
            dest_code = str(float(ref_origin_dest_zone[ref].destination_code)).replace(
                ".0", ""
            )
            weight_code = wcc.get_weight_code(basecodes, ref_vol_weight, origin, ref)
            key = Key(origin, zone, dest_code, weight_code)
            ref_key[ref] = key

        except KeyError:
            # print(ref)
            pass
    return ref_key


def build_key2(
    bill,
    ref_order,
    order_sku,
    store_city,
    basecodes,
    ref_vol_weight,
    initials_region_code,
    initials_to_zone,
):
    print("Creando Keys...")
    Key = namedtuple("Key", ["origin", "zone", "dest_code", "weight_code"])
    ref_key = {}
    error = set()
    error = 0
    for ref in bill:
        try:
            # Obtener pedido id
            order = ref_order[ref].order

        except KeyError:
            # print(ref)
            pass
            # error += 1
            # ref = None
            order = ref

        if ref:
            # Obtener Bodega y Comuna de origen
            warehouse = order_sku[order][0].origin_warehouse
            origin = store_city[warehouse]
            if origin == "Santiago":
                region = "RM"
            else:
                region = "REGIONES"
            # print(warehouse)
            # destination_city = unidecode.unidecode(order_sku[order][0].destination_city)
            destination_initials = bill[ref].dest_initials
            # dest_region = initials_to_region[destination_initials]

            dest_code = initials_region_code[(destination_initials, region)]
            zone = initials_to_zone[destination_initials]

            # dest_code = str(city_region[destination_city]).replace(".0", '')
            weight_code = wcc.get_weight_code(basecodes, ref_vol_weight, origin, ref)
            key = Key(origin, zone, dest_code, weight_code)
            ref_key[ref] = key

        # except KeyError:
        #     # print(ref)
        #     pass
    # if error:
    #     print(f'ALERTA: Hay {error} referencias con errores')
    # print(ref_key['P1-1074043040504-01'])
    # exit()

    return ref_key
