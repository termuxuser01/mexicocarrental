import xlsxwriter

def create_file(name, city, date):
    wb =  xlsxwriter.Workbook("{}-{}-{}.xlsx".format(name, city, date))
    return wb.add_worksheet(), wb

def wb_close(wb):
    wb.close()

def write_to_file(ws, prices, names, hours=None, insurances=None, descriptions=None, claves=None, groups=None):
    row = 0
    col = 0

    titles = ["Nombre", "Precio", "Hora", "Description", "Clave", "Grupo", "Seguros"]

    for title in titles:
        ws.write(row, col, title)
        col += 1

    row += 1
    col = 0

    if(hours == None):
        hours = return_NA(names)

    if(insurances == None):
        insurances = return_NA(names)
    
    if(descriptions == None):
        descriptions = return_NA(names)
    
    if(claves == None):
        claves = return_NA(names)
    
    if(groups == None):
        groups = return_NA(names)
    

    for n, p, h, d, c, g, s in zip(names, prices, hours, descriptions, claves, groups, insurances):
        ws.write(row, col, n)
        col += 1
        ws.write(row, col, p)
        col += 1
        ws.write(row, col, h)
        col += 1
        if(type(d) == list):
            ws.write(row, col, create_string(d))
        else:
            ws.write(row, col, d)
        col += 1
        ws.write(row, col, c)
        col += 1
        ws.write(row, col, g)
        col += 1
        ws.write(row, col, create_string(s))
        row += 1
        col = 0

def return_NA(names):
    temp = list()
    
    for i in range(len(names)):
            temp.append("N/A")

    return temp

def create_string(i):
    if(i == "N/A"):
        return i
    final = str()
    for ins in i:
        final += "*{}\n".format(ins)

    return final


