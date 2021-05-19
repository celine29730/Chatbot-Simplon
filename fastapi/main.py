import random
import json
import pickle
import string
from fastapi import FastAPI
from connexion import Connexion
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/reponse")
async def get_reponse(person: str=None, tag:str=None):
    if person == None or tag == None:
        return {'error': 'enter the parameters (person, tag)'}

    reponse = Connexion.get_response(person, tag)
    return {"reponse": reponse}


@app.get("/questions")
async def get_questions(tag:str=None):
    
    data = Connexion.get_questions(tag)

    return {"data": data}

@app.get("/add_question")
async def add_question(tag: str, question:str):
    try:
        Connexion.insert_question(tag, question)
        return {"message": f'Question inserée pour le tag {tag}. Il y a maintenant {nb} questions pour ce tag'}
    except:
        return {"error": 'Format incorrect'}

@app.post('/predict')
async def predict(phrase:str, person:str):
    model = tf.keras.models.load_model('model.h5')
    tokenizer_file = open('tokenizer.pickle', 'rb')
    tokenizer = pickle.load(tokenizer_file)
    encoder_file = open('encoder.pickle', 'rb')
    encoder = pickle.load(encoder_file)

    phrase = [ltrs.lower() for ltrs in phrase if ltrs not in string.punctuation]

    phrase = tokenizer.texts_to_sequences(phrase)
    phrase = pad_sequences(phrase)

    prediction = model.predict(phrase)

    tag = encoder.inverse_transform(prediction)

    reponse = requests.get(f'http://35.241.156.130:8080/reponse?tag={tag}&person={person}').json()

    return reponse



# @app.get("/train")
# async def train_model(epochs:int=100):
#     model = ModelTraining('http://35.241.156.130:5000/questions')
#     model.preprocess()
#     temps = model.train(epochs=epochs)
#     model.save('model.h5')

#     return {'message': f'Model entrainé en {round(temps, 2)} secondes'}