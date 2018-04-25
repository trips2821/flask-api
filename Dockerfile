from ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python-pip

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python app.py
