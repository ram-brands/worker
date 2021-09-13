from collections import namedtuple
from os import listdir
from os.path import isfile, join

from xlrd import open_workbook

from . import paths

# El único cambio es la clase, que se debe ir a buscar a parámetros,
# usando la columna en el archivo de compra que se llama PRODUCT SUBCLASS (columna E)
# a parámetros de la J a la L.


def read_data(_, format_header, path):  #
    print(f"Leyendo {path}")
    wb = open_workbook(_.get_path(f"{path}"))
    data = []
    header = None
    stores = []
    for s in wb.sheets():
        if s.name == "1. ARCHIVO COMPRA":
            # Attribute = namedtuple("Attribute", [])
            # final_header = ['PAÍS', 'EMPRESA', 'REF EMBARQUE', 'CANAL', 'NOMBRE DE TIENDAS', 'JERARQUIA', 'DEPARTAMENTO', 'CLASE', 'GENERO', 'MARCA', 'AÑO ON FLOOR', 'STYLE', 'DESPROD', 'TEMPORADA', 'AÑO TEMPORADA', 'DELIVERY', 'ON FLOOR ORIGINAL', 'ON FLOOR REAL', 'MES ONFLOOR REAL', 'PO#', 'UNIDADES', 'FOB USD']
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                # if row == 13:
                if row_values[0] == "STYLECOLOR":
                    header = row_values
                    if "Clase" in header:
                        header[header.index("Clase")] = "CLASE"
                else:
                    if header and row_values[0]:
                        data.append(row_values)
                        # if 'U0BG21K6YW1' in row_values:
                        #     print(row_values)
                    pass
    return header, data, stores


def read_parameters(_, path=paths.FORMAT_FILE):  # read parameters in sheet '3.PARAMETROS'
    print(f"Leyendo {path}")
    wb = open_workbook(_.get_path(f"{path}"))
    Parameters = namedtuple(
        "Parameters", ["subclass", "firstletter", "department", "store", "arrival"]
    )
    # parameters = {}
    for s in wb.sheets():
        if s.name == "3.PARAMETROS":
            # SubClass Parameters
            subclass = {}
            start_index = 9
            length = 4
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 1:
                    header = row_values
                else:
                    if row_values[start_index]:
                        subclass[row_values[start_index]] = row_values[
                            start_index + 1 : start_index + length
                        ]

            # FirstLetter Parameters
            firstletter = {}
            start_index = 14
            length = 4
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 1:
                    header = row_values
                else:
                    if row_values[start_index]:
                        firstletter[
                            str(row_values[start_index]).replace(".0", "")
                        ] = row_values[start_index + 1 : start_index + length]

            # Department Parameters
            department = {}
            start_index = 19
            length = 2
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 1:
                    header = row_values
                else:
                    if row_values[start_index]:
                        department[row_values[start_index]] = row_values[
                            start_index + 1 : start_index + length
                        ]

            # Store Parameters
            store = {}
            start_index = 22
            length = 3
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 1:
                    header = row_values
                else:
                    if row_values[start_index]:
                        store[row_values[start_index]] = row_values[
                            start_index + 1 : start_index + length
                        ]

            # # ChilePrice Parameters
            # chile_price = {}
            # start_index = 27
            # length = 2
            # for row in range(s.nrows):
            #     row_values = []
            #     row_values = [s.cell(row, col).value for col in range(s.ncols)]
            #     if row == 1:
            #         header = row_values
            #     else:
            #         print(row_values)
            #         if row_values[start_index] and row > 2:
            #             chile_price[row_values[start_index]] = row_values[start_index + 1:start_index + length]
            # print(chile_price)

            # Arrival Parameters
            arrival = {}
            start_index = 32
            length = 5
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 1:
                    header = row_values
                else:
                    if row_values[start_index]:
                        key = (row_values[start_index], row_values[start_index + 1])
                        arrival[key] = row_values[start_index + 2 : start_index + length]

    parameters = Parameters(subclass, firstletter, department, store, arrival)
    return parameters


def read_origin_header(_, path=paths.FORMAT_FILE):  #
    print(f"Leyendo {path}")
    wb = open_workbook(_.get_path(f"{path}"))
    for s in wb.sheets():
        if s.name == "1. ARCHIVO COMPRA":
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 13:
                    header = row_values[:43]
                    break
    return header


def read_final_header(_, path=paths.FORMAT_FILE):  #
    print(f"Leyendo {path}")
    wb = open_workbook(_.get_path(f"{path}"))
    for s in wb.sheets():
        if s.name == "2. CONTROL COMPRA":
            for row in range(s.nrows):
                row_values = []
                row_values = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 10:
                    header = row_values[2:]
                    break
    return header


def consolidate_data(
    _, origin_header, dir_name="data"
):  # consolidate all files in dir if format fits
    # dir_ = _.get_path(dir_name)
    # for f in listdir(_.get_path(dir_)):
    #     print(f) (isfile(join(dir_, f))) and
    files = [f for f in listdir(_.get_path(dir_name)) if ("~" not in f) and (".xls" in f)]
    data = []
    stores = None
    x = 0
    c = []
    format_error = set()
    header = None
    File = namedtuple("File", ["header", "data", "path"])
    for f in files:

        h, partial_data, s = read_data(_, origin_header, f"{dir_name}/{f}")
        required_values = [
            "STYLE",
            "COLOR",
            "DESCRIPTION",
            "TEMPORADA",
            "AÑO",
            "DEL",
            "DELIVERY (MES)",
            "PRE-COSTING",
            "LLEGADA",
            "PRODUCT SUBCLASS",
            "PO#",
            "CLASE",
        ]
        required_stores = [
            "PARQUE ARAUCO",
            "COSTANERA MALL",
            "ANTOFAGASTA",
            "ALTO LAS CONDES",
            "PLAZA EGAÑA",
            "PLAZA VESPUCIO",
            "PLAZA TREBOL",
            "LOS DOMINICOS",
            "ESTADO",
            "MARINA ARAUCO",
            "E- COMM CL",
            "FACTORY II",
            "FACTORY III",
            "LA POLAR",
            "MULTICENTRO",
            "FALABELLA",
            "MIYAKI",
            "MEGAPLAZA",
            "FAUCET",
            "SALAVERRY",
            "Larcomar",
            "San Miguel",
            "Jockey Plaza",
            "E- COMM PE",
        ]
        # if h and (required_values <= h) and (required_stores <= h):
        if (
            h
            and all(elem in h for elem in required_values)
            and all(elem in h for elem in required_stores)
        ):

            x += 1
            c.append(f)
            # if header:
            # data += partial_data
            stores = s
            header = h.copy()
            # print(f)
            File_ = File(header, partial_data, f)
            data.append(File_)
        else:
            format_error.add(f)

    # print(f'stores: {stores}, {x}')
    # print(f'c: {c}')
    if format_error:
        print("ERROR: Los siguientes archivos tienen error de formato:")
        for e in format_error:
            print(e)
    return header, data, required_stores


if __name__ == "__main__":
    pass
    # path = 'data/MN HO21 (PS22) MARKET ORDER CHART.xlsx'
    path = "data/format/formato.xlsx"
    # data = read_(path)
    header = read_origin_header(path)
    # p = read_parameters(path)
    # print(p.subclass)
    # print(data)
    # consolidate_data()
