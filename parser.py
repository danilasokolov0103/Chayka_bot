from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from creating_db import add_to_db
from creating_db import delete_expired_data
from time import mktime
import re
import settings
import chromedriver_binary
import logging


def create_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        filename='parser.log'
                        )


def get_html_and_weekdescription(week):

    error = 0
    while error < 11:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("window-size=1400,2100")
        chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(options=chrome_options)
        browser.get(settings.chaika_address)
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "room1"))
            )
            error == 12
            if week == 'this_week':
                week_description = 'Текущая неделя'
            if week == 'next_week':
                browser.find_element_by_class_name("nav_next").click()
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "nav_prev"))
                )
                week_description = 'Следующая неделя'
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')

            return soup, week_description
        except(WebDriverException, AttributeError, TypeError):
            error += 1
            if error == 10:
                print("Не получается получить javascript")
            else:
                print('Network Error')
            return False


def parsing_and_adding_to_db(soup, room_number, room_number_parsing, sec_since_epoch, week_description):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    room_number = str(room_number)
    room_tag = soup.find(class_=str(room_number_parsing)
                         )  # находим нашу комнату
    if int(str(room_number_parsing[4])) % 2 == 0 or int(str(room_number_parsing[4])) == 0:
        room_tag_exception = soup.find(class_=str(room_number_parsing))
    else:
        room_tag_exception = soup.find(class_=str(room_number_parsing).replace(
            str(room_number_parsing[4]), str(int(str(room_number_parsing[4])) - 1)))
    tr_tag = (room_tag.find('tbody')).find_all('tr')  # ищем все тэги 'tr'
    date_number = room_tag_exception.find('tr')
    date_number.find_all(class_='toprow')
    day_list = [i.get_text() for i in date_number]
    date_list = day_list[1:]
    for every_tr in tr_tag:
        # берем все тэги 'td', где лежит день недели и статус
        td_tag = every_tr.find_all('td')
        # находим время репетиций
        time = every_tr.find_all('th', class_='leftcol')
        # и делаем список времени
        time_list = [i.get_text() for i in time]

        for every_td, every_day in zip(td_tag, date_list):
            status = every_td.get('class')
            if len(status) == 0:
                status.append('free')
            day = every_day
            day = day.replace('.', ' ')
            day = day.split()
            date = day[0] + " " + day[1]  # Это дата
            day_of_week = every_td.get('data-wday')
            # избавляемся от лишнего текста
            day_format = day_of_week.replace('<span>', '')
            day_of_week_final_format = day_format.replace(
                '</span>', '')  # А это день недели
            add_to_db(room_number, time_list[0], status[0], day_of_week_final_format,
                      date, time_now, sec_since_epoch, week_description)
            delete_expired_data()


def get_room_description(soup):  # Парсим все комнаты и их описание
    number_rooms_list = []
    description_list = []
    n = -1
    for items in soup.find_all('div', class_=re.compile('^ro')):
        number_rooms_list.append((items.get('class')[0]))
    number_rooms_list_keys = number_rooms_list
    for num in number_rooms_list:
        n += 1
        if (n % 2) == 0 or n == 0:
            all_text = soup.find(class_=num)
            description = all_text.find('h2')
            description_list.append(description.get_text())
        else:
            all_text = soup.find(class_=(num.replace((num[4]), str(n-1))))
            description = all_text.find('h2')
            description_list.append(description.get_text())
    description_list_values = description_list
    rooms_dict = dict(zip(number_rooms_list_keys, description_list_values))
    return rooms_dict


def get_all_rooms_schedule():  # Выводим данные всех комнат вместе
    weeks_list = ['this_week', 'next_week']
    dt = datetime.now()
    sec_since_epoch = int(mktime(dt.timetuple()) + dt.microsecond/1000000)
    for week in weeks_list:
        html, week_description = get_html_and_weekdescription(week)
        rooms = get_room_description(html)

        for room_number_parsing, room_number in rooms.items():
            parsing_and_adding_to_db(html, room_number, room_number_parsing,
                              sec_since_epoch, week_description)
    delete_expired_data()


if __name__ == "__main__":
    get_all_rooms_schedule()
