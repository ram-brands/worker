from xlrd import open_workbook
from collections import namedtuple
from . import paths
import os


def read_(fs, path):  # read input
    print(f"Leyendo XXXX...")
    wb = open_workbook(fs.get_path(f"{path}"))
    for s in wb.sheets():
        data = {}
        Attribute = namedtuple("Attribute", [])
        for row in range(s.nrows):
            col_value = []
            col_value= [s.cell(row, col).value for col in range(s.ncols)]
            if row == 0:
                header = col_value
            else:
                pass

def read_csv(fs, path=paths.DATA):

    data = {}
    with open(fs.get_path(path), 'r') as f:
        for line in f:
            line = line.strip().split(',')
            tid = line[0]
            if tid != "TID":
                amount = int(line[1].replace('.', ''))
                data[tid] = amount

    files = os.listdir(fs.get_path(f"data"))
    if files:
        for f in files:
            os.remove(fs.get_path(f"data/{f}"))

    return data


if __name__ == "__main__":
    pass
    # data = read_csv()
    # print(data)
