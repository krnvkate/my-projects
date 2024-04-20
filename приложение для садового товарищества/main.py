from PyQt6.uic import loadUiType
from PyQt6 import QtWidgets,  QtCore, QtGui, QtPrintSupport
from PyQt6.QtWidgets import QDialog, QApplication,  QMessageBox, QTableWidget, QHeaderView
import psycopg2
from psycopg2 import Error
from help import value, count, ostnach, no
from mainim import Ui_MainWindow

class ErrorMessageBox(QMessageBox):  # в случае ввода неверных данных для входа в систему пользователь увидит сообщение
    def __init__(self,text):
        super().__init__()
        self.setWindowTitle("Внимание")
        self.setText(text)

# изменение ширины колонок в соответствии с их содержимым
def width(table_name):
    header = table_name.horizontalHeader()
    for i in range(table_name.columnCount()):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
#постановка текущей даты на календарь
def date_now(a):
    from datetime import date
    dt_now = str(date.today()).split("-")
    a.setDate(QtCore.QDate(QtCore.QDate(int(dt_now[0]), int(dt_now[1]), int(dt_now[2]))))
# заполнение combobox
def comb(sel, forma, b):
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute(sel)
        for row in cursor.fetchall():
            forma.addItem(row[b])
        conn.close()
    except:
        return 0
# вывод таблицы
def select(selec,tableWidget):
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute(selec)
        fetch = cursor.fetchall()
        tableWidget.setRowCount(len(fetch))
        for i in range(len(fetch)):
            for j in range(len(fetch[0])):
                tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(fetch[i][j])))
        conn.close()
    except:
        return 0
def win():

    width(form.plots)
    width(form.fees)
    width(form.payment)
    width(form.charget)
    width(form.payt)


    #ограничение на ввод букв в поле суммы
    form.symma.setValidator(QtGui.QDoubleValidator())
    form.sum_rest.setValidator(QtGui.QDoubleValidator())

    date_now(form.date_fix)
    date_now(form.dateEdit)
    date_now(form.dateEdit_3)
    comb(f""" select distinct a.fee_name from fees_guide a join fees_rate b on a.fee_id=b.fee_id;""", form.fee_name_2, 0)
    comb(f""" select * from plots;""", form.home_number, 0)
    comb(f""" select * from plots;""", form.home_name, 1)
    comb(f""" select * from plots;""", form.num_home, 0)
    comb(f""" select distinct a.fee_name from fees_guide a join fees_rate b on a.fee_id=b.fee_id;""", form.name_fee, 0)
    comb(f""" select * from fees_guide;""", form.fee_name, 1)

    select(f""" select number, name, replace(square::text,'.',',') from plots order by number;""", form.plots)

    select( f""" select a.fee_name, to_char(b.date_change, 'DD.MM.YYYY'), replace(b.sum::text,'.',','), replace(b.sum_all::text,'.',',')
        from fees_guide a join fees_rate b on a.fee_id = b.fee_id;""",form.fees)



def dobavit(): # добавление записи в таблицу сведений об участках
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        number_plot = form.number_plot.text().strip()
        name = form.name.text().strip()
        square = form.square.text().replace(",", ".")
        if len(number_plot)==0 or len(name)==0 or square=='0.00':  # проверка на отправку пустых значений
            ErrorMessageBox(f"Заполните все поля    ").exec()
            return
        check = f""" SELECT number FROM plots WHERE name = '{name}';""" #проверка на уже имеющиеся данные
        cursor.execute(check)
        if cursor.fetchone() == None:
            insert = f""" INSERT INTO plots (number, name, square) VALUES ('{number_plot}', '{name}', '{square}')"""
            cursor.execute(insert)
            conn.commit()
            select(f""" select number, name, replace(square::text,'.',',') from plots order by number;""", form.plots)
            form.number_plot.clear()  # очистка полей
            form.name.clear()
            form.square.setValue(0.00)
        else:
            ErrorMessageBox(f"Информация по этому дому уже существует, измените её   ").exec()
            return
        conn.close()
    except (Exception, Error) as error:
        print('Ошибка', error)

