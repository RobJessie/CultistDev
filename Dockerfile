FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U --upgrade-strategy eager discord-py

COPY . .

RUN apt-get update

CMD ["python3","main.py"]