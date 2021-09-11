import csv
import time
from collections import namedtuple
from datetime import datetime

import xlsxwriter
from dateutil.relativedelta import relativedelta
from xlrd import open_workbook


def read_PVD(_, path):  # Leer Proceso Ventas Diarias
    print(f"Leyendo Proceso Venta Diarias...")
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "ProcesoVentasDiarias":
            data = []
            for row in range(1, s.nrows):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 1:
                    header = col_value
                    fecha_index = header.index("Fecha")
                    fecha_con_index = header.index("FechaCon")
                    antiguedad_index = header.index("Antiguedad")
                else:
                    for f in [fecha_con_index, fecha_con_index, antiguedad_index]:
                        serial = str(col_value[f])
                        if serial and "/" not in serial:
                            # print(serial)
                            fecha = datetime.utcfromtimestamp(
                                (float(serial) - 25569) * 86400.0
                            )
                            fecha = f"{fecha.month}/{fecha.day}/{fecha.year}"
                            col_value[f] = fecha
                    # col_value = [str(i) for i in col_value]
                    data.append(col_value)
    return header, data


def read_param(_, path):  # Leer parametros
    print(f"Leyendo Parametros...")
    P = namedtuple(
        "Parameters",
        [
            "llave_emp",
            "empresas",
            "temporada",
            "genero",
            "descripcion",
            "pais",
            "marca2",
            "descripcionC",
            "tiendas",
            "tipo_cambio",
            "tipo_doc",
        ],
    )
    empresa_dict = {}
    llave_emp_dict = {}
    temporada_dict = {}
    genero_dict = {}
    descripcion_dict = {}
    pais_dict = {}
    marca2_dict = {}
    descripcionC_dict = {}
    tiendas_dict = {}
    tipo_cambio_dict = {}
    tipo_doc_dict = {}
    wb = open_workbook(_.get_path(path))
    for s in wb.sheets():
        if s.name == "Hoja1":
            data = []
            # if True:
            for row in range(0, s.nrows):
                # for row in range(1, 15):
                col_value = []
                for col in range(s.ncols):
                    value = s.cell(row, col).value
                    col_value.append(value)
                if row == 0:
                    row += 1
                    header = col_value
                    header[0] = header[0].replace("\ufeff", "")
                    empresa_index = header.index("Empresa Sistema")
                    temporada_index = header.index("Temporada")
                    genero_index = header.index("Género")
                    llave_emp_index = header.index("Llave Emp CC")
                    pais_corr_index = header.index("País Corr")
                    marca2_index = header.index("Marca2")
                    descripcionC_index = header.index("DescripcionCCosto/DesBode")
                    tienda_index = header.index("Nombre Tienda Corregido")
                    tipo_cambio_index = header.index("Mes")
                    tipo_doc_index = header.index("TipoDocto")

                else:
                    if col_value[empresa_index]:
                        empresa_dict[col_value[empresa_index]] = [
                            col_value[empresa_index + 1],
                            col_value[empresa_index + 2],
                            col_value[empresa_index + 3],
                        ]
                    if col_value[llave_emp_index]:
                        llave_emp_dict[col_value[llave_emp_index]] = col_value[
                            llave_emp_index : llave_emp_index + 6
                        ]
                    if col_value[temporada_index]:
                        temporada_dict[col_value[temporada_index]] = col_value[
                            temporada_index + 1
                        ]
                    if col_value[genero_index]:
                        genero_dict[col_value[genero_index]] = col_value[genero_index + 1]
                    if col_value[pais_corr_index]:
                        pais_dict[col_value[pais_corr_index - 1]] = col_value[
                            pais_corr_index
                        ]
                    if col_value[marca2_index]:
                        marca2_dict[col_value[marca2_index]] = col_value[marca2_index + 1]
                    if col_value[descripcionC_index]:
                        descripcionC_dict[
                            col_value[descripcionC_index].upper()
                        ] = col_value[descripcionC_index + 1 : descripcionC_index + 4]
                    if col_value[tienda_index]:
                        tiendas_dict[col_value[tienda_index]] = col_value[
                            tienda_index + 1 : tienda_index + 3
                        ]
                    if col_value[tipo_cambio_index]:
                        key = col_value[tipo_cambio_index]
                        fecha = datetime.utcfromtimestamp((float(key) - 25569) * 86400.0)
                        key = f"{fecha.month}/{fecha.day}/{fecha.year}"
                        tipo_cambio_dict[key] = col_value[
                            tipo_cambio_index + 1 : tipo_cambio_index + 3
                        ]
                    if col_value[tipo_doc_index]:
                        tipo_doc_dict[col_value[tipo_doc_index].upper()] = col_value[
                            tipo_doc_index + 1
                        ]
    param = P(
        llave_emp_dict,
        empresa_dict,
        temporada_dict,
        genero_dict,
        descripcion_dict,
        pais_dict,
        marca2_dict,
        descripcionC_dict,
        tiendas_dict,
        tipo_cambio_dict,
        tipo_doc_dict,
    )
    # print(param.tiendas)
    # exit()
    return param


