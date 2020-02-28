from creating_db import get_info_this_week
from creating_db import get_info_next_week
from creating_db import get_number_of_rows
from bot import chosen_day, chosen_room, chosen_week
import time
import settings


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
