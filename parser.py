from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def get_info():
    try:
        browser = webdriver.PhantomJS(executable_path='/Users/danilasokolov/Downloads/phantomjs')
        browser.get('https://chaykastudia.ru/onlajn-bronirovanie/repeticionnye-komnaty/')
        html = browser.page_source
        return html
    except(WebDriverException):
        print('Network Error')
        return False


def get_room_scheldue(html, room_number, room_number_parsing):
    room_number = "Комната " + str(room_number)
    soup = BeautifulSoup(html, 'html.parser')
    room_tag = soup.find(class_=str(room_number_parsing)) # находим нашу комнату
    tr_tag = (room_tag.find('tbody')).find_all('tr')  # ищем все тэги 'tr' 
    scheldue_list = []
    for every_tr in tr_tag:
        td_tag = every_tr.find_all('td')    #берем все тэги 'td', где лежит день недели и статус
        time = every_tr.find_all('th', class_='leftcol')  # находим время репетиций 
        time_list = [i.get_text() for i in time]        # и делаем список времени
        for every_td in td_tag:
            status = every_td.get('class')
            day = every_td.get('data-wday')
            day_format = day.replace('<span>', '') #избавляемся от лишнего текста 
            day_final_format = day_format.replace('</span>', '')
            info = {
                    'room': room_number,
                    'time': time_list,
                    'status': status,
                    'day': day_final_format
            }
            scheldue_list.append(info)

    return scheldue_list


def get_all_rooms_scheldue():
    data_room1 = get_room_scheldue(html_link, "1", "room0")
    data_room1_1 = get_room_scheldue(html_link, "1", "room1")  #тут парсинг для времени 21-24,которое лежит на сайте отдельно 
    data_room2 = get_room_scheldue(html_link, "2", "room2")
    data_room2_1 = get_room_scheldue(html_link, "2", "room3")  #тут парсинг для времени 21-24,которое лежит на сайте отдельно 
    data_room3 = get_room_scheldue(html_link, "3", "room4")
    data_room3_1 = get_room_scheldue(html_link, "3", "room5")  #тут парсинг для времени 21-24,которое лежит на сайте отдельно 
    data_room4 = get_room_scheldue(html_link, "4", "room6")
    data_room4_1 = get_room_scheldue(html_link, "4", "room7")  #тут парсинг для времени 21-24,которое лежит на сайте отдельно 
    data_all = data_room1 + data_room1_1 + data_room2 + data_room2_1 + data_room3 + data_room3_1 + data_room4 + data_room4_1
    print(data_all)
    return data_all
        
              
if __name__ == "__main__":
        
    html_link = get_info()
    get_all_rooms_scheldue()  
