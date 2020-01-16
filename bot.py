from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, RegexHandler
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from creating_db import get_info
import logging
from datetime import datetime
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
level=logging.INFO,
filename='bot.log'
)

PROXY = {'proxy_url': 'socks5h://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': settings.PROXY_username, 'password': settings.PROXY_password}}

def start(update,context):
    text = 'Привет {}! Это бот, который показывает тебе свободные слоты по времени в студии Чайка. С помощью команды /choose_room выбирай репетиционную комнату. С помощью команды /choose_day выбирай день. И команда /show_results покажет тебе свободные слоты!)'.format(update.message.chat.first_name)
    update.message.reply_text(text)
    
def choose_room(update, context):
    text = 'Выбирай репитиционную комнату, посмотрим какие слоты там свободны!'
    logging.info(text)
    keyboard = [ [InlineKeyboardButton("реп.комната №1", callback_data='Репетиционная комната №1'),
                 InlineKeyboardButton("реп.комната №2", callback_data='Репетиционная комната №2')],

                 [InlineKeyboardButton("реп.комната №3", callback_data='Репетиционная комната №3'),
                  InlineKeyboardButton("реп. комната №4", callback_data='Репетиционная комната №4')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text,reply_markup=reply_markup)

def choose_day(update, context):

    keyboard = [[InlineKeyboardButton("понеделльник", callback_data='понедельник'),
                 InlineKeyboardButton("вторник", callback_data='вторник')],

                [InlineKeyboardButton("среда", callback_data='среда'),
                 InlineKeyboardButton("четверг", callback_data='четверг')],

                [InlineKeyboardButton("пятница", callback_data='пятница'),
                 InlineKeyboardButton("суббота", callback_data='суббота')],

                [InlineKeyboardButton("воскресенье", callback_data='воскресенье')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Теперь выбери день недели', reply_markup=reply_markup)

chosen_room = []
chosen_day = []

def choice(update, context):
    query = update.callback_query
    if query.data == "Репетиционная комната №1" or query.data == "Репетиционная комната №2" or query.data == "Репетиционная комната №3" or query.data == "Репетиционная комната №4":
        chosen_room.clear()
        chosen_room.append(query.data)
        query.edit_message_text(text="Ты выбрал: {}".format(chosen_room[0]))
    else:
        chosen_day.clear()
        chosen_day.append(query.data)
        query.edit_message_text(text="Ты выбрал: {}".format(chosen_day[0]))


def show_time(update,context):
    text = 'Вот что есть на данный момент'
    answer = get_info(chosen_room[0], chosen_day[0])
    update.message.reply_text(text)
    for item in answer:
        update.message.reply_text(item)



def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("choose_room", choose_room))
    dp.add_handler(CommandHandler("choose_day", choose_day))
    dp.add_handler(CommandHandler("show_results", show_time))
    dp.add_handler(CallbackQueryHandler(choice))
    
    mybot.start_polling()
    mybot.idle()
    
main() 
