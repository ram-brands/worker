def cross(physical, sap):
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

    return categories


def get_summary(categories):
    category_1_name = 'Faltantes estan en sap y faltan en fisico'
    category_2_name = 'Faltantes resta entre fisico y sap'
    category_3_name = 'Negativos estan en sap y faltan en fisico'
    category_4_name = 'sobrantes estan en fisico y faltan en SAP'
    category_5_name = 'Sobrantes resta entre fisico y sap'

    categories_names = [category_1_name, category_2_name, category_3_name, category_4_name, category_5_name]

    total = 0
    summary = []
    for i in range(len(categories)):
        c = categories[i]
        name = categories_names[i]
        count = 0
        for x in c:
            count += x[1]
        summary.append([name, count])
        total += count
    summary.append(['Total general', total])

    return summary
