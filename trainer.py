import numpy as np 
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
import nltk
nltk.download('punkt')

from gensim.models.doc2vec import TaggedDocument
from nltk.tokenize import word_tokenize

from training_utils import *
import pickle


df = pd.concat([read_data('data/truth_sample.txt', 0), read_data('data/fakes_sample.txt', 1)], axis=0)
df = df.sample(frac=1)
df.reset_index(inplace=True, drop=True)

data = df['text']
tagged_tex = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

model_tex = get_trained_model(64, tagged_tex)

X = predict(model_tex, data)
y = df['label']

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

model_tex.save("trained_models/text_vectorizer.model")

with open('trained_models/knn.model', 'wb') as files:
    pickle.dump(knn, files)


