FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install pyTelegramBotAPI
RUN pip3 install nltk==3.7
RUN pip3 install scikit-learn==1.1.2
RUN pip3 install gensim
RUN pip3 install langdetect
RUN pip3 install mysql-connector-python

COPY . .

CMD [ "python3", "./main.py"]