def setplots():    #вывод значений из таблицы участков в ячейки после двойного нажатия
    for idx in form.plots.selectionModel().selectedIndexes():
        row_number = idx.row()
        form.number_plot.setText(form.plots.item(row_number, 0).text())
        form.number_plot.setEnabled(False)          # запрет редактирования
        form.name.setText(form.plots.item(row_number, 1).text())
        form.square.setValue(float(form.plots.item(row_number, 2).text().replace(',','.')))

def up(): #обновление таблицы с участками
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        upp = f"""update plots set name = '{form.name.text().strip()}', square ='{form.square.text().replace(",", ".")}' where number = '{form.number_plot.text().strip()}';"""
        cursor.execute(upp)
        conn.commit()
        conn.close()
        select(f""" select number, name, replace(square::text,'.',',') from plots order by number;""", form.plots)
        form.number_plot.clear()    #очистка полей
        form.name.clear()
        form.square.setValue(0.00)
        form.number_plot.setEnabled(True)    #возвращение редактирования
    except:
        return 0

def zero(): # полное удаление информации о владельце
    ErrorMessageBox(f"После нажатия на 'ок' удалится вся информация о начислениях и оплатах владельца этого участка\nВы уверены, что хотите продолжить?").exec()
    for idx in form.plots.selectionModel().selectedIndexes():
        row_number = idx.row()
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        d = f"""delete from plots where number = '{form.plots.item(row_number, 0).text()}';"""
        cursor.execute(d)
        conn.commit()
        conn.close()
        select(f""" select number, name, replace(square::text,'.',',') from plots order by number;""", form.plots)
    except:
        return 0
def add():              # добавление записей в обе таблицы справочника
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        k = float(count())
        fee_name = form.fee_name.currentText().strip()
        if len(fee_name) == 0 or len(form.symma.text().strip()) == 0 or form.comboBox.currentText() == 'нет':
            ErrorMessageBox(f"Заполните все поля    ").exec()
            return
        else:
            check = f""" SELECT fee_id FROM fees_guide WHERE fee_name = '{fee_name}';"""
            cursor.execute(check)
            if cursor.fetchone() == None:
                insert = f""" INSERT INTO fees_guide (fee_name) VALUES ('{fee_name}')"""
                cursor.execute(insert)
                conn.commit()
            id = value(f"""select fee_id from fees_guide where fee_name = '{fee_name}';""")
            date = form.dateEdit.text()
            symma = float(form.symma.text().replace(",", "."))
            if form.comboBox.currentText() == 'за одну сотку':
                sum_all=symma*k
                insert = f""" INSERT INTO fees_rate (fee_id,date_change, sum, sum_all) VALUES ('{id}','{date}','{symma}','{sum_all}')"""
                cursor.execute(insert)
                conn.commit()
            elif form.comboBox.currentText() == 'общая сумма':
                sum = round(symma/k, 2)
                insert = f""" INSERT INTO fees_rate (fee_id, date_change, sum, sum_all) VALUES ('{id}','{date}','{sum}','{symma}')"""
                cursor.execute(insert)
                conn.commit()
            select(f""" select a.fee_name, to_char(b.date_change, 'DD.MM.YYYY'), replace(b.sum::text,'.',','), replace(b.sum_all::text,'.',',')
            from fees_guide a join fees_rate b on a.fee_id = b.fee_id;""",form.fees)
        conn.close()
    except (Exception, Error) as error:
        print('Ошибка', error)
def charge(): #заполнение таблицы начислений
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        id = value(f"""select fee_id from fees_guide where fee_name = '{form.fee_name.currentText().strip()}';""")
        sym = float(value(f""" select sum from fees_rate where fee_id = '{id}' and date_change = '{form.dateEdit.text()}'; """))
        select = f""" select * from plots; """
        cursor.execute(select)
        for row in cursor.fetchall():
            s = sym * float(row[2])
            insert = f""" INSERT INTO fees_charge (number, fee_id, date_charge, sum_charge) VALUES ('{row[0]}','{id}','{form.dateEdit.text()}','{s}')"""
            cursor.execute(insert)
            conn.commit()
        conn.close()
    except (Exception, Error) as error:
        print('Ошибка', error)

