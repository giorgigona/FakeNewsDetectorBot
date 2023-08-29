
import pickle
from telefone import Bot

from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

from langdetect import detect

import mysql.connector
import configparser

def predict(vectorizer_model, knn_model, d, msg):
    tokenized = word_tokenize(msg.lower())
    vector = vectorizer_model.infer_vector(tokenized)
    prediction = knn_model.predict([vector])[0]

    return d[prediction]



def get_config():
    config_data = configparser.ConfigParser()
    config_data.read('config.ini')
    return config_data

def get_db_connection(sql_credentials):
    host = sql_credentials['host']
    port = sql_credentials['port']
    user = sql_credentials['user']
    password = sql_credentials['password']
    database = sql_credentials['database']

    # Create a connection to the database
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )

    return connection

def log_message_into_db(sql_credentials, message_text, response_text, prediction):

    try:
        connection = get_db_connection(sql_credentials)
        cursor = connection.cursor()
        insert_query = "INSERT INTO TelegramBotLog (message_text, response_text, prediction) VALUES (%s, %s, %s)"
        data_to_insert = (message_text, response_text, prediction)

        cursor.execute(insert_query, data_to_insert)
        # Commit the transaction
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()

    except Exception as e:
        print(e)

def check_message_info(message_text):

    detected_language = detect(message_text)

    if len(message_text.split()) < 5:
        return "Please provide more information for prediction."

    if detected_language != 'en':
        return "Please provide information in English text."

    return ""