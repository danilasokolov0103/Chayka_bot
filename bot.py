from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from creating_db import get_info_this_week
from creating_db import get_info_next_week
from creating_db import get_number_of_rows
import time
import logging
import settings


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {'proxy_url': 'socks5h://t1.learn.python.ru:1080',
         'urllib3_proxy_kwargs': {'username': settings.PROXY_username, 'password': settings.PROXY_password}}


def start(update, context):
    text = 'Привет {}! Это бот, который показывает тебе свободные слоты по времени в студии Чайка. Для начала используй команду /choose_week чтобы выбрать неделю. С помощью команды /choose_room выбирай репетиционную комнату. С помощью команды /choose_day выбирай день. И команда /show_results покажет тебе свободные сеты на текущую и следующую недели!)'.format(
        update.message.chat.first_name)
    command_keyboard = ReplyKeyboardMarkup(
        [['/choose_week'], ['/choose_room'], ['/choose_day'], ['/show_results'], ['/help']])
    update.message.reply_text(text, reply_markup=command_keyboard)
    logging.info("User: {}, Chat id: {}, Message: {}".format(
        update.message.chat.username, update.message.chat.id, update.message.text))


def help(update, context):
    text = 'Привет {}! Это бот, который показывает тебе свободные слоты по времени в студии Чайка. Для начала используй команду / choose_week чтобы выбрать неделю. С помощью команды / choose_room выбирай репетиционную комнату. С помощью команды / choose_day выбирай день. И команда / show_results покажет тебе свободные сеты на текущую и следующую недели!)'.format(
        update.message.chat.first_name)
    update.message.reply_text(text)


def choose_room(update, context):
    text = 'Выбирай репитиционную комнату, посмотрим какие сеты там свободны!'
    logging.info(text)
    keyboard = [[InlineKeyboardButton("реп.комната №1", callback_data='Репетиционная комната №1'),
                 InlineKeyboardButton("реп.комната №2", callback_data='Репетиционная комната №2')],

                [InlineKeyboardButton("реп.комната №3", callback_data='Репетиционная комната №3'),
                 InlineKeyboardButton("реп. комната №4", callback_data='Репетиционная комната №4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


def choose_day(update, context):

    keyboard = [[InlineKeyboardButton("понедельник", callback_data='понедельник'),
                 InlineKeyboardButton("вторник", callback_data='вторник')],

                [InlineKeyboardButton("среда", callback_data='среда'),
                 InlineKeyboardButton("четверг", callback_data='четверг')],

                [InlineKeyboardButton("пятница", callback_data='пятница'),
                 InlineKeyboardButton("суббота", callback_data='суббота')],

                [InlineKeyboardButton("воскресенье", callback_data='воскресенье')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Теперь выбери день недели', reply_markup=reply_markup)


def choose_week(update, context):
    keyboard = [[InlineKeyboardButton("Текущая неделя", callback_data='Текущая неделя'),
                 InlineKeyboardButton("Следующая неделя", callback_data='Следующая неделя')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Пока можешь выбрать из двух недель, но мы усердно работаем над добавлением новых!)', reply_markup=reply_markup)

def send_message_while_refreshing_db(update, context):
    while get_number_of_rows != 728:
        update.message.reply_text('Подождите немного база данных обновляется ,это займет пару секунд')
        time.sleep(3)

chosen_room = []
chosen_day = []
chosen_week = []
week_days = ['понедельник', 'вторник', 'среда',
             'четверг', 'пятница', 'суббота', 'воскресенье']


def choice(update, context):
    query = update.callback_query
    if query.data == "Репетиционная комната №1" or query.data == "Репетиционная комната №2" or query.data == "Репетиционная комната №3" or query.data == "Репетиционная комната №4":
        chosen_room.clear()
        chosen_room.append(query.data)
        query.edit_message_text(text="Ты выбрал: {}".format(chosen_room[0]))

    elif query.data in week_days:
        chosen_day.clear()
        chosen_day.append(query.data)
        query.edit_message_text(text="Ты выбрал: {}".format(chosen_day[0]))

    elif query.data == "Текущая неделя" or query.data == "Следующая неделя":
        chosen_week.clear()
        chosen_week.append(query.data)
        query.edit_message_text(text="Ты выбрал: {}".format(chosen_week[0]))
    else:
        None


def show_time(update, context):
    n = 0 
    while get_number_of_rows() != 728:
        n += 1
        if n < 2 :  # Отправляет сообщение о обновлении бд один раз во время цикла 
            update.message.reply_text('Подождите немного база данных обновляется, это займет пару секунд, мы сразу же пришлем вам расписание')
        time.sleep(5)
    else:
        if len(chosen_week) == 0:
            answer_this_week = get_info_this_week(chosen_room[0], chosen_day[0])
            answer_next_week = get_info_next_week(chosen_room[0], chosen_day[0])
            if len(answer_this_week) == 0:
                update.message.reply_text(
                    'На этой неделе этот день уже прошел, либо нет свободных сетов, вот что есть на следующей неделе в этот день:')
                for item in answer_next_week:
                    update.message.reply_text(item)
                update.message.reply_text(
                    'Забронировать сеты можно на сайте ' + settings.chaika_address)
            else:
                update.message.reply_text('Вот что есть на этой неделе:')
                for item in answer_this_week:
                    update.message.reply_text(item)
                update.message.reply_text('Вот что есть на следующей неделе:')
                for item in answer_next_week:
                    update.message.reply_text(item)
                update.message.reply_text(
                    'Забронировать сеты можно на сайте ' + settings.chaika_address)
        else:
            if chosen_week[0] == 'Текущая неделя':
                answer_this_week = get_info_this_week(
                    chosen_room[0], chosen_day[0])
                if len(answer_this_week) == 0:
                    update.message.reply_text(
                        'На этой неделе этот день уже прошел, либо нет свободных сетов')
                else:
                    update.message.reply_text(
                        'Вот что есть на этой неделе в выбранный день')
                    for item in answer_this_week:
                        update.message.reply_text(item)
                    update.message.reply_text(
                        'Забронировать сеты можно на сайте ' + settings.chaika_address)
                chosen_week.clear()
            else:
                answer_next_week = get_info_next_week(
                    chosen_room[0], chosen_day[0])
                if len(answer_next_week) == 0:
                    update.message.reply_text(
                        'Свободных сетов нет, попробуй другой день:()')
                else:
                    update.message.reply_text(
                        'Вот что есть на следующей неделе в этот день:')
                    for item in answer_next_week:
                        update.message.reply_text(item)
                    update.message.reply_text(
                        'Забронировать сеты можно на сайте ' + settings.chaika_address)
                chosen_week.clear()


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("choose_room", choose_room))
    dp.add_handler(CommandHandler("choose_day", choose_day))
    dp.add_handler(CommandHandler("show_results", show_time))
    dp.add_handler(CommandHandler("choose_week", choose_week))
    dp.add_handler(CallbackQueryHandler(choice))

    mybot.start_polling()
    mybot.idle()


main()
