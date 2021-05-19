import requests
import string
import nltk
import json
import time

import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, LSTM , Dense,GlobalMaxPooling1D,Flatten
from tensorflow.keras.models import Model

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


class ModelTraining:
    def __init__(self, url):
        self.json = requests.get(url).json()
        self.df = pd.json_normalize(self.json['data']).explode('questions')

    def preprocess(self):
        self.df['questions'] = self.df['questions'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
        self.df['questions'] = self.df['questions'].apply(lambda wrd: ''.join(wrd))

        #tokenize les données (qui désigne le découpage en mots des différents documents qui constituent le corpus)
        self.tokenizer = Tokenizer(num_words=2000)
        self.tokenizer.fit_on_texts(self.df['questions'])
        self.X = self.tokenizer.texts_to_sequences(self.df['questions'])

        #application d'un padding
        self.X = pad_sequences(self.X)
        self.y = self.df['tag']

        # encodage des sorties
        le = LabelEncoder()
        self.y = le.fit_transform(self.df['tag'])

        # répartition en données de train et de test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

    def create_model(self):
        i = Input(shape=(self.X.shape[1],))
        x = Embedding(len(self.tokenizer.word_index)+1,10)(i)
        x = LSTM(10, return_sequences=True)(x)
        x = Flatten()(x)
        x = Dense(len(set(self.y)), activation="softmax")(x)
        self.model  = Model(i,x)

        #compilation du modèle
        self.model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])

    def train(self, epochs):
        #création du modèle
        self.create_model()
        #entraînement du modèle
        start_time = time.time()
        
        self.model.fit(self.X_train, self.y_train, epochs=epochs, validation_data=(self.X_test, self.y_test))
        
        end_time = time.time()
        
        return end_time - start_time

    def save(self, name):
        self.model.save(name)



model = ModelTraining('http://35.241.156.130:5000/questions')
model.preprocess()
temps = model.train(epochs=500)
model.save('model.h5')