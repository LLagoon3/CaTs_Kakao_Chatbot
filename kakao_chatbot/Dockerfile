FROM python:3.10.12

WORKDIR /home/api_server/kakao_chatbot

ADD . /home/api_server/kakao_chatbot

RUN apt-get update && apt-get install -y \
    libdbus-1-dev \
    libgirepository1.0-dev
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install dbus-python PyGObject
RUN pip install -r requirements.txt
RUN python manage.py makemigrations