def sett():    #удаление записи о взносе
    for idx in form.fees.selectionModel().selectedIndexes():
        row_number = idx.row()
        s = f""" select fee_id from fees_guide where fee_name = '{form.fees.item(row_number, 0).text()}';"""
        try:
            conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
            cursor = conn.cursor()
            selec = f"""delete from fees_rate where fee_id = '{value(s)}' and date_change = '{form.fees.item(row_number, 1).text()}'
            and sum = '{form.fees.item(row_number, 2).text().replace(',', '.')}' and sum_all = '{form.fees.item(row_number, 3).text().replace(',', '.')}';"""
            cursor.execute(selec)
            conn.commit()
            s = f"""delete from fees_charge where fee_id = '{value(s)}' and date_charge = '{form.fees.item(row_number, 1).text()}';"""
            cursor.execute(s)
            conn.commit()
            conn.close()
            select(f""" select a.fee_name, to_char(b.date_change, 'DD.MM.YYYY'), replace(b.sum::text,'.',','), replace(b.sum_all::text,'.',',')
            from fees_guide a join fees_rate b on a.fee_id = b.fee_id;""",form.fees)
        except:
            return 0

def show_n():   #вывод оплаты по дому
    try:
        a = 'from payment a join fees_guide b on a.fee_id = b.fee_id'
        if form.home_number.currentText().strip() == '' and form.home_name.currentText().strip() == '':
            ErrorMessageBox(f"Выберите номер дома или ФИО владельца для просмотра иформации    ").exec()
            return
        elif form.home_number.currentText().strip() != '' and form.home_name.currentText().strip() == '':
            number = form.home_number.currentText()
            select(f"""select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {a} where number = '{number}' order by a.date_pay;""", form.payment)
        elif form.home_number.currentText().strip() == '' and form.home_name.currentText().strip() != '':
            number = value(f"""select number from plots where name='{form.home_name.currentText()}';""")
            form.home_number.setCurrentText(number)
            select(f"""select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {a} where number = '{number}' order by a.date_pay;""", form.payment)
        elif form.home_number.currentText().strip() != '' and form.home_name.currentText().strip() != '':
            namen = value(f"""select name from plots where number='{form.home_number.currentText()}';""")
            if namen == form.home_name.currentText():
                select(f"""select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {a} where number = '{form.home_number.currentText()}' order by a.date_pay;""", form.payment)
            else:
                ErrorMessageBox(f"Выбранный номер дома не соответствует выбранному ФИО владельца").exec()
                return
    except (Exception, Error) as error:
        print('Ошибка', error)

def ins(): # добавление данных в таблицу оплат
    try:
        conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
        cursor = conn.cursor()
        home_number= form.home_number.currentText().strip()
        if len (home_number) == 0 or form.fee_name_2.currentText() == 'нет' or form.sum_rest.text() == '':
            ErrorMessageBox(f"Заполните все поля    ").exec()
            return
        else:
            id = value(f"""select fee_id from fees_guide where fee_name = '{form.fee_name_2.currentText()}';""")
            insert = f""" INSERT INTO payment (number, fee_id, date_pay, sum_pay) VALUES ('{home_number}', '{id}', '{form.date_fix.text()}', '{form.sum_rest.text().replace(',','.')}')"""
            cursor.execute(insert)
            conn.commit()
            select(f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',')
                    from payment a join fees_guide b on a.fee_id = b.fee_id where number = '{home_number}' order by a.date_pay""", form.payment)
        conn.close()
    except: return 0
def delete_data():    #удаление записи об оплате
    try:
        for idx in form.payment.selectionModel().selectedIndexes():
            row_number = idx.row()
            s = f""" select fee_id from fees_guide where fee_name = '{form.payment.item(row_number, 1).text()}';"""
            conn = psycopg2.connect(dbname='garden', user='main', password='1a2b3c', host="localhost", port="5432")
            cursor = conn.cursor()
            selec = f"""delete from payment where number = '{form.payment.item(row_number, 0).text()}' and fee_id = '{value(s)}'
            and date_pay = '{form.payment.item(row_number, 2).text()}' and sum_pay = '{form.payment.item(row_number, 3).text().replace(',','.')}';"""
            cursor.execute(selec)
            conn.commit()
            conn.close()
            select(f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',')
            from payment a join fees_guide b on a.fee_id = b.fee_id where number = '{form.payment.item(row_number, 0).text()}' order by a.date_pay""", form.payment)
    except:
        return 0

