from telefone import Bot

from gensim.models.doc2vec import Doc2Vec
import pickle
from nltk.tokenize import word_tokenize


bot = Bot("5375634736:AAEKhrNYg7bpoDJ0ykzOZXtdll52WDKrXLw")

d = {
    0 : 'Truth',
    1 : 'Fake'
}

text_vectorizer_model = Doc2Vec.load("trained_models/text_vectorizer.model")
with open('trained_models/knn.model' , 'rb') as f:
    knn = pickle.load(f)

def predict(vectorizer_model, knn_model, msg):
    tokenized = word_tokenize(msg.lower())
    vector = vectorizer_model.infer_vector(tokenized)
    prediction = knn_model.predict([vector])[0]

    return d[prediction]

@bot.on.message()
async def handler(msg) -> str:
    message_text = msg.text
    prediction = predict(text_vectorizer_model, knn, message_text)
    first_name = msg.from_.first_name

    return "Hi, {} This news sounds like {}".format(first_name, prediction)

bot.run_forever()