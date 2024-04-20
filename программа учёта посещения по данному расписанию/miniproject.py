from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget, QFileDialog, QTextEdit
from PyQt6 import uic, QtPrintSupport, QtCore
import retrieve
Form, Windows = uic.loadUiType(r'miniproject.ui')
win = QApplication([])
windows = Windows()
form = Form()
form.setupUi(windows)

class ErrorMessageBox(QMessageBox):
    def __init__(self,text):
        super().__init__()
        self.setWindowTitle("Ошибка")
        self.setText(text)


def fio():
    form.Find.clear()
    form.Find.addItem('Введите фамилию и имя студента')
    for dann in retrieve.Combof(2,4,form.Group.currentText()): #загрузка данных всех существующих студентов
        form.Find.addItem(dann)

form.Find.clear()
form.Find.addItem('Введите фамилию и имя студента')
for dann in retrieve.Combo(2, 4):  # загрузка данных всех существующих студентов
    form.Find.addItem(dann)


form.Group.clear()
form.Group.addItem('Нет')
for dann in retrieve.Combo(1,2):     #загрузка данных всех существующих студентов
    form.Group.addItem(dann)


from datetime import date     #текущая дата
dt_now = str(date.today()).split("-")
form.dateVedomost.setDate(QtCore.QDate(QtCore.QDate(int(dt_now[0]), int(dt_now[1]), int(dt_now[2]))))


def Print():
    if form.Ved.toPlainText()=="":
        ErrorMessageBox("Нет данных для печати    ").exec()
        return 0
    form.dialog = QtPrintSupport.QPrintPreviewDialog()        # предварительный просмотр
    form.dialog.setWindowTitle("Предварительный просмотр")
    form.dialog.paintRequested.connect(Request)               # загрузка данных для предпросмотра
    form.dialog.exec()
def Request ():
    form.Ved.document().print(form.dialog.printer())

def Vedomost():                       #создание ведомости
    import os
    s=0
    for failname in os.listdir():
        print(failname)
        if failname.split(".")[:-1] == form.dateVedomost.dateTime().toString('dd.MM.yyyy').split("."):
            fail = failname
            s+=1
    if s==0:
        ErrorMessageBox("Нет данных для создания ведомости   ").exec()
        return 0
    form.d=retrieve.VedomostStud(form.Find.currentText(), form.Group.currentText(),fail,form.dateVedomost.dateTime().toString('dd.MM.yyyy'))    #получение данных для ведомости
    if len(form.d) == 0:
        ErrorMessageBox(f"Проверьте данные в расписании    ").exec()
        return 0
    if form.d ==['0']: #если данные не найдены сообщить об этом
        form.Ved.clear()
        ErrorMessageBox(f"Студент отсутствовал на занятиях в этот день    ").exec()
        return 0
    if form.d ==['1']: #если данные не найдены сообщить об этом
        form.Ved.clear()
        ErrorMessageBox(f"Студент не опоздал на занятия в этот день    ").exec()
        return 0
    form.Ved.clear()                                            #очистить поле вывода ведомости
    form.d.insert(0,str("Ведомость об опозданиях студентов за " + form.dateVedomost.dateTime().toString('dd.MM.yyyy')))
    form.Ved.textCursor().insertText(form.d[0]+"\n"+"\n")   #добавить первую строку и несколько вводов
    for i in range (1, len(form.d)):                              #вывести основное тело ведомости
        form.Ved.textCursor().insertText(form.d[i]+"\n")

def reset():             #сброс данных
    form.Ved.clear()
    form.Find.setCurrentIndex(0)
    form.Group.setCurrentIndex(0)
    form.Edit.setChecked(False)

def Edit():              #возможность редактирования
    if not form.Edit.isChecked():
        form.Ved.setReadOnly(True)
    else:
        form.Ved.setReadOnly(False)

def openD():        #загрузить ранее сохраненую ведомость
    s = QTextEdit()
    fname = QFileDialog.getOpenFileName(s, 'Открыть ведомость',filter='Текстовый файл(*.txt);;All Files (*)')[0]
    #если не был выбран файл для загрузки, то ничего не делай
    if fname == '':
        return 0
    f = open(fname, 'r', encoding="utf-8")
    form.Ved.clear()
    with f:
        form.Ved.insertPlainText(f.read())
def saveD():
    dannys = form.Ved.toPlainText()
    if dannys == "":
        ErrorMessageBox("Нет данных для сохранения   ").exec()
        return 0
    t = dannys.split('\n')[0]       # получение первой строки из объекта QtextEdit для задания имени файла по умолчанию
    w = QWidget()
    filename = QFileDialog.getSaveFileName(w,'Сохранить ведомость', t,"Текстовый документ (*.txt);;All Files (*)")
    if filename[0] == '':      # если пользователь не ввел имя файла
        return 0
    filename = filename[0]
    with open(filename, 'w', encoding="utf-8") as fp:
        fp.writelines(dannys)
form.pushButtonSave.clicked.connect(saveD)
form.pushButtonPrint.clicked.connect(Print)
form.pushButton.clicked.connect(Vedomost)
form.Edit.clicked.connect(Edit)
form.pushButton_2.clicked.connect(reset)
form.pushButton_3.clicked.connect(openD)
form.Group.currentIndexChanged.connect(fio)

windows.show()
win.exec()