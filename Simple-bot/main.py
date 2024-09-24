import telebot
from telebot import types
import psycopg2
import datetime
token = '6484370705:AAGCtmjuxLhNApuy_gDWTpNBWECg0Htr9HM'
bot = telebot.TeleBot(token)

#подключение к базе данных
conn = psycopg2.connect(database="lab_2",user="mospolytech",password="1a2b3c4d")
cur = conn.cursor()

#обработка команды /polytech
@bot.message_handler(commands = ['polytech'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Сайт Политеха 🏬', url='https://mospolytech.ru/')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти на сайт ВУЗа", reply_markup = markup)

#обработка команды /lk
@bot.message_handler(commands = ['lk'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='Личный кабинет 👨‍🎓', url='https://e.mospolytech.ru/#/login')
    markup.add(btn1)
    bot.send_message(message.from_user.id, "По кнопке ниже можно перейти в личный кабинет студента", reply_markup = markup)

#функция определения типа недели
def get_current_week():
    today = datetime.date.today()
    week_number = today.isocalendar()[1]
    if week_number % 2 == 0:
        return "Нижняя неделя"
    else:
        return "Верхняя неделя"

#обработка команды /week
@bot.message_handler(commands=['week'])
def show_current_week(message):
    week = get_current_week()
    bot.send_message(message.chat.id, week)

#обработка команды /help
@bot.message_handler(commands=['help'])
def show_help(message):
    help_text = "Здравствуйте! Я бот с расписанием для вашей группы.\n\n"
    help_text += "Доступные команды:\n"
    help_text += "/week - узнать какая текущая неделя - верхняя или нижняя\n"
    help_text += "/polytech - получить ссылку на сайт Московского Политеха\n"
    help_text += "/lk - получить ссылку на личный кабинет студента\n"
    help_text += "/help - вывести это сообщение"
    bot.send_message(message.chat.id, help_text)

#обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    weeks = [types.KeyboardButton("Расписание на текущую неделю"),
            types.KeyboardButton("Расписание на следующую неделю")]
    keyboard.add(*[types.KeyboardButton(day) for day in days])
    keyboard.add(*weeks)
    bot.send_message(message.chat.id, 'Здравствуйте! Выберите день недели:', reply_markup=keyboard)

# Обработка кнопок с текущей и следующей неделей
@bot.message_handler(func=lambda message: message.text in ["Расписание на текущую неделю", "Расписание на следующую неделю"])
def handle_schedule_buttons(message):
    week = message.text
    type_of_week = get_current_week()
    zapros = "SELECT a.day_of_week, name, room_numb, start_time, full_name FROM timetable a JOIN subject b ON a.subject_id = b.subject_id JOIN teacher c ON b.subject_id = c.subject_id"
    if week == "Расписание на текущую неделю":
        if type_of_week == "Верхняя неделя":
            cur.execute( f"{zapros}" + " WHERE type_of_week = 'нечётная';")
        else: cur.execute( f"{zapros}" + " WHERE type_of_week = 'чётная';")
    elif week == "Расписание на следующую неделю":
        if type_of_week == "Верхняя неделя":
            cur.execute(f"{zapros}" + " WHERE type_of_week = 'чётная';")
        else: cur.execute(f"{zapros}" + " WHERE type_of_week = 'нечётная';")
    schedule = cur.fetchall()
    if len(schedule) > 0:
        schedule_text = ""
        for i in schedule:
            subject = i[1]
            room_numb = i[2]
            start_time = i[3]
            full_name = i[4]
            if i[0] not in schedule_text:  schedule_text +=f"\n{i[0]} \n\n"
            schedule_text += f"{subject} \n{room_numb} {start_time} \n{full_name} \n\n"
        bot.send_message(message.chat.id, schedule_text)
    else:
        bot.send_message(message.chat.id, "Расписание не найдено")

# Обработка кнопок с днями недели
@bot.message_handler(func=lambda message: message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
def handle_weekday_buttons(message):
    day = message.text
    zapros = "SELECT a.day_of_week, name, room_numb, start_time, full_name FROM timetable a JOIN subject b ON a.subject_id = b.subject_id JOIN teacher c ON b.subject_id = c.subject_id"
    type_of_week = get_current_week()
    if type_of_week == "Верхняя неделя":
        cur.execute(f"{zapros}" + " WHERE type_of_week = 'нечётная' AND a.day_of_week = " + f"'{day}'" + ";")
    else:
        cur.execute(f"{zapros}" + " WHERE type_of_week = 'чётная' AND a.day_of_week = " + f"'{day}'" + ";")
    schedule = cur.fetchall()
    if len(schedule) > 0:
        schedule_text = f"{day}:\n\n"
        for i in schedule:
            subject = i[1]
            room_numb = i[2]
            start_time = i[3]
            full_name = i[4]
            schedule_text += f"{subject} \n{room_numb} {start_time} \n{full_name} \n\n"
        bot.send_message(message.chat.id, schedule_text)
    else:
        bot.send_message(message.chat.id, "На выбранный день расписание отсутствует")


#обработка трёх типов сообщений + если не понимает
data = ['спасибо','благодарю', 'привет', 'здравствуй','здравствуйте','у тебя есть расписание сессии?']
@bot.message_handler(content_types=['text'])
def thanks(message):
    if message.text.lower() == data[0] or message.text.lower() == data[1]:
        bot.send_message(message.chat.id, 'Рад был Вам помочь.\nПишите ещё!😊')
    elif message.text.lower() == data[2] or message.text.lower() == data[3] or message.text.lower() == data[4]:
        bot.send_message(message.chat.id, 'Здравствуйте, ' + message.from_user.first_name + '!👋\nВся информация обо мне -\nпо команде /help')
    elif message.text.lower() == data[5]:
        bot.send_message(message.chat.id, "К сожалению, этой информации у меня нет.\n❓ Чтобы узнать о моих возможностях , выполните команду /help")
    else: bot.send_message(message.chat.id, "Извините, я Вас не понял.😿")

#запуск бота, затем - закрытие соединения с БД
bot.polling()
cur.close()
conn.close()






