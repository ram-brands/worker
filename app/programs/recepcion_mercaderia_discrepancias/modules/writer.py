import xlsxwriter


def write_excel(_, header, data, name="test"):
    # Create a workbook and add a worksheet.
    path = f'results/{name}.xlsx'
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
    _.log(f"Se creó el archivo {name}.xlsx exitosamente")


def write_csv(_, header, data, name="test"):
    header = ", ".join(header) + '\n'
    path = f'results/{name}.csv'
    _.makedirs(path)
    with open(_.get_path(path), 'w') as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + '\n')
    _.log(f"Se creó el archivo {name}.csv exitosamente")