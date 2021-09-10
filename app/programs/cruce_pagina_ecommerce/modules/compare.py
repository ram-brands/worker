from collections import namedtuple

from . import writer


def _filter(header, data):
    categories = {}
    pim_index = header.index("MOSTRAR EN TIENDA PIM")
    activate_index = header.index("_ActivateSkuIfPossible c")
    repeated_index = header.index("REPETIDOS")
    category_index = header.index("_CategoryName al")
    sap_stock_index = header.index("stock sap")
    available_qty_index = header.index("AvailableQuantity")
    style_color_index = header.index("Estilo-color")
    active2_index = header.index("_SkuIsActive (No es posible modificar)")
    show_index = header.index("_ShowOnSite")
    for line in data:
        if (
            float(line[pim_index])
            and int(line[repeated_index]) == 1
            and int(line[activate_index]) == 1
            and line[active2_index]
            and line[show_index]
        ):
            values = [
                line[style_color_index],
                int(line[available_qty_index]),
                int(line[sap_stock_index]),
            ]
            if line[category_index] not in categories:
                categories[line[category_index]] = [values]
            else:
                categories[line[category_index]].append(values)
    return categories


def compare_categories(categories):
    data = []
    for category in categories:
        values = [category, 0, 0]
        for line in categories[category]:
            values[1] += line[1]
            values[2] += line[2]
        data.append(values)
    return data


def compare_styles(categories):
    data = []
    for category in categories:
        for line in categories[category]:
            style = line[0]
            values = [category, style, line[1], line[2]]
            data.append(values)
    return data


def compare(fs, header, data):
    categories = _filter(header, data)
    data = compare_categories(categories)
    header = ["Category", "AvailableQty", "stock sap"]
    # write(header, data)
    writer.write_excel(fs, header, data, "categorias")

    data = compare_styles(categories)
    header = ["Category", "style-color", "AvailableQty", "stock sap"]
    # write(header, data, 'style.csv')
    writer.write_excel(fs, header, data, "estilo-color")


def write(fs, header, data, name="test.csv"):
    header = ", ".join(header) + "\n"

    path = f"results/{name}"
    fs.makedirs(path)

    with open(fs.get_path(path), "w") as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + "\n")
        print(f"Se creó el archivo {name} exitosamente")


if __name__ == "__main__":
    pass
