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
Устанока redis-server
.. code-block:: text
    $ brew install redis
После установки его нужно запустить командой 
.. code-block:: text
    $ redis-server
Далее открываем еще 2 окна терминала и запускаем сначала celery beat ,потом celery worker 
.. code-block:: text
    celery -A periodic beat

.. code-block:: text
    celery -A periodic worker

Настройка
--------- 
Также нужно скачать Chromedriver локально и указать его путь в parser.py
.. code-block:: text
    browser = webdriver.Chrome(executable_path='Путь к Chromedirver',options=chrome_options)
Ниже ссылка на сам драйвер

.. Chromedirver: https://chromedriver.chromium.org/downloads
        