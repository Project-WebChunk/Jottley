from pymongo import MongoClient
from uuid import uuid4
import random
import datetime
import requests

class Database:
    def __init__(self, URL):
        self.client = MongoClient(URL)
        self.db = self.client.Snipper
        self.users = self.db.users
        self.snips = self.db.snips
        
    def addUser(self, email):
        name = requests.get('http://names.drycodes.com/1').json()[0]
        id =str(uuid4())
        self.users.insert_one({
            '_id': id,
            'username': name,
            'email': email,
            'created': datetime.datetime.now().strftime("%d %B %Y, %I:%M:%S %p")
        })
    
    def userExists(self, email):
        return self.users.find_one({'email': email}) is not None
    
    def getUser(self, email):
        return self.users.find_one({'email': email})
    
    def getUserWithId(self, id):
        return self.users.find_one({'_id': id})
    
    def updateName(self, email, name):
        self.users.update_one({'email': email}, {'$set': {'username': name}})
        return True