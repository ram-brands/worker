from collections import namedtuple
from os import listdir

from xlrd import open_workbook

from . import paths


def read_sap(_, store, keyword=paths.SAP_KEYWORD):  # Read sap stock [[sku, stock]]
    _.log(f"Leyendo sap stock...")
    file_name = [
        f
        for f in listdir(_.get_path(f"data/{store}"))
        if ("~" not in f) and (keyword in f)
    ]
    if file_name:
        file_name = file_name[0]
    else:
        _.log(f"Incorrect format with store {store} and keyword {keyword}")
        raise FileNotFoundError
    wb = open_workbook(_.get_path(f"data/{store}/{file_name}"))
    for s in wb.sheets():
        data = {}
        Attribute = namedtuple("item", ["sku", "stock"])
        for row in range(s.nrows):
            col_value = []
            col_value = [s.cell(row, col).value for col in range(s.ncols)]
            if row == 0:
                header = col_value
                sku_index = col_value.index("ItemCode")
                stock_index = col_value.index("Stock")
            else:
                sku = col_value[sku_index]
                stock = col_value[stock_index]
                if sku:
                    if int(sku) in data:
                        data[int(sku)] += int(stock)
                    else:
                        data[int(sku)] = int(stock)
    return data


def read_physical(
    _, store, keyword=paths.PHYSICAL_KEYWORD
):  # Read sap stock [[sku, stock]]
    _.log(f"Leyendo stock físico...")
    file_name = [
        f
        for f in listdir(_.get_path(f"data/{store}"))
        if ("~" not in f) and (keyword in f)
    ]
    if file_name:
        file_name = file_name[0]
    else:
        _.log(f"Incorrect format with store {store} and keyword {keyword}")
        raise FileNotFoundError
    wb = open_workbook(_.get_path(f"data/{store}/{file_name}"))
    for s in wb.sheets():
        if True:
            data = {}
            Attribute = namedtuple("item", ["sku", "stock"])
            for row in range(s.nrows):
                col_value = []
                col_value = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 0:
                    header = col_value
                else:
                    for sku in col_value:
                        if sku:
                            if int(sku) in data:
                                data[int(sku)] += 1
                            else:
                                data[int(sku)] = 1
    return data


def get_all_stores(_, dir_name="data"):
    # _.log('Get all stores')
    # print('get all stores')
    # all_stores = listdir(_.get_path(dir_name))
    all_stores = [
        s for s in listdir(_.get_path(dir_name)) if ("~" not in s) and ("." not in s)
    ]
    # print(all_stores)
    _.log(all_stores)
    return all_stores
