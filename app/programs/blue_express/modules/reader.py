from collections import namedtuple

from xlrd import open_workbook

from . import paths


def read_BBDD_Peso_Vol(_, path=paths.BBDD_Peso_Vol):  # Leer BBDD de peso y vol por sku
    print(f"Leyendo BBDD Peso & Vol...")
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "BBDD PESO&VOL":
            data = {}
            Attribute = namedtuple("Attribute", ["weight", "volume"])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    sku_index = header.index("Sku Codigo")
                    weight_index = header.index("Sku Peso Real")
                    volume_index = header.index("Volumetrico")
                else:
                    sku = str(col_value[sku_index]).replace(".0", "")
                    weight = int(col_value[weight_index]) / 1000
                    volume = float(col_value[volume_index])
                    data[sku] = Attribute(weight, volume)
    return data


def read_BBDD_Tarifario(_, path=paths.BBDD_TARIFARIOS):  # Leer BBDD de tarifas por tramo
    print(f"Leyendo BBDD Tarifario...")
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "BBDD":
            data = {}
            dest_code = {}
            Key = namedtuple("Key", ["origin", "zone", "dest_code", "weight_code"])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    origin_index = header.index("Origen")
                    geo_origin_dest_index = header.index("Grupo Geo Destino")
                    code_index = header.index("Cod")
                    weight_code_index = header.index("Cod Peso")
                    cost_index = header.index("Valor")
                    dest_index = header.index("Base Destino")
                else:
                    origin = col_value[origin_index]
                    geo_destiny_group = col_value[geo_origin_dest_index].upper()
                    code = str(float(col_value[code_index])).replace(".0", "")
                    weight_code = str(col_value[weight_code_index])
                    try:
                        cost = int(col_value[cost_index])
                    except ValueError:
                        print(
                            f"error: no hay costo para llave {origin},{geo_destiny_group}"
                        )
                    key = Key(origin, geo_destiny_group, code, weight_code)
                    data[key] = cost

                    dest = col_value[dest_index]
                    if dest not in dest_code:
                        dest_code[dest] = code
    return data, dest_code


def read_ECOMSUR(_, path=paths.ECOMSUR):  # Leer Factura de ECOMSUR
    print(f"Leyendo Factura ECOMSUR...")
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "Sheet1":
            data = {}
            Bill = namedtuple("Bill", ["volume", "weight", "cost", "dest_initials"])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    volume_index = header.index("Suma de VOLUMEN")
                    weight_index = header.index("Suma de KILOS")
                    cost_index = header.index("Suma de MontoFacturado")
                    reference_index = header.index("REFERENCIAS")
                    initials_index = header.index("DESTINO")
                else:
                    if col_value[0]:
                        volume = float(col_value[volume_index])
                        weight = float(col_value[weight_index])
                        cost = int(col_value[cost_index])
                        reference = str(col_value[reference_index]).replace(".0", "")
                        initials = col_value[initials_index]
                        bill = Bill(volume, weight, cost, initials)
                        data[reference] = bill
    return data


def read_BBDD_Blue_Analisis(_, path=paths.BBDD_BLUE_ANALISIS):
    print(f"Leyendo BBDD Blue Analisis...")
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "BBDD OMS":  # Obtener dict con referencia:pedido_Id
            ref_order = {}
            Order = namedtuple("Order", ["order", "warehouse"])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    reference_index = header.index("Nro Pedido Externo")
                    order_index = header.index("Pedido")
                    warehouse_index = header.index("Bodega")
                else:
                    reference = str(col_value[reference_index])
                    order = str(col_value[order_index]).replace(".0", "")
                    warehouse = col_value[warehouse_index]
                    value = Order(order, warehouse)
                    ref_order[reference] = value
        if s.name == "BBDD PB Limpia":  # Obtener dict con sku por orden
            order_sku = {}
            Sku = namedtuple("Sku", ["sku", "origin_warehouse", "destination_city"])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    order_index = header.index("Pedido_Id")
                    sku_index = header.index("SKU")
                    origin_index = header.index("Bodega_Nombre")
                    destination_index = header.index("Comuna")
                else:
                    sku = str(col_value[sku_index]).replace(".0", "")
                    order = str(col_value[order_index]).replace(".0", "")
                    origin = col_value[origin_index]
                    destination = col_value[destination_index].upper()
                    value = Sku(sku, origin, destination)
                    if order in order_sku:
                        order_sku[order].append(value)
                    else:
                        order_sku[order] = [value]
        if s.name == "BBDD Varias":  # Obtener dict de Tienda:Cuidad y CodigoPeso
            store_city = {}
            for row in range(2, s.nrows):
                col_value = []
                for col in range(1, 3):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 2:
                    header = col_value
                    store_index = header.index("Tienda")
                    city_index = header.index("Ciudad")
                else:
                    store = col_value[store_index]
                    city = col_value[city_index]
                    store_city[store] = city
            basecodes = {}
            santiago_basecodes = []
            regions_basecodes = []
            BaseCode = namedtuple("BaseCode", ["weightcode", "min", "max"])
            for row in range(3, s.nrows):
                col_value = []
                for col in range(4, 8):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 3:
                    header = col_value
                    code_index = header.index("Cod Peso")
                    min_index = header.index("Minimo")
                    max_index = header.index("Maximo")
                else:
                    code = col_value[code_index]
                    min_ = col_value[min_index]
                    max_ = col_value[max_index]
                    if not code:
                        break
                    basecode = BaseCode(code, min_, max_)
                    santiago_basecodes.append(basecode)
            for row in range(3, s.nrows):
                col_value = []
                for col in range(9, 13):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 3:
                    header = col_value
                    code_index = header.index("Cod Peso")
                    min_index = header.index("Minimo")
                    max_index = header.index("Maximo")
                else:
                    code = col_value[code_index]
                    min_ = col_value[min_index]
                    max_ = col_value[max_index]
                    if not code:
                        break
                    basecode = BaseCode(code, min_, max_)
                    regions_basecodes.append(basecode)
            basecodes["santiago"] = santiago_basecodes
            basecodes["regiones"] = regions_basecodes

        if s.name == "BBDD Destino":  # Obtener dict sigla:cuidad
            city_zone = {}
            initials_region_code = {}
            initials_to_zone = {}
            rm_cities = set()
            Region = namedtuple("Region", ["origin_region", "zone"])
            for row in range(1, s.nrows):
                col_value = []
                for col in range(9, s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 1:
                    header = col_value
                    initial_index = header.index("SIGLA")
                    city_index = header.index("LOCALIDAD")
                    code_index = header.index("codigoRegion")
                    zone_index = header.index("ZONA")
                    # region_index = header.index('nombreComuna')
                    origin_index = header.index("Origen")
                else:
                    # initial = col_value[initial_index]
                    dest_initials = col_value[initial_index]
                    city = col_value[city_index].upper()
                    code = col_value[code_index]
                    origin = col_value[origin_index]
                    zone = col_value[zone_index]
                    # value = City(code, zone)
                    # initial_city[initial] = value
                    # city_zone[city] = value

                    # origin = col_value[origin_index]
                    #     city_code[(city, origin)] = str(code).replace('.0', '')
                    initials_region_code[(dest_initials, origin)] = str(code).replace(
                        ".0", ""
                    )
                    initials_to_zone[dest_initials] = zone
    return (
        ref_order,
        order_sku,
        basecodes,
        store_city,
        city_zone,
        initials_region_code,
        initials_to_zone,
    )


if __name__ == "__main__":
    pass
