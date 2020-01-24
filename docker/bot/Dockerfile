FROM python:3.7


RUN mkdir bot
COPY requirements.txt /bot
WORKDIR /bot


RUN pip install -r requirements.txt

COPY . /bot




CMD [ "python","bot.py" ]    