from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import ephem
from datetime import datetime
from creating_db import get_info


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
level=logging.INFO,
filename='bot.log'
)

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

def greet_user(bot, update):
    text = 'Привет! Хочешь узнать свободные слоты? Пиши время!'
    print(text)

    update.message.reply_text(text)

# def talk_to_me(bot, update):
#     user_text = update.message.text
#     print(user_text)
#     update.message.reply_text(user_text)

def show_time(bot, update):
    user_text = update.message.text
    result1 = []
    result1.append(get_info(result1, user_text))
    print (result1)
    update.message.reply_text(result1)

# def planet_check(bot, update):
#     m = update.message.text
#     list1 = m.split()
#     planet_start = list1[1]
#     print(list1[1])
#     if planet_start.lower() == "mars":
#         planet_start = ephem.Mars(datetime.now())
#     elif planet_start.lower() == "jupiter":
#         planet_start = ephem.Jupiter(datetime.now())
#     elif planet_start.lower() == "venus":
#         planet_start = ephem.Venus(datetime.now())
#     elif planet_start.lower() == "saturn":
#         planet_start = ephem.Saturn(datetime.now())
#     elif planet_start.lower() == "uranus":
#         planet_start = ephem.Uranus(datetime.now())
#     elif planet_start.lower() == "earth":
#         planet_start = ephem.Earth(datetime.now())
#     elif planet_start.lower() == "mercury":
#         planet_start = ephem.Mercury(datetime.now())
#     elif planet_start.lower() == "neptune":
#         planet_start = ephem.Neptune(datetime.now())
#     user_text = ephem.constellation(planet_start)
#     print(user_text)
#     update.message.reply_text(user_text)


def main():
    mybot = Updater("1051194187:AAEkERAhosD_CFNCBFE3qA6acn78hWEdVKA", request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    # dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    dp.add_handler(MessageHandler("timetable", show_time))
    # dp.add_handler(CommandHandler("planet", planet_check))
    mybot.start_polling()
    mybot.idle()

main()
