import pymongo
import random

class Connexion:
    @classmethod
    def connect(cls):
        return pymongo.MongoClient(f"mongodb://mongodb:27017/")
    
    @classmethod
    def open_connexion(cls):
        cls.client = cls.connect()
        cls.collection = cls.client.chatbot.data

    @classmethod
    def close_connexion(cls):
        cls.client.close()

    @classmethod
    def get_response(cls, person, tag):
        cls.open_connexion()
        result = list(cls.collection.find({person: 1, 'tag': tag}, {'_id': 0, 'reponses': 1}))
        cls.close_connexion()
        return random.choice(result[0]['reponses'])

    @classmethod
    def get_questions(cls, tag):
        cls.open_connexion()
        if tag == None:
            result = list(cls.collection.find({}, {'_id': 0, 'tag': 1, 'questions': 1}))
        else:
            result = list(cls.collection.find({'tag': tag}, {'_id': 0, 'tag': 1, 'questions': 1}))
        cls.close_connexion()
        return result

    @classmethod
    def insert_question(cls, tag, question):
        cls.open_connexion()
        cls.collection.update({'tag': tag}, {'$push': {'questions': question}})
        result = list(cls.collection.find({'tag': tag}, {'_id': 0, 'questions': 1}))
        cls.close_connexion()
        return len(result[0]['questions'])