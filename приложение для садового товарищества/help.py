def value(f): #функция для нахождения определённого значения
    import psycopg2
    conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute(f)
    c = cursor.fetchall()[0][0]
    conn.close()
    return c

def count():                    #расчёт общего количества соток
    import psycopg2
    conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
    cursor = conn.cursor()
    select = f""" select sum (square) from plots;"""
    cursor.execute(select)
    c = cursor.fetchall()[0][0]
    conn.close()
    return c


def ostnach(n,p): # определение остатка
    if value(n) == None and value(p) == None:
        r=0.00
    elif value(n) != None and value(p) == None:
        r = float(value(n).replace(',','.'))
    elif value(n) == None and value(p) != None:
        r = float(value(p).replace(',', '.'))*(-1)
    elif value(n) != None and value(p) != None:
        r =float(value(n).replace(',', '.')) - float(str(value(p)).replace(',','.'))
    return r
def no(p1,n1,n,p): # обработка пустых значений сумм
    if value(p1) is None: pay = str(0.00)
    else: pay = value(p1)
    if value(n1) is None: nach = str(0.00)
    else: nach = value(n1)
    k = str(ostnach(n, p) + float(nach.replace(',', '.')) - float(pay.replace(',', '.'))).replace('.', ',')
    return k,nach,pay