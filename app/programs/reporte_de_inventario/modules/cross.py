from status import Status


def cross(_, physical, sap, maestro):
    category_1 = []
    category_2 = []
    category_3 = []
    category_4 = []
    category_5 = []

    for sku in sap:
        if sku not in physical:
            if sap[sku] > 0:  # positivo in sap
                category_1.append([sku, -1 * sap[sku]])
            else:  # Negative in sap
                category_3.append([sku, -1 * sap[sku]])

    for sku in physical:
        if sku not in sap:
            category_4.append([sku, physical[sku]])

    # Categories for when sku is in both sides:
    for sku in sap:
        if sku in physical:
            if sap[sku] != physical[sku]:
                if sap[sku] > physical[sku]:
                    category_2.append([sku, physical[sku] - sap[sku]])
                else:
                    category_5.append([sku, physical[sku] - sap[sku]])

    categories = [category_1, category_2, category_3, category_4, category_5]
    for cat in categories:
        for line in cat:
            sku = line[0]
            stock = line[1]
            if sku in maestro:
                price = maestro[sku]
                total_price = round(stock * price)
            else:
                price = ""
                total_price = ""
                _.warning(f"El sku {sku} no está en el maestro.")
                _.status = Status.WARNING
            line.append(price)
            line.append(total_price)

    return categories


def get_summary(_, categories, sap_qty, physical_qty, store):
    category_1_name = "Faltantes estan en sap y faltan en fisico"
    category_2_name = "Faltantes resta entre fisico y sap"
    category_3_name = "Negativos estan en sap y faltan en fisico"
    category_4_name = "sobrantes estan en fisico y faltan en SAP"
    category_5_name = "Sobrantes resta entre fisico y sap"

    categories_names = [
        category_1_name,
        category_2_name,
        category_3_name,
        category_4_name,
        category_5_name,
    ]

    total_stock = 0
    total_price = 0
    summary = []
    for i in range(len(categories)):
        c = categories[i]
        name = categories_names[i]
        stock = 0
        price = 0
        for x in c:
            stock += x[1]
            if x[3]:
                price += x[3]
        summary.append([name, stock, price])
        total_stock += stock
        total_price += price
    summary.append(["Total general", total_stock, total_price])
    summary.append([""])
    summary.append(["Cantidad Físico", physical_qty])
    summary.append(["Cantidad Sap", sap_qty])
    summary.append(["Diferencia", physical_qty - sap_qty])
    if (physical_qty - sap_qty) != total_stock:
        _.warning(f"En la tienda {store} existe diferencia en stock.")
        _.status = Status.WARNING

    return summary
