from collections import namedtuple

from xlrd import open_workbook

# from modules import paths


def read_base_pay(_, path="data/Datos Planilla Activos PB.xlsx"):  #
    _.log(f"Leyendo base pay...")
    with open_workbook(_.get_path(path)) as wb:
        for s in wb.sheets():
            base_pay = {}
            BasePay = namedtuple("BasePay", ["dni", "name", "pay"])
            for row in range(2, s.nrows):
                col_value = [s.cell(row, col).value for col in range(s.ncols)]
                if row == 2:
                    header = col_value
                    dni_index = header.index("DNI Nº")
                    name_index = header.index("APELLIDOS Y  NOMBRES")
                    base_pay_index = header.index("BASICO\nMENSUAL")
                    family_pay_index = header.index("ASIGN.\nFAMILIAR")
                else:
                    dni = col_value[dni_index]
                    if dni:
                        dni = int(dni)
                        name = col_value[name_index]
                        base = col_value[base_pay_index]
                        family_pay = col_value[family_pay_index]
                        if not base:
                            base = 0
                        else:
                            base = int(base)
                        if not family_pay:
                            family_pay = 0
                        pay = base + family_pay
                        base_pay[dni] = BasePay(dni, name, pay)
    return base_pay


def read_total_pay(_, path="data/Planilla Haberes Julio-2021 - Peru Brands.xlsx"):  #
    _.log(f"Leyendo total pay...")
    with open_workbook(_.get_path(path)) as wb:
        for s in wb.sheets():
            if s.name == "Planilla":
                total_pay = {}
                TotalPay = namedtuple("TotalPay", ["dni", "name", "pay"])
                for row in range(5, s.nrows):
                    col_value = [s.cell(row, col).value for col in range(s.ncols)]
                    if row == 5:
                        header = col_value
                        dni_index = header.index("DNI Nº")
                        name_index = header.index("APELLIDOS Y  NOMBRES")
                        total_pay_index = header.index("TOTAL\nINGRESOS\nAFECTOS")
                    else:
                        dni = col_value[dni_index]
                        if dni:
                            dni = int(dni)
                            name = col_value[name_index]
                            pay = col_value[total_pay_index]
                            total_pay[dni] = TotalPay(dni, name, pay)
    return total_pay


if __name__ == "__main__":
    pass
    read_base_pay()
    read_total_pay()
