Chayka Bot
==========
Телеграм бот для онлайн отслеживания расписания репетиционных комнат 

Настройка и запуск
------------------
Настройка 
---------
Для начала создайте .env файл, где будут лежать все настройки( токен для бота , адрес сайта ......) 
Требуемые значения можно посмотреть в файле settings.py

Запуск 
---------

Для начала нужно установить Docker и Docker-compose  
.. code-block:: text
    brew install docker docker-compose docker-machine xhyve docker-machine-driver-xhyve

Для запуска программы нужно сначала собрать все Docker контейнеры
.. code-block:: text
    docker-compose build

Для запуска программы нужно сначала собрать все Docker контейнеры
.. code-block:: text
    docker-compose up