def create_macro(header1, data, param):  # realizar el trabajo de la macro
    print(f"Creando macro...")
    # header1 = input header  |  header2 = output header
    header2 = "Key 1	Empresa	DocEntry	ObjType	Tipo	Fecha	Día	Mes	Año	DesBode	Nombre de Tienda	Folio	CodCaja	Canal	CodProd	DesProd	Descripcion Grupo	SubGrupo	Jerarquia	Departamento	Clase	SubClase	Cantidad	Venta Neta	Costo Unitario	Dcto aplicado	Genero	Desc Genero	Temporada	Desc Temp	Año Temporada	Temp / Año	Mes Temporada	Style	Color	Talla	Delivery	Número Semana	CodVendedor	Nombre Vendedor	Stock	Antiguedad	Marca	LP2	Hora Venta	Column1	Costo de Venta	Contrib	Margen	Nombre cliente	Rut	CCosto	Moneda	Pais	DescripcionCCosto	Marca Corr	FOB	NombrePromo	PorcentajePromo	Redondeo Descuento	Tipo de Promociones	VendedorPromo	ValorPromo	UsuarioSAP	TipoCambio	FechaCon	REFEMB	PROV	TipoDocto	Precio Venta Full	Stock al Costo	Venta Pesos	Costo Pesos	Contrib Pesos	Stock PVP	Id Q	Id $	Id C$	Compara"
    header2 = header2.split("\t")
    new_data = []
    error_keys_canal = set()
    error_keys_temporada = set()
    error_keys_genero = set()
    error_keys_llave_emp = set()

    # Indices de columnas a calcular o parametrizar
    empresa_index = header1.index("Empresa")
    descripcion_index = header1.index("DescripcionCCosto")
    marca2_index = header1.index("Marca2")
    canal_index = header2.index("Canal")
    fecha_index = header2.index("Fecha")
    temporada_index = header2.index("Desc Temp")
    genero_index = header2.index("Genero")
    ano_temp_index = header2.index("Temp / Año")
    tipo_index = header2.index("Tipo")
    costo_venta_index = header2.index("Costo de Venta")
    cantidad_index = header2.index("Cantidad")
    costo_unitario_index = header2.index("Costo Unitario")
    obj_type_index = header2.index("ObjType")
    venta_neta_index = header2.index("Venta Neta")
    contrib_index = header2.index("Contrib")
    margen_index = header2.index("Margen")
    pais_index = header2.index("Pais")
    marca_corr_index = header2.index("Marca Corr")
    porcentaje_promo_index = header2.index("PorcentajePromo")
    redondeo_index = header2.index("Redondeo Descuento")
    precio_venta_full_index = header2.index("Precio Venta Full")
    lp2_index = header2.index("LP2")
    stock_costo_index = header2.index("Stock al Costo")
    stock_index = header2.index("Stock")
    stock_pvp_index = header2.index("Stock PVP")
    id_q_index = header2.index("Id Q")
    compara_index = header2.index("Compara")
    nombre_tienda_index = header2.index("Nombre de Tienda")
    desbode_index = header1.index("DesBode")
    jerarquia_index = header2.index("Jerarquia")
    departamento_index = header2.index("Departamento")
    key_index = header2.index("Key 1")
    venta_pesos_index = header2.index("Venta Pesos")
    costo_pesos_index = header2.index("Costo Pesos")
    contrib_pesos_index = header2.index("Contrib Pesos")
    tipo_doc_index = header2.index("TipoDocto")
    doc_entry_index = header2.index("DocEntry")

    # Revisar columnas con mismos nombres
    keys = []
    for key in header2:
        if key in header1:
            index = header1.index(key)
        else:
            index = None
        keys.append(index)
    for line in data:
        new_line = []
        # Para columnas con index (mismo nombre en ambos headers)
        for key in keys:
            if key:
                new_line.append(line[key])
            else:
                new_line.append("")

        # Para hacer relaciones de columnasc con distintos nombres | pairs: (input header, output header)
        pairs = [
            ("CantFacturada", "Cantidad"),
            ("Anio", "Año Temporada"),
            ("Semana", "Número Semana"),
            ("Marca2", "Marca Corr"),
            ("Total Final", "Venta Neta"),
            ("Costo Rep", "Costo Unitario"),
            ("HoraVentaRetail", "Hora Venta"),
        ]

        for pair in pairs:
            input_index = header1.index(pair[0])
            output_index = header2.index(pair[1])
            input_value = line[input_index]
            new_line[output_index] = input_value

        # Manejo de formato fecha
        meses = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }
        fecha = new_line[fecha_index]
        fecha = datetime.utcfromtimestamp((float(fecha) - 25569) * 86400.0)
        full_fecha = "{:02d}/{:02d}/{:4d}".format(fecha.month, fecha.day, fecha.year)
        fecha = f"{fecha.month}/{fecha.day}/{fecha.year}"
        fecha = datetime.strptime(fecha, "%m/%d/%Y")
        new_line[header2.index("Día")] = fecha.day
        new_line[header2.index("Mes")] = meses[fecha.month]
        new_line[header2.index("Año")] = fecha.year

        # NOMRBE TIENDA
        tipo = new_line[tipo_index]
        if tipo == "Venta":
            descripcion = line[descripcion_index].upper()
            if descripcion:
                if "GUESS JEANS TR?BOL" == descripcion:
                    descripcion = "GUESS JEANS TREBOL"
                if "SAGA FALABELLA GUESS PER?" == descripcion:
                    descripcion = "SAGA FALABELLA GUESS PERÚ"
                tienda = param.descripcionC[descripcion][0]
            else:
                print("ALERTA: Tipo VENTA sin DescripciónCCosto")
                tienda = "S/I"
        else:
            desbode = line[desbode_index].upper()
            if desbode:
                if "CENTRO DE DISTRIBUCI?N KERRY" == desbode:
                    desbode = "CENTRO DE DISTRIBUCIÓN KERRY"
                if "GUESS JEANS TR?BOL" == desbode:
                    desbode = "GUESS JEANS TREBOL"
                tienda = param.descripcionC[desbode][0]
            else:
                print("ALERTA: Tipo STOCK sin DesBode")
                tienda = "S/I"
        # CANAL
        if tienda == "S/I":
            canal = "S/I"
        else:
            canal = param.tiendas[tienda][0]

        new_line[canal_index] = canal
        new_line[nombre_tienda_index] = tienda

        # Reemplazo de valores que no necesitan parametros
        # empresa = line[0]
        empresa = line[empresa_index]
        if empresa in param.empresas:
            empresa = param.empresas[empresa][0]
        descripcion = line[descripcion_index]
        temporada = new_line[header2.index("Temporada")]
        a_t = new_line[header2.index("Año Temporada")]
        genero = new_line[genero_index].upper()
        ano_temp = str(temporada) + str(a_t).replace(".0", "")
        tipo = new_line[tipo_index]
        pais = param.pais[new_line[pais_index]]
        jerarquia = new_line[jerarquia_index]
        departamento = new_line[departamento_index]

        key = pais + empresa + canal + tienda + jerarquia + departamento
        new_line[key_index] = key.upper()
        new_line[1] = empresa
        new_line[ano_temp_index] = ano_temp

        # Formulas
        doc_entry = new_line[doc_entry_index]
        obj_type = str(new_line[obj_type_index]).replace(".0", "")
        venta_neta = float(new_line[venta_neta_index])
        lp2 = float(new_line[lp2_index])
        stock = float(new_line[stock_index])
        costo_unitario = float(new_line[costo_unitario_index])
        cantidad = float(new_line[cantidad_index])
        costo_venta = cantidad * costo_unitario
        # costo_unitario = 0
        contrib = 0
        precio_venta_full = 0
        if tipo == "Venta":
            precio_venta_full = round(cantidad * lp2, 2)
            if not precio_venta_full:
                precio_venta_full = 0
            if obj_type == "14":
                contrib = round(costo_venta + venta_neta, 2)
            elif obj_type == "13":
                contrib = round(venta_neta - costo_venta, 2)
            else:
                print(f"ALERTA: Obj Type extraño: {obj_type}")

            stock_costo = 0
            stock_pvp = 0
        else:
            stock_costo = stock * costo_unitario
            stock_pvp = stock * lp2
            if pais in ["Perú"]:
                stock_pvp = stock_pvp / 1.18
            elif pais in ["Chile", "Panamá"]:
                stock_pvp = stock_pvp / 1.19
            else:
                print(f"ALERTA: País no reconocido: {pais}")
        if venta_neta:
            margen = str(round((contrib / venta_neta) * 100)) + "%"
        else:
            margen = ""
        new_line[costo_venta_index] = costo_venta
        new_line[contrib_index] = contrib
        new_line[margen_index] = margen
        new_line[marca_corr_index] = param.marca2[line[marca2_index]]
        new_line[precio_venta_full_index] = precio_venta_full
        new_line[stock_costo_index] = stock_costo
        new_line[stock_pvp_index] = round(stock_pvp, 2)

        porcentaje_promo = new_line[porcentaje_promo_index]
        if porcentaje_promo != "":
            redondeo = int(round(float(porcentaje_promo), -1))
        else:
            redondeo = 0
        new_line[redondeo_index] = redondeo

        iq_value = f"R {fecha.year} - {str(fecha.month).zfill(2)}"
        new_line[id_q_index] = iq_value + "Q"
        new_line[id_q_index + 1] = iq_value + "$"
        new_line[id_q_index + 2] = iq_value + "C$"

        # Tipo de promo
        nombre_promo = new_line[header2.index("NombrePromo")]
        tipo_promocion_index = header2.index("Tipo de Promociones")
        if tipo == "Stock":
            tipo_promocion = ""
            # test_nombre = param.descripcion[nomre]
        elif nombre_promo == "":
            tipo_promocion = "Sin promoción"
        elif nombre_promo in ["NODISC", "NODICS", "SYS:0"]:
            tipo_promocion = "Descuento Manual"
        elif nombre_promo not in ["", "NODISC", "NODICS"]:
            tipo_promocion = "Promociones"
        else:
            tipo_promocion = 0
        new_line[tipo_promocion_index] = tipo_promocion

        # Venta Pesos / costo pesos / contrib pesos
        fecha = new_line[fecha_index]
        fecha = datetime.utcfromtimestamp((float(fecha) - 25569) * 86400.0)
        fecha = f"{fecha.month}/{fecha.day}/{fecha.year}"
        fecha = datetime.strptime(fecha, "%m/%d/%Y")

        ultimo_dia_mes = fecha + relativedelta(day=31)
        ultimo_dia_mes = (
            f"{ultimo_dia_mes.month}/{ultimo_dia_mes.day}/{ultimo_dia_mes.year}"
        )
        # ultimo_dia_mes = "{:02d}/{:02d}/{:4d}".format(ultimo_dia_mes.month, ultimo_dia_mes.day, ultimo_dia_mes.year)
        # print(param.tipo_cambio)
        cambio = param.tipo_cambio[ultimo_dia_mes]

        # print(cambio)
        if tipo == "Venta":
            if pais == "Perú":
                venta_pesos = (venta_neta / float(cambio[1])) * float(cambio[0])
                costo_pesos = (costo_venta / float(cambio[1])) * float(cambio[0])
                contrib_pesos = (contrib / float(cambio[1])) * float(cambio[0])
            elif pais == "Panamá":
                venta_pesos = venta_neta * float(cambio[0])
                costo_pesos = costo_venta * float(cambio[0])
                contrib_pesos = contrib * float(cambio[0])
            else:
                venta_pesos = venta_neta
                costo_pesos = costo_venta
                contrib_pesos = contrib
            new_line[venta_pesos_index] = round(venta_pesos, 2)
            new_line[costo_pesos_index] = round(costo_pesos, 2)
            new_line[contrib_pesos_index] = round(contrib_pesos, 2)
        else:
            new_line[venta_pesos_index] = ""
            new_line[costo_pesos_index] = ""
            new_line[contrib_pesos_index] = ""

        # Para sacar valores de parametros
        # tienda = tienda.replace('?','ó')
        try:
            new_line[compara_index] = param.tiendas[tienda][1]
        except KeyError:
            if tienda == "":
                new_line[compara_index] = ""
            elif tipo == "venta":
                new_line[compara_index] = param.tiendas[tienda][1]
        try:
            new_line[temporada_index] = param.temporada[temporada]
        except KeyError:
            if temporada == "XX":
                new_line[temporada_index] = ""
            else:
                error_keys_temporada.add(temporada)
        try:
            new_line[genero_index + 1] = param.genero[genero]
            new_line[key_index] += param.genero[genero].upper()
        except KeyError:
            error_keys_genero.add(genero)
        pais = new_line[pais_index]
        new_line[pais_index] = param.pais[pais]
        tipo_doc = new_line[tipo_doc_index].upper()
        new_line[tipo_doc_index] = param.tipo_doc[tipo_doc]

        new_data.append(new_line)

        # Arreglar formato fechas
        fecha = new_line[fecha_index]
        fecha = datetime.utcfromtimestamp((float(fecha) - 25569) * 86400.0)
        fecha = f"{fecha.month}/{fecha.day}/{fecha.year}"
        fecha = datetime.strptime(fecha, "%m/%d/%Y")
        new_line[fecha_index] = f"{fecha.day:02}/{fecha.month:02}/{fecha.year}"
        # new_line[fecha_index] = "{:02d}/{:02d}/{:4d}".format(fecha.month, fecha.day, fecha.year)
        fecha2_index = header2.index("FechaCon")
        fecha2 = new_line[fecha2_index]
        # print(fecha2)
        if fecha2:
            # year = fecha2[-2:]
            # fecha2 = fecha2[:-2] + '20' + year  # Revisar esto, para formato de año entero
            fecha2 = datetime.strptime(fecha2, "%m/%d/%Y")
            new_line[fecha2_index] = f"{fecha2.day:02}/{fecha2.month:02}/{fecha2.year}"
            # new_line[fecha2_index] = "{:02d}/{:02d}/{:4d}".format(fecha2.month, fecha2.day, fecha2.year)
        fecha3_index = header2.index("Antiguedad")
        fecha3 = new_line[fecha3_index]
        if fecha3:
            # year = fecha3[-2:]
            # fecha3 = fecha3[:-2] + '20' + year  # Revisar esto, para formato de año entero
            fecha3 = datetime.strptime(fecha3, "%m/%d/%Y")
            new_line[fecha3_index] = f"{fecha3.day:02}/{fecha3.month:02}/{fecha3.year}"
            # new_line[fecha3_index] = "{:02d}/{:02d}/{:4d}".format(fecha3.month, fecha3.day, fecha3.year)

        # Arreglar formato de numeros
        for col in [
            "Venta Neta",
            "Costo Unitario",
            "Costo de Venta",
            "Contrib",
            "Venta Pesos",
            "Costo Pesos",
            "Contrib Pesos",
        ]:
            col_index = header2.index(col)
            # print(new_line[col_index])
            # value = str(new_line[col_index])
            value = new_line[col_index]
            # print(value)
            # new_line[col_index] = value.replace('.', ',')
            new_line[col_index] = value
            # print(new_line[col_index])
        # exit()

    # Ver si hay errores de llaves para parametros
    if error_keys_canal or error_keys_genero or error_keys_temporada:
        print("ERROR: Revisar llaves.")
    if error_keys_canal:
        print(f"CANAL: {error_keys_canal}")
    if error_keys_temporada:
        print(f"TEMPORADA: {error_keys_temporada}")
    if error_keys_genero:
        print(f"GENERO: {error_keys_genero}")
    if error_keys_llave_emp:
        print(f"LLAVE EMP: {error_keys_llave_emp}")

    # for line in new_data:
    #     for col in range(len(line)):
    #         try:
    #             value = float(line[col])
    #             print(line[col])
    #             print(value)
    #             exit()
    #         except ValueError:
    #             value = line[col]
    return header2, new_data


def write(
    _, header, data, name="out", limit=None
):  # Crear csv para poder copiar en matriz
    print(f"Escribiendo resultados...")
    # header = ','.join(header)
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y %H-%M")
    name += f" {dt_string}"
    write_excel(_, header, data, name)
    print(f"Se creó con éxito el archivo {name}.xlsx")
    print("*" * 50, "\n")


def write_excel(_, header, data, name):
    # Create a workbook and add a worksheet.
    path = f"results/{name}.xlsx"
    _.makedirs(path)
    workbook = xlsxwriter.Workbook(_.get_path(path))
    worksheet = workbook.add_worksheet()
    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0
    # write header
    for pos in range(len(header)):
        worksheet.write(row, pos, header[pos])
    row += 1
    # Iterate over the data and write it out row by row.
    for line in data:
        for col in range(len(line)):
            worksheet.write(row, col, line[col])
        row += 1

    workbook.close()


if __name__ == "__main__":
    pass
