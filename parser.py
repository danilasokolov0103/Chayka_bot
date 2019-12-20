from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import re


def get_info():
    error = 0
    while error < 11:
        browser = webdriver.PhantomJS(executable_path='/Users/danilasokolov/Downloads/phantomjs')
        browser.get('https://chaykastudia.ru/onlajn-bronirovanie/repeticionnye-komnaty/')
        html = browser.page_source
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tr_tag = (soup.find('tbody')).find_all('tr')
            error = 12
            return html
        except(WebDriverException, AttributeError):
            error += 1
            if error == 10:
                print("Не получается получить javascript")
            print('Network Error')
            return False


def get_room_schedule(html, room_number, room_number_parsing):
    room_number = str(room_number)
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    soup = BeautifulSoup(html, 'html.parser')
    room_tag = soup.find(class_=str(room_number_parsing))  # находим нашу комнату
    tr_tag = (room_tag.find('tbody')).find_all('tr')  # ищем все тэги 'tr' 
    schedule_list = []
    for every_tr in tr_tag:
        td_tag = every_tr.find_all('td')  #берем все тэги 'td', где лежит день недели и статус
        time = every_tr.find_all('th', class_='leftcol')  # находим время репетиций 
        time_list = [i.get_text() for i in time]        # и делаем список времени
        for every_td in td_tag:
            status = every_td.get('class')
            day = every_td.get('data-wday')
            day_format = day.replace('<span>', '')  #избавляемся от лишнего текста 
            day_final_format = day_format.replace('</span>', '')
            info = {
                    'room': room_number,
                    'time': time_list,
                    'status': status,
                    'day': day_final_format,
                    'parsing time': time_now
                    }
            schedule_list.append(info)
    return schedule_list


def get_room_info(html):  #Парсим все комнаты и их описание
    soup = BeautifulSoup(html, 'html.parser')
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


def get_all_rooms_schedule():  #Выводим данные всех комнат вместе
    html = get_info()
    rooms = get_room_info(html)
    final_schedule = []
    for room1, room2 in rooms.items():
        final_schedule += get_room_schedule(html, room2, room1)
    print(final_schedule)
    return final_schedule


if __name__ == "__main__":
    get_all_rooms_schedule()
