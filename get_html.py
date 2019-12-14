from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.common.exceptions import  WebDriverException


def get_info():
    try:

        browser = webdriver.PhantomJS(executable_path='/Users/danilasokolov/Downloads/phantomjs')
        browser.get('https://chaykastudia.ru/onlajn-bronirovanie/repeticionnye-komnaty/')
        html = browser.page_source
        return html
    except(WebDriverException):
        print('Сетевая ошибка')
        return False
        
def get_python_parser(html):

    soup = BeautifulSoup(html, 'html.parser')
    room = soup.find('tbody') #Берем таблицу для комнаты
    
    try:
        y = room.find_all('tr') # берем расписание 
        
        if y is not None:
            time = room.find_all('th',class_ = 'leftcol') #Выводит время  комнаты 
            time_list = [i.get_text() for i in time]
            y = y[1:]
            rooms_scajual = []
            
            for i in y:
                rooms_scajual.append(i.find_all('td'))  #выводит день недели и статус комнаты 
            
            together_list = zip(time_list,rooms_scajual) #объединяет время с днем недели и статусом комнаты
            
            for i in together_list:         #печатать каждое время со статусом комнат с новой строчки
                print(i)
            
            
        else:
            print('none')
    
    except(AttributeError):
        print('Не спарсил')
   

    return soup.prettify()
    
  
    


        
if __name__ == "__main__":
    get_info()
    html_link = get_info()
    get_python_parser(html_link)
    #saving = get_python_parser(html_link)
    #with open("parsing_link.html", "w", encoding="utf8") as f:
            #f.write(saving)
