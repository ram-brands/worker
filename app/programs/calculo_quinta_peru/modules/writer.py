import xlsxwriter


def write_excel(header, data, name="test"):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(f"results/{name}.xlsx")
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


def write_csv(header, data, name="test.csv"):
    header = ", ".join(header) + "\n"
    with open(f"results/{name}", "w") as file:
        file.write(header)
        for line in data:
            line = [str(x) for x in line]
            file.write(", ".join(line) + "\n")
        print(f"Se creó el archivo {name} exitosamente")
