from collections import namedtuple
from os import listdir

from xlrd import open_workbook

from status import Status

from . import paths


# Read all files in dir data
def read_all_files(_, dir_=paths.DIR):
    files = [f for f in listdir(_.get_path(dir_)) if ".txt" in f]
    data = []
    for f in files:
        d = read_asn(_, f)
        data.append(d)
    return data
  

def read_asn(_, f):  # Read asn
    _.log(f"Leyendo {f}...")
    Asn = namedtuple("ASN", ["details", "faltantes", "sobrantes"])
    with open(_.get_path(f"{paths.DIR}/{f}"), "r") as file:
        data = []
        for line in file:
            line = line.strip()
            # print(line)
            data.append(line)
    details = get_details(data)
    faltantes = get_faltantes(data)
    sobrantes = get_sobrantes(data)
    return Asn(details, faltantes, sobrantes)


# Get all details for order
def get_details(data):
    for line in data:
        if "ASN Revisado" in line:
            asn_code = line.replace("ASN Revisado: ", "")
        elif "Tracking Revisado" in line:
            tracking_code = line.replace("Tracking Revisado: ", "")
        elif "Voucher Revisado" in line:
            voucher_code = line.replace("Voucher Revisado: ", "")
        elif "Fecha de revisión del ASN: " in line:
            date = line.replace("Fecha de revisión del ASN: ", "")
        elif "Hora de revisión del ASN: " in line:
            time = line.replace("Hora de revisión del ASN: ", "")
        elif "Tienda" in line:
            store = line.replace("Tienda: ", "")
    Details = namedtuple(
        "Details", ["asn_code", "tracking_code", "voucher_code", "date", "time", "store"]
    )
    return Details(asn_code, tracking_code, voucher_code, date, time, store)


# Get Faltantes if there are any
def get_faltantes(data):
    if "******** No se presentan Faltantes *********" in data:
        return []
    faltantes = []
    start = data.index("**** Detalle de Faltantes en Recepcion *****")
    for line in data[start + 2 :]:
        if "******* Fin del detalle de Faltantes *******" in line:
            return faltantes
        faltantes.append(line.split("\t"))


# Get Sobrantes if there are any
def get_sobrantes(data):
    if "******** No se presentan Sobrantes *********" in data:
        return []
    sobrantes = []
    start = data.index("**** Detalle de Sobrantes en Recepcion *****")
    for line in data[start + 2 :]:
        if "******* Fin del detalle de Sobrantes *******" in line:
            return sobrantes
        sobrantes.append(line.split("\t"))
