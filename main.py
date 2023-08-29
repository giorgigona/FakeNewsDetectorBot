import pickle
import telebot

from utils import *

from gensim.models.doc2vec import Doc2Vec
import nltk
nltk.download('punkt')

config_data = get_config()
sql_credentials = config_data['mysql_database']
bot_credentials = config_data['telegram_bot_token']

bot = telebot.TeleBot(bot_credentials['token'])


d = {
    0 : 'Truth',
    1 : 'Fake'
}

text_vectorizer_model = Doc2Vec.load("trained_models/text_vectorizer_old.model")
with open('trained_models/knn_old.model' , 'rb') as f:
    knn = pickle.load(f)

@bot.message_handler(func=lambda message: True)
def handler(msg) -> str:
    try:

        message_text = msg.text
        defective_message_repsponse = check_message_info(message_text)

        if  defective_message_repsponse != "":
            bot.reply_to(msg, defective_message_repsponse)
            log_message_into_db(sql_credentials, message_text, defective_message_repsponse, 'Defective')
            return defective_message_repsponse

        prediction = predict(text_vectorizer_model, knn, d, message_text)
        first_name = msg.from_user.first_name
        response_message = "Hi, {} This news sounds like {}".format(first_name, prediction)

        bot.reply_to(msg, response_message)
        log_message_into_db(sql_credentials, message_text, response_message, prediction)

        return response_message

    except Exception as e: 
        print(e)
        return "Please provide more information."

bot.infinity_polling()