def otchet(): #вывод таблицы начислений и оплат за период
    try:
        a = 'from fees_guide b join fees_charge a on a.fee_id = b.fee_id'
        b = 'from payment a join fees_guide b on a.fee_id = b.fee_id'
        number = form.num_home.currentText()
        fee_name = form.name_fee.currentText()
        date_2 = form.dateEdit_2.text()
        date_3 = form.dateEdit_3.text()
        if number == 'всё СНТ' and fee_name == 'все взносы':
            n = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where date_charge < '{date_2}';"""
            p = f""" select replace(sum (sum_pay)::text,'.',',') from payment where date_pay < '{date_2}';"""
            p1 = f""" select replace(sum (sum_pay)::text,'.',',') from payment where date_pay >= '{form.dateEdit_2.text()}' and date_pay <= '{form.dateEdit_3.text()}';"""
            n1 = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where date_charge >= '{form.dateEdit_2.text()}' and date_charge <= '{form.dateEdit_3.text()}';"""
            k,nach,pay = no(p1,n1,n,p)
            form.inf.setText('Информация по всему СНТ по всем взносам:' + '\n' + 'Остаток на начало периода: ' + str(ostnach(n,p)).replace('.',',') + ' руб.\n'
            + 'Начислено: ' + str(nach).replace('.',',') + ' руб. Оплачено: ' + str(pay).replace('.',',') + ' руб. Остаток на конец периода: ' + k.replace('.',',') +' руб.'   )
            select(f""" select a.number, b.fee_name, to_char(a.date_charge, 'DD.MM.YYYY'), replace(a.sum_charge::text,'.',',') {a} where a.date_charge >= '{form.dateEdit_2.text()}' and a.date_charge <= '{form.dateEdit_3.text()}';""", form.charget)
            select( f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {b} where a.date_pay >= '{form.dateEdit_2.text()}' and a.date_pay <= '{date_3}';""", form.payt)
        elif form.num_home.currentText() != 'всё СНТ' and form.name_fee.currentText() == 'все взносы':
            n = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where date_charge < '{date_2}' and number = '{number}';"""
            p = f""" select replace(sum (sum_pay)::text,'.',',') from payment where date_pay < '{date_2}' and number = '{number}';"""
            n1 = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where number = '{number}' and date_charge >= '{form.dateEdit_2.text()}' and date_charge <= '{form.dateEdit_3.text()}';"""
            p1 = f""" select replace(sum (sum_pay)::text,'.',',') from payment where number = '{number}' and date_pay >= '{form.dateEdit_2.text()}' and date_pay <= '{form.dateEdit_3.text()}';"""
            k,nach,pay = no(p1,n1,n,p)
            form.inf.setText('Информация по участку номер ' + number  + '\n' + 'Остаток на начало периода: ' + str(ostnach(n,p)).replace('.',',') + ' руб.\n'
            + 'Начислено: ' + str(nach).replace('.',',') + ' руб. Оплачено: ' + str(pay).replace('.',',') + ' руб. Остаток на конец периода: ' + k.replace('.',',') +' руб.')
            select(f""" select a.number, b.fee_name, to_char(a.date_charge, 'DD.MM.YYYY'), replace(a.sum_charge::text,'.',',') {a} where a.number = '{number}' and a.date_charge >= '{form.dateEdit_2.text()}' and a.date_charge <= '{form.dateEdit_3.text()}';""", form.charget)
            select(f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {b} where number = '{number}' and a.date_pay >= '{form.dateEdit_2.text()}' and a.date_pay <= '{form.dateEdit_3.text()}';""",form.payt)
        elif form.num_home.currentText() != 'всё СНТ' and form.name_fee.currentText() != 'все взносы':
            id = value(f"""select fee_id from fees_guide where fee_name = '{fee_name}';""")
            n = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where date_charge < '{date_2}' and number = '{number}' and fee_id = '{id}' ;"""
            p = f""" select replace(sum (sum_pay)::text,'.',',') from payment where date_pay < '{date_2}' and number = '{number}' and fee_id = '{id}' ;"""
            n1 = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where number = '{number}' and fee_id = '{id}' and date_charge >= '{form.dateEdit_2.text()}' and date_charge <= '{form.dateEdit_3.text()}';"""
            p1 = f""" select replace(sum (sum_pay)::text,'.',',') from payment where number = '{number}' and fee_id = '{id}' and date_pay >= '{form.dateEdit_2.text()}' and date_pay <= '{form.dateEdit_3.text()}';"""
            k,nach,pay = no(p1,n1,n,p)
            form.inf.setText('Информация по участку номер ' + number + ', взнос: ' + fee_name + '\n' + 'Остаток на начало периода: '
            + str(ostnach(n, p)).replace('.',',') + ' руб.\n' + 'Начислено: ' + str(nach).replace('.',',') + ' руб. Оплачено: ' + str(pay).replace('.',',') + ' руб. Остаток на конец периода: ' + k.replace('.',',') + ' руб.')
            select(f""" select a.number, b.fee_name, to_char(a.date_charge, 'DD.MM.YYYY'), replace(a.sum_charge::text,'.',',') {a} where a.number = '{number}' and b.fee_name = '{fee_name}' and a.date_charge >= '{form.dateEdit_2.text()}' and a.date_charge <= '{form.dateEdit_3.text()}';""",form.charget)
            select(f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {b} where a.number = '{number}' and b.fee_name = '{fee_name}' and a.date_pay >= '{form.dateEdit_2.text()}' and a.date_pay <= '{form.dateEdit_3.text()}';""", form.payt)
        elif form.num_home.currentText() == 'всё СНТ' and form.name_fee.currentText() != 'все взносы':
            id = value(f"""select fee_id from fees_guide where fee_name = '{fee_name}';""")
            n = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where date_charge < '{date_2}' and fee_id = '{id}' ;"""
            p = f""" select replace(sum (sum_pay)::text,'.',',') from payment where date_pay < '{date_2}' and fee_id = '{id}' ;"""
            n1 = f""" select replace(sum (sum_charge)::text,'.',',') from fees_charge where fee_id = '{id}' and date_charge >= '{form.dateEdit_2.text()}' and date_charge <= '{form.dateEdit_3.text()}';"""
            p1 = f""" select replace(sum (sum_pay)::text,'.',',') from payment where fee_id = '{id}' and date_pay >= '{form.dateEdit_2.text()}' and date_pay <= '{form.dateEdit_3.text()}';"""
            k,nach,pay = no(p1,n1,n,p)
            form.inf.setText( 'Информация по всему СНТ, взнос: ' + fee_name + '\n' + 'Остаток на начало периода: '
                + str(ostnach(n, p)).replace('.',',') + ' руб.\n' + 'Начислено: ' + str(nach).replace('.',',') + ' руб. Оплачено: ' + str(pay).replace('.',',') + ' руб. Остаток на конец периода: ' + k.replace('.',',') + ' руб.')
            select(f""" select a.number, b.fee_name, to_char(a.date_charge, 'DD.MM.YYYY'), replace(a.sum_charge::text,'.',',') {a} where b.fee_name = '{form.name_fee.currentText()}' and a.date_charge >= '{form.dateEdit_2.text()}' and a.date_charge <= '{form.dateEdit_3.text()}';""",form.charget)
            select(f""" select a.number, b.fee_name, to_char(a.date_pay, 'DD.MM.YYYY'), replace(a.sum_pay::text,'.',',') {b} where b.fee_name = '{fee_name}' and a.date_pay >= '{form.dateEdit_2.text()}' and a.date_pay <= '{form.dateEdit_3.text()}';""", form.payt)
    except (Exception, Error) as error:
        print('Ошибка', error)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    form = Ui_MainWindow()
    form.setupUi(MainWindow)
    win()
    form.add_in_plots.clicked.connect(dobavit)
    form.plots.doubleClicked.connect(setplots)
    form.pushButton_2.clicked.connect(up)
    form.delet.clicked.connect(zero)

    form.add_data.clicked.connect(add)
    form.delete_2.clicked.connect(sett)
    form.nachis.clicked.connect(charge)

    form.show_n.clicked.connect(show_n)
    form.ins.clicked.connect(ins)
    form.delete_data.clicked.connect(delete_data)

    form.sform.clicked.connect(otchet)

    MainWindow.show()
    sys.exit(app.exec())


