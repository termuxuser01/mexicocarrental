import xlsxwriter

def create_workbook(city, date):
    return xlsxwriter.Workbook("{}-{}.xlsx".format(city, date))

def create_worksheet(wb):
    return wb.add_worksheet()

def write_to_file(ws, prices, names, hours, insurances, descriptions, claves, groups):
    row = 0
    col = 0

    titles = ["Nombre", "Precio", "Hora", "Description", "Clave", "Grupo", "Seguros"]

    for title in titles:
        ws.write(row, col, title)
        col += 1

    row += 1
    col = 0

    for n, p, h, d, c, g, s in zip(names, prices, hours, descriptions, claves, groups, insurances):
        ws.write(row, col, n)
        col += 1
        ws.write(row, col, p)
        col += 1
        ws.write(row, col, h)
        col += 1
        ws.write(row, col, d)
        col += 1
        ws.write(row, col, c)
        col += 1
        ws.write(row, col, g)
        col += 1
        ws.write(row, col, create_insurance_string(s))
        row += 1
        col = 0

def create_insurance_string(i):
    final = str()
    for ins in i:
        final += "*{}\n".format(ins)

    return final


