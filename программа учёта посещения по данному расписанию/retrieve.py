def Combo(x, y):
    predmet = []
    c = open("Данные.txt", encoding='utf-8')
    c.readline()                               # пропустить заголовок
    for sp in c.readlines():
        if " ".join(sp.split()[x:y]) not in predmet:     # добавить очередную запись, только если такой еще не было
            predmet.append(" ".join(sp.split()[x:y]))
    c.close()
    return predmet
def Combof(x, y, group):
    predmet = []
    c = open("Данные.txt", encoding='utf-8')
    c.readline()            # пропустить заголовок
    if group == "Нет":
        for sp in c.readlines():
            if " ".join(sp.split()[x:y]) not in predmet:     # добавить очередную запись, только если такой еще не было
                predmet.append(" ".join(sp.split()[x:y]))
    else:
        for sp in c.readlines():
            if " ".join(sp.split()[x:y]) not in predmet and group in sp:  # добавить очередную запись, только если такой еще не было
                predmet.append(" ".join(sp.split()[x:y]))
    c.close()
    return predmet

def VedomostStud(fio, group,fail,d):
    Predmet = []
    c = open(fail, encoding='utf-8')
    b = open("Расписание.txt", encoding='utf-8')
    for s in b.readlines(1):
        if d in s:
            k = new(d)
            c.readline()  # пропустить заголовок
            v = 0
            n = 0
            if group != "Нет" and fio != 'Введите фамилию и имя студента':
                for sp in c.readlines():
                    if fio in sp: v+=1
                c.seek(0)
                c.readline()
                for sp in c.readlines():
                    if fio in sp and group in sp and sp.split()[-1] == '-':
                        if v == 1: Predmet.append(f"0")
                        else: Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " отсутствовал(а) на занятиях в этот день    ")
                    if fio in sp and group in sp and sp.split()[-1] != '-':
                        b.seek(0)
                        b.readline()
                        for s in b.readlines():
                            if group in s and number(s, k) >= number(sp, -1):
                                if v == 1: Predmet.append(f"1")
                                else: Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + "не опоздал(а) на занятия в этот день    ")
                            if group in s and number(s, k) < number(sp,-1):  # добавить очередную запись, если она нам подходит
                                if str(count(sp, s, k)).split(':')[0] == '0':
                                    Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " опоздал(а) на " + str(count(sp, s, k)).split(':')[1] + " мин.")
                                else:
                                    Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " опоздал(а) на " + str(count(sp, s, k)).split(':')[0] + ' ч. ' + str(count(sp, s, k)).split(':')[1] + " мин.")
            elif group != "Нет" and fio == 'Введите фамилию и имя студента':
                Predmet.append(f"               Группа {group}\n    Фамилия Имя        опоздал(а) на:")
                for s in b.readlines():
                    if group in s:
                        for sp in c.readlines():
                            if sp.split()[-1] != '-':
                                if group in sp:
                                    if number(s,k) < number(sp,-1): # добавить очередную запись, если она нам подходит
                                        n += 1
                                        if str(count(sp,s,k)).split(':')[0]== '0':
                                            Predmet.append(str(n) + ". " + " ".join(sp.split()[2:4]).ljust(30) + " " + str(count(sp,s,k)).split(':')[1] +" мин.")
                                        else: Predmet.append(str(n) + ". " + " ".join(sp.split()[2:4]).ljust(30) + " " + str(count(sp,s,k)).split(':')[0] + ' ч. ' + str(count(sp,s,k)).split(':')[1] +" мин.")
            elif group == "Нет" and fio == 'Введите фамилию и имя студента':
                Predmet.append(f"    Группа       Фамилия Имя               опоздал(а) на: ")
                for s in b.readlines():
                    c.seek(0)
                    c.readline()
                    for sp in c.readlines():
                        if s.split()[0] in sp and sp.split()[-1] != '-':
                            if number(s, k) < number(sp, -1):  # добавить очередную запись, если она нам подходит
                                n += 1
                                if str(count(sp, s, k)).split(':')[0] == '0':
                                    Predmet.append(str(n) + ". " + " ".join(sp.split()[1:4]).ljust(40) + " " + str(count(sp, s, k)).split(':')[1] + " мин.")
                                else:
                                    Predmet.append(str(n) + ". " + " ".join(sp.split()[1:4]).ljust(40) + " " + str(count(sp, s, k)).split(':')[0] + ' ч. '+ str(count(sp, s, k)).split(':')[1] + " мин.")
            elif group == "Нет" and fio != 'Введите фамилию и имя студента':
                for sp in c.readlines():
                    if fio in sp: v+=1
                c.seek(0)
                c.readline()
                for sp in c.readlines():
                    if fio in sp and sp.split()[-1] == '-':
                        if v==1: Predmet.append(f"0")
                        else: Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " отсутствовал(а) на занятиях в этот день    ")
                    if fio in sp and sp.split()[-1] != '-':
                        group =(str(sp.split()[1:2]))[2:][:-2]
                        b.seek(0)
                        b.readline()
                        for s in b.readlines():
                            if group in s and number(s, k) >= number(sp, -1):
                                if v==1: Predmet.append(f"1")
                                else: Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4])  + "не опоздал(а) на занятия в этот день    ")
                            if group in s and number(s, k) < number(sp,-1):  # добавить очередную запись, если она нам подходит
                                if str(count(sp, s, k)).split(':')[0] == '0':
                                    Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " опоздал(а) на " + str(count(sp, s, k)).split(':')[1] + " мин.")
                                else:
                                    Predmet.append(sp.split()[0] + ". Группа " + " ".join(sp.split()[1:4]) + " опоздал(а) на " + str(count(sp, s, k)).split(':')[0] + ' ч. ' + str(count(sp, s, k)).split(':')[1] + " мин.")

    return Predmet
def number(a,e):                #Нахождение времени для сравнения
    from datetime import time
    tim = a.split()[e].split(':')
    srok = time(int(tim[0]), int(tim[1]))
    return srok
def new(d):                     #Нахождение места времени для нужного дня нужной группы в расписании
    b = open("Расписание.txt", encoding='utf-8')
    for s in b.readlines(1):
        r = s.split('\t')
        for i in range(len(r)):
            if r[i] == str(d):
                return i
def count(sp,s,i):            #Вычитание времени
    from datetime import datetime
    format = '%H:%M'
    time = datetime.strptime(sp.split()[-1], format) - datetime.strptime(s.split()[i], format)
    return time