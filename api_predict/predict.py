from flask import Flask
from corsheaders.defaults import default_headers
from flask_cors import CORS
from flask import request
import pickle
from keras.models import load_model
import string
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import requests

import json


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
    }
})

app.config['CORS_HEADERS'] = 'application/json'

@app.route('/<message>', methods=['GET'])
def login(message):
    print(message)
    if request.method == 'GET':
        #load tokenizer
        with open('/Users/guillaumeverpoest/Desktop/predict/model/api_predict/model/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)
            

        # load mapping
        with open('/Users/guillaumeverpoest/Desktop/predict/model/api_predict/model/data.json') as json_file:
            mapping = json.load(json_file)
            print(mapping)

        # load model
        model = load_model('/Users/guillaumeverpoest/Desktop/predict/model/api_predict/model/model.h5')

        texts_p = []
        prediction_input = [letters.lower() for letters in message if letters not in string.punctuation]
        prediction_input = ''.join(prediction_input)
        texts_p.append(prediction_input)

        prediction_input = tokenizer.texts_to_sequences(texts_p)
        prediction_input = np.array(prediction_input).reshape(-1)
        prediction_input = pad_sequences([prediction_input],11)  

        output = model.predict(prediction_input)
        #print(output.max())
        if output.max() < 0:
          tag = "je ne sais pas "
        else:
            output = output.argmax() 
            #print(output)
            tag = mapping[str(output)] 
            print(tag) 
        person = "etudiant"
        #tag="programme"
        reponse = requests.get(f'http://35.241.156.130:5000/reponse?tag={tag}&person={person}').json()
        #print(reponse)

        return {"reponse": reponse}


if __name__ == "__main__":
    app.run()
