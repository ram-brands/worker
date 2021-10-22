from status import Status


def process(
    _, final_header, header, data, stores
):  # Format to final header and then split by store
    # final_header = ['PAÍS', 'EMPRESA', 'REF EMBARQUE', 'CANAL', 'NOMBRE DE TIENDAS', 'JERARQUIA', 'DEPARTAMENTO', 'CLASE', 'GENERO', 'MARCA', 'AÑO ON FLOOR', 'STYLE', 'DESPROD', 'TEMPORADA', 'AÑO TEMPORADA', 'DELIVERY', 'ON FLOOR ORIGINAL', 'ON FLOOR REAL', 'MES ONFLOOR REAL', 'PO#', 'UNIDADES', 'FOB USD']
    final_data = []
    for file_ in data:
        header = file_.header
        _.log(f"Processing file named: {file_.path}")
        for line in file_.data:
            new_line = [""] * len(final_header)

            new_line[final_header.index("STYLE")] = line[header.index("STYLE")]
            new_line[final_header.index("COLOR")] = line[header.index("COLOR")]
            new_line[final_header.index("DESPROD")] = line[header.index("DESCRIPTION")]
            new_line[final_header.index("TEMPORADA")] = line[header.index("TEMPORADA")]
            if line[header.index("AÑO")]:
                new_line[final_header.index("AÑO TEMPORADA")] = int(
                    line[header.index("AÑO")]
                )
                new_line[final_header.index("AÑO")] = int(line[header.index("AÑO")])
            new_line[final_header.index("DELIVERY")] = line[header.index("DEL")]
            new_line[final_header.index("DELIVERY (MES)")] = line[
                header.index("DELIVERY (MES)")
            ]
            new_line[final_header.index("PO#")] = line[header.index("PO#")]
            new_line[final_header.index("FOB USD")] = round(
                float(line[header.index("PRE-COSTING")]), 2
            )
            new_line[final_header.index("LLEGADA")] = line[header.index("LLEGADA")]
            new_line[final_header.index("CLASE (COMPRADOR)")] = line[
                header.index("CLASE")
            ]

            # if new_line[final_header.index("STYLE")] == 'U0BG21K6YW1' and not new_line[final_header.index("DELIVERY (MES)")]:
            #     print(line)
            #     print(new_line)
            #     exit()

            # new_line[final_header.index("CLASE")] = line[header.index('CLASE')]
            # new_line[final_header.index("CLASE")] = line[header.index('PRODUCTION TYPE/CATEGORY')]
            try:
                # new_line[final_header.index("DEPARTAMENTO")] = line[header.index('PRODUCT SUBCLASS')]
                new_line[final_header.index("CLASE (PROVEEDOR)")] = line[
                    header.index("PRODUCT SUBCLASS")
                ]
                # new_line[final_header.index("CLASE")] = line[header.index('PRODUCT SUBCLASS')]
            except Exception:
                _.warning(f"error with {file_.path}")
                # print(header)
                _.status = Status.CLIENT_ERROR
                exit()

            for store in stores:
                new_line_copy = new_line.copy()
                new_line_copy[final_header.index("NOMBRE DE TIENDAS")] = store
                units = line[header.index(store)]
                if not units:
                    units = 0
                new_line_copy[final_header.index("UNIDADES")] = units
                final_data.append(new_line_copy)

    return final_header, final_data


def add_parameters(
    _, final_header, data_header, data, parameters
):  # Add value de parameter fields
    final_data = []
    fl_errors = set()
    errors = set()
    errors2 = set()
    for line in data:
        store = line[final_header.index("NOMBRE DE TIENDAS")]
        line[final_header.index("PAÍS")] = parameters.store[store][0]
        line[final_header.index("EMPRESA")] = parameters.store[store][1]

        firstletter = line[final_header.index("STYLE")][0]
        try:
            line[final_header.index("CANAL")] = parameters.firstletter[firstletter][2]
            line[final_header.index("GENERO")] = parameters.firstletter[firstletter][0]
            line[final_header.index("MARCA")] = parameters.firstletter[firstletter][1]
        except Exception:
            fl_errors.add(firstletter)
            line[final_header.index("CANAL")] = "N/A"
            line[final_header.index("GENERO")] = "N/A"
            line[final_header.index("MARCA")] = "N/A"

        # subclass = line[final_header.index("DEPARTAMENTO")]
        subclass = line[final_header.index("CLASE (PROVEEDOR)")]

        try:
            department = parameters.subclass[subclass][0]
            # class_code = parameters.subclass[subclass][1]
        except Exception:
            errors.add(subclass)
            department = "N/A"
        try:
            class_code = parameters.subclass[subclass][1]
        except Exception:
            class_code = "N/A"
        try:
            jerarquia = parameters.department[department][0]
        except Exception:
            jerarquia = "N/A"

        line[final_header.index("DEPARTAMENTO")] = department
        line[final_header.index("CLASE (PROVEEDOR)")] = class_code
        line[final_header.index("JERARQUIA")] = jerarquia

        arrival = line[final_header.index("LLEGADA")]
        delivery_month = line[final_header.index("DELIVERY (MES)")]
        key = (arrival, delivery_month)
        # param arrival
        # try:
        if key in parameters.arrival:
            line[final_header.index("ON FLOOR ORIGINAL")] = parameters.arrival[key][0]
            line[final_header.index("ON FLOOR REAL")] = parameters.arrival[key][1]
            line[final_header.index("MES ONFLOOR REAL")] = parameters.arrival[key][2]
        else:
            # print(key)
            pass

        # Edit Canal to wholesale
        store = line[final_header.index("NOMBRE DE TIENDAS")]
        if store in ["MIYAKI", "FALABELLA", "PARIS", "SAGA FALABELLA"]:
            line[final_header.index("CANAL")] = "WHOLESALE"
        if store == "SAGA FALABELLA":
            line[final_header.index("PAÍS")] = "PERÚ"

    if errors:
        _.warning(f"ERROR: Estas subclases no se encuentran en los parámetros:")
        # for e in errors:
        #     print(e)
        _.warning(errors)
        _.status = Status.WARNING

    return data
