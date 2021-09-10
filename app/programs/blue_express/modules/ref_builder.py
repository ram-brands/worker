from . import cost_calculator as cc
from collections import namedtuple
import unidecode


def build_ref_sku(bill, ref_order, order_sku):
    ref_sku = {}  # {ref:[sku, sku, ...]}
    order_error = set()
    for ref in bill:
        if ref in ref_order:
            order = ref_order[ref].order
        else:
            order = ''.join([s for s in ref if s.isdigit()])
        try:
            ref_sku[ref] = order_sku[order]
        except KeyError:
            order_error.add(ref)
    if order_error:
        print("Error en ordenes OMS en las siguentes ref:")
        print(order_error)
    return ref_sku


def build_ref_origin_dest_zone(bill, ref_to_order, order_sku, store_city, city_zone):
    pass
    dest_error = set()
    ref_origin_dest_zone = {}
    Path = namedtuple("Path", ['origin', 'zone', 'destination_code'])
    for ref in bill:
        try:
            if ref in ref_to_order[ref]:
                order = ref_to_order[ref]
            else:
                order = ref
            data = order_sku[order]
            origin = store_city[data[0].origin_warehouse]
            destination = unidecode.unidecode(data[0].destination_city)
            zone = city_zone[destination].zone
            destination_code = city_zone[destination].code
            destination = data[0].destination_city
            ref_origin_dest_zone[ref] = Path(origin, zone, destination_code)
        except KeyError:
            # print(destination)
            dest_error.add(destination)
            pass
    if dest_error:
        print("Error con destinos en BBDD Destino en:")
        print(dest_error)
    return ref_origin_dest_zone


def build_ref_to_order(ref_order, bill):
    ref_to_order = {}
    for ref in bill:
        if ref not in ref_order:
            order = ''.join([s for s in ref if s.isdigit()])
        else:
            order = ref_order[ref].order
        ref_to_order[ref] = order
    return ref_to_order




def build_ref_vol_weight(ref_sku, vol_weight):
    Attributes = namedtuple("Attributes", ['total_vol', 'total_weight'])
    ref_weight_vol = {}
    error_sku = set()
    for ref in ref_sku:
        # print(ref_sku[ref])
        items = ref_sku[ref]
        order_items = [x.sku for x in items]
        total_vol, total_weight, error = cc.get_order_weight(order_items, vol_weight)
        ref_weight_vol[ref] = Attributes(total_vol, total_weight)
        error_sku |= error
    if error_sku:
        print("Error en sku, probablemente de BBDD PB Limpia en:")
        print(error_sku)
    return ref_weight_vol


if __name__ == "__main__":
    # ref_order, order_sku = reader.read_BBDD_Blue_Analisis(paths.BBDD_BLUE_ANALISIS)
    # bill = reader.read_ECOMSUR(paths.ECOMSUR)
    # build_ref_sku(bill, ref_order, order_sku)
    pass
