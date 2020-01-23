FROM python:3.7

RUN apt-get update 
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils

#download and install chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Задаём текущую рабочую 
ADD . /usr/src/my_app_directory
WORKDIR /usr/src/my_app_directory

# Копируем код из локального контекста в рабочую директорию образа
COPY . .
# Задаём значение по умолчанию для переменной
ARG my_var=my_default_value
# Настраиваем команду, которая должна быть запущена в контейнере во время его выполнения
#ENTRYPOINT ["celery", "-A", "periodic", "beat"]
RUN pip install -r requirements.txt
# Открываем порты
EXPOSE 8000
# Создаём том для хранения данных
VOLUME /my_volume





CMD ["make"]   