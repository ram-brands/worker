import xlsxwriter


def write_excel(fs, header, data, name="test"):
    # Create a workbook and add a worksheet.
    path = f"results/{name}.xlsx"
    fs.makedirs(path)
    workbook = xlsxwriter.Workbook(fs.get_path(path))
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
    print(f"Se creó el archivo {name}.xlsx exitosamente")


def write_csv(fs, header, data, name="test.csv"):
    config_path = 'results'
    header = ", ".join(header) + '\n'

    path = f"results/{name}"
    fs.makedirs(path)

    with open(fs.get_path(path), "w") as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + '\n')
        print(f"Se creó el archivo {name} exitosamente")