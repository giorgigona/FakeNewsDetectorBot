from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import pandas as pd

def read_data(dataset_name, label):
    with open(dataset_name) as f:
        lines = f.readlines()
        
    df = pd.DataFrame(lines, columns = ['text'])
    mask = df['text'] != '\n'

    df['label'] = label
    return df[mask].copy()

def get_trained_model(vec_size, tagged_data):
    max_epochs = 100
    alpha = 0.025

    model = Doc2Vec(vector_size=vec_size,
                  alpha=alpha, 
                  min_alpha=0.00025,
                  min_count=1,
                  dm =1)

    model.build_vocab(tagged_data)

    for epoch in range(max_epochs):
        print('iteration {0}'.format(epoch))
        model.train(tagged_data,
                  total_examples=model.corpus_count,
                  epochs=10)
        # print(tagged_data)

        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha
  
    return model

def predict(model, sentences):
    vectors = list()
    for x in sentences:
        tokenized = word_tokenize(x.lower())
        vector = model.infer_vector(tokenized)
        vectors.append(vector)
    return vectors
