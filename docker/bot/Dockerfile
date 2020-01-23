FROM python:3.7



COPY requirements.txt /tmp
WORKDIR /tmp
VOLUME  /tmp 

RUN pip install -r requirements.txt

COPY . /tmp




CMD [ "python","bot.py" ]    