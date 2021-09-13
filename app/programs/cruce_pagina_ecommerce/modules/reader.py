import os
import sys
from collections import namedtuple
from status import Status
from xlrd import open_workbook

from . import paths

##########################################################################
# UC (unique_code) = warehouse-sku
# SC = estilo-color
##########################################################################


def get_file_name(_, key_word):
    all_files = os.listdir(_.get_path("data/"))
    all_files = [x for x in all_files if "$" not in x]
    file_ = None
    for f in all_files:
        if key_word in f:
            file_ = f
            return file_
    if not file_:
        _.warning(f"ERROR: No hay archivo con palabra clave {key_word}")
        _.status = Status.CLIENT_ERROR
        exit()


def read_stock(_, path=paths.STOCK):  # Leer BBDD de peso y vol por sku
    file_ = get_file_name(_, path)
    _.log(f"Leyendo Inventario...")
    wb = open_workbook(_.get_path(f"data/{file_}"))
    for s in wb.sheets():
        unique_code_stock = {}
        unique_codes = []
        Attribute = namedtuple("Attribute", ["warehouse", "sku"])
        for row in range(s.nrows):
            col_value = []
            # for col in range(s.ncols):

            #     value = (s.cell(row, col).value)
            #     col_value.append(value)
            col_value = [s.cell(row, col).value for col in range(s.ncols)]
            if row == 0:
                header = col_value
                warehouse_index = header.index("WhsCode")
                sku_index = header.index("ItemCode")
                stock_index = header.index("Stock")
            else:
                warehouse = col_value[warehouse_index]
                sku = str(col_value[sku_index]).replace(".0", "")
                stock = col_value[stock_index]
                key = f"{warehouse}-{sku}"
                unique_code_stock[key] = stock
                # unique_codes.append([key])
    # print(unique_code_stock)
    # print(unique_codes)
    return unique_code_stock


def read_maestro(_, path=paths.MAESTRO):  # Leer Maestro para obtener {estilo-color: sku}
    file_ = get_file_name(_, path)
    if ".txt" in file_:
        maestro = read_maestro_txt(_, file_)
    else:
        _.log(f"Leyendo Maestro...")
        wb = open_workbook(_.get_path(f"data/{file_}"))
        for s in wb.sheets():
            style_color = set()
            maestro = {}
            # Attribute = namedtuple("Attribute", ['style', 'color'])
            for row in range(s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    header = col_value
                    style_index = header.index("Style")
                    color_index = header.index("Color")
                    sku_index = header.index("Número de artículo")
                else:
                    style = str(col_value[style_index]).replace(".0", "")
                    color = str(col_value[color_index]).replace(".0", "")
                    sku = str(col_value[sku_index]).replace(".0", "")
                    SC = f"{style}-{color}"
                    maestro[sku] = SC
                    style_color.add(SC)
        # print(data)
        style_color = list(style_color)
        # print(style_color)
    return maestro


def read_maestro_txt(_, path):  # Leer Maestro para obtener {estilo-color: sku}
    _.log(f"Leyendo Maestro txt...")
    with open(_.get_path(path), "r", encoding="utf16", errors="ignore") as f:
        # contents = f.read()
        # contents = contents.decode('utf-16', 'ignore')
        style_color = set()
        maestro = {}
        header = None
        for row in f:
            line = row.strip().split("\t")

            Attribute = namedtuple("Attribute", ["style", "color"])
            if not header:
                header = line
                style_index = header.index("Style")
                color_index = header.index("Color")
                sku_index = header.index("Número de artículo")
            else:
                style = str(line[style_index]).replace(".0", "")
                color = str(line[color_index]).replace(".0", "")
                sku = str(line[sku_index]).replace(".0", "")
                SC = f"{style}-{color}"
                # print(sku)
                # print(color)
                # exit()
                maestro[sku] = SC
                style_color.add(SC)
    # print(data)
    style_color = list(style_color)
    # print(style_color)
    return maestro


def read_estoque(
    _, path=paths.ESTOQUE
):  # Consolidar estoque con saldo mayor a 0, {UC:stock}
    file_ = get_file_name(_, path)
    _.log(f"Leyendo Estoque...")
    wb = open_workbook(_.get_path(f"data/{file_}"))
    estoque = {}
    for s in wb.sheets():
        # print(f'Leyendo {s.name}')
        # Attribute = namedtuple("Attribute", ['warehouse', 'sku'])
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = s.cell(row, col).value
                col_value.append(value)
            if row == 0:
                header = col_value
                warehouse_index = header.index("WarehouseId")
                sku_index = header.index("RefId")
                stock_index = header.index("AvailableQuantity")
            else:
                warehouse = col_value[warehouse_index]
                sku = str(col_value[sku_index]).replace(".0", "")
                stock = col_value[stock_index]
                if stock > 0:
                    key = f"{warehouse}-{sku}"
                    estoque[key] = stock
    return estoque


def read_exportacion(_, path=paths.EXPORTACION):  # Obtner {sku: pim}
    file_ = get_file_name(_, path)
    _.log(f"Leyendo Exportacion...")
    wb = open_workbook(_.get_path(f"data/{file_}"))
    exportacion = {}
    for s in wb.sheets():
        # Attribute = namedtuple("Attribute", ['warehouse', 'sku'])
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = s.cell(row, col).value
                col_value.append(value)
            if row == 0:
                header = col_value
                sku_index = header.index("Sku Codigo")
                pim_index = header.index("Producto Mostrar Producto Tienda")
            else:
                sku = str(col_value[sku_index]).replace(".0", "")
                pim = col_value[pim_index]
                exportacion[sku] = pim
    # print(data)
    # print(len(data))
    # print(unique_codes)
    return exportacion


def read_atrapero(_, path=paths.ATRAPERO):  # Obtener si sku esta prendido
    file_ = get_file_name(_, path)
    _.log(f"Leyendo atrapero...")
    wb = open_workbook(_.get_path(f"data/{file_}"))
    atrapero = {}
    for s in wb.sheets():
        # print(f'Leyendo {s.name}')
        Attribute = namedtuple("Attribute", ["active", "active2", "show", "category"])
        for row in range(s.nrows):
            col_value = []
            for col in range(s.ncols):
                value = s.cell(row, col).value
                col_value.append(value)
            if row == 0:
                header = col_value
                sku_index = header.index("_SkuEan")
                active_index = header.index("_ActivateSkuIfPossible")
                category_index = header.index("_CategoryName")
                active2_index = header.index("_SkuIsActive (No es posible modificar)")
                show_index = header.index("_ShowOnSite")
            else:
                sku = str(col_value[sku_index]).replace(".0", "")
                active = col_value[active_index]
                active2 = col_value[active2_index]
                show = col_value[show_index]
                category = col_value[category_index]
                if active == "SÍ":
                    active = 1
                else:
                    active = 0
                if active2 == "SÍ":
                    active2 = 1
                else:
                    active2 = 0
                if show == "SÍ":
                    show = 1
                else:
                    show = 0
                attribute = Attribute(active, active2, show, category)
                atrapero[sku] = attribute
    return atrapero


if __name__ == "__main__":
    pass
    # read_maestro_txt()
    # read_maestro()
    # read_stock()
