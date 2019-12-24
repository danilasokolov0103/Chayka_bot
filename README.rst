Chayka Bot
==========
Telegram bot for practice rooms

Installing
----------
Для запуска необходимо установить все библиотеки из requirements.txt
.... code-block:: text
      pip install -r requirements.txt
Установить redis-server c помощью команд ниже:
.. code-block:: text
    #устанока redis-server
    $ brew install redis
    #после установки его нужно запустить командой 
    $ redis-server
    #далее открываем еще 2 окна терминала и запускаем сначала celery beat ,потом celery worker 
    celery -A periodic beat
    
    celery -A periodic worker

Настройка
--------- 
Также нужно скачать Chromedriver локально и указать его путь в parser.py
.. code-block:: text
    browser = webdriver.Chrome(executable_path='Путь к Chromedirver',options=chrome_options)
Ниже ссылка на сам драйвер

.. Chromedirver: https://chromedriver.chromium.org/downloads
        