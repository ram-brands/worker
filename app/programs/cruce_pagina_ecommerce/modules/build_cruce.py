def get_sku_from_uc(uc):
    l = uc.split("-")
    if len(l) == 2:
        return l[1]
    if len(l) == 3:
        return l[1] + "-" + l[2]


def build_cruce(_, estoque, stock, maestro, exportacion, atrapero):
    _.log("Realizando Cruce de información...")
    header = [
        "AvailableQuantity",
        "stock sap",
        "RefId",
        "Codigo Unico",
        "Estilo-color",
        "REPETIDOS",
        "_ActivateSkuIfPossible c",
        "_SkuIsActive (No es posible modificar)",
        "_ShowOnSite",
        "_CategoryName al",
        "MOSTRAR EN TIENDA PIM",
    ]
    data = []
    count = 0
    sc_counter = {}
    # Get header indexes
    estoque_stock_index = header.index("AvailableQuantity")
    stock_stock_index = header.index("stock sap")
    sku_index = header.index("RefId")
    uc_index = header.index("Codigo Unico")
    sc_index = header.index("Estilo-color")
    repeated_index = header.index("REPETIDOS")
    active_index = header.index("_ActivateSkuIfPossible c")
    category_index = header.index("_CategoryName al")
    pim_index = header.index("MOSTRAR EN TIENDA PIM")
    active2_index = header.index("_SkuIsActive (No es posible modificar)")
    show_index = header.index("_ShowOnSite")

    # Build cruce
    for uc in estoque:
        line = [None] * 11
        line[estoque_stock_index] = int(estoque[uc])
        line[uc_index] = uc
        sku = get_sku_from_uc(uc)
        line[sku_index] = sku
        try:
            line[stock_stock_index] = int(float(stock[uc]))
        except KeyError:
            line[stock_stock_index] = 0

        # Maestro para obtener estilo-color
        try:
            sc = maestro[sku]
            line[sc_index] = sc
        except KeyError:
            sc = "sin estilo-color"
            line[sc_index] = sc

        # Exportacion para pim
        try:
            line[pim_index] = exportacion[sku]
        except KeyError:
            line[pim_index] = 0

        # Atrapero para active y category
        try:
            value = atrapero[sku]
            line[active_index] = value.active
            line[active2_index] = value.active2
            line[show_index] = value.show
            line[category_index] = value.category
        except KeyError:
            print(sku)
            line[active_index] = value.active
            line[category_index] = value.category

        # Calcular Repeticiones

        if sc in sc_counter:
            sc_counter[sc] += 1
        else:
            sc_counter[sc] = 1
        line[repeated_index] = sc_counter[sc]

        data.append(line)

    # Calcular Repeticiones

    return header, data
