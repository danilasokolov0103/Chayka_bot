from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from creating_db import get_info
import logging
import ephem
from datetime import datetime
import config

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
level=logging.INFO,
filename='bot.log'
)


def greet_user(update, context):
    text = 'Привет {}! Хочешь узнать свободные слоты? Пиши время!'.format(update.message.chat.first_name)
    logging.info(text)
    schedule_keyboard = ReplyKeyboardMarkup([['9–10'], ['10–11'],['11–12'],['12–13'], ['13–14'], ['14–15'],['15–16'], ['16–17'], ['17–18'], ['18–19'],['19–20'], ['20–21'], ['21–24']]) 
    update.message.reply_text(text, reply_markup=schedule_keyboard)

def talk_to_me(update, context):
    user_text = update.message.text
    logging.info(update.message)
    answer = get_info(user_text)
    for item in answer:
        update.message.reply_text(item[0])
        update.message.reply_text(item[1])
        update.message.reply_text(item[2])



def main():
    mybot = Updater(config.API_KEY, request_kwargs=config.PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    mybot.start_polling()
    mybot.idle()
    


main() 
