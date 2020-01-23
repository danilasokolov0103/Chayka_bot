from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from creating_db import schedule_db
from creating_db import Schedule
from creating_db import add_to_db
from creating_db import delete_expired_data
from creating_db import get_log
import time
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



def get_info():

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
            browser.find_element_by_class_name("nav_next").click()
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            logging.info("Selenium is working fine")
                
            return soup
        except(WebDriverException, AttributeError,TypeError):
            error += 1
            if error == 10:
                print("Не получается получить javascript")
                logging.info('Problems with getting javascript')
            else:
                print('Network Error')
                logging.info('Connection problems')
            return False


def get_room_schedule(soup, room_number, room_number_parsing, sec_since_epoch):
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')
    room_number = str(room_number)
    room_tag = soup.find(class_=str(room_number_parsing))  # находим нашу комнату
    if  int(str(room_number_parsing[4])) % 2 == 0 or int(str(room_number_parsing[4])) == 0:   
        room_tag_exception = soup.find(class_=str(room_number_parsing))
    else:
        room_tag_exception = soup.find(class_=str(room_number_parsing).replace(str(room_number_parsing[4]),str(int(str(room_number_parsing[4])) - 1)))
    #schedule_list = []
    tr_tag = (room_tag.find('tbody')).find_all('tr')  # ищем все тэги 'tr' 
    date_number = room_tag_exception.find('tr')
    date_number.find_all(class_ = 'toprow')
    day_list = [i.get_text() for i in date_number]
    date_list = day_list[1:]
    for every_tr in tr_tag:
        td_tag = every_tr.find_all('td')  #берем все тэги 'td', где лежит день недели и статус
        time = every_tr.find_all('th', class_='leftcol')  # находим время репетиций 
        time_list = [i.get_text() for i in time]        # и делаем список времени

        for every_td,every_day in zip(td_tag,date_list):
            status = every_td.get('class')
            if len(status) == 0 :
                status.append('free')
    
            day = every_day
            day = day.replace('.',' ')
            day = day.split()
            date = day[0]+ " " +day[1] # Это дата 
            day_of_week = every_td.get('data-wday')
            day_format = day_of_week.replace('<span>', '')  #избавляемся от лишнего текста 
            day_of_week_final_format = day_format.replace('</span>', '') # А это день недели
            #info = {
            #        'room': room_number,
            #        'time': time_list,
            #        'status': status,
            #        'day': day,
            #        'parsing time': time_now,
            #        'day_of_week': day_of_week_final_format,
            #        'date': date
            #        }
            add_to_db(room_number, time_list[0], status[0], day_of_week_final_format, date, time_now, sec_since_epoch)
            #schedule_list.append(info)
    #return schedule_list

def get_room_info(soup):  #Парсим все комнаты и их описание
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
    
    create_logger()
    html = get_info()
    rooms = get_room_info(html)
    dt = datetime.now()
    
    sec_since_epoch = int (mktime(dt.timetuple()) + dt.microsecond/1000000)
    for room1, room2 in rooms.items():
        get_room_schedule(html, room2, room1,sec_since_epoch)
    logging.info('Parsed to DataBase')
    delete_expired_data()
    logging.info('Deleted expired data')

    logging.info('Number of rows in database = '+get_log())
    logging.info('Parsing time ---- '+str(dt))
  



if __name__ == "__main__":
    get_all_rooms_schedule()
    
