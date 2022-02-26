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
        self.books = self.db.books

    def addUser(self, email):
        name = requests.get('http://names.drycodes.com/1').json()[0]
        id = str(uuid4())
        self.users.insert_one({
            '_id': id,
            'username': name,
            'email': email,
            'created': datetime.datetime.now().strftime("%d %B %Y, %I:%M:%S %p"),
            "books": []
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
    
    def generateID(self):
        return "".join(random.choice("0123456789ABCDEF") for i in range(10))

    def createBook(self, id, name):
        bookID = str(uuid4())
        book = {
            "_id": bookID,
            "name": name,
            "chapters": {},
            "chapterOrder": [],
            "by": id
        }
        self.books.insert_one(book)
        self.users.update_one({'_id': id}, {'$push': {'books': bookID}})

    def createChapter(self, bookID, name):
        chapterID = self.generateID()
        chapter = {
            "_id": chapterID,
            "name": name,
            "snippets": {},
            "snippetOrder": []
        }
        
        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapters.' + chapterID: chapter}})
        self.books.update_one(
            {'_id': bookID}, {'$push': {'chapterOrder': chapterID}})

    def createSnippet(self, bookID, chapterID, name):
        snippetID = self.generateID()
        snippet = {
            "_id": snippetID,
            "name": name,
            "content": ""
        }
        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapters.' + chapterID + '.snippets.' + snippetID: snippet}})
        self.books.update_one(
            {'_id': bookID}, {'$push': {'chapters.' + chapterID + '.snippetOrder': snippetID}})
        
    def getBook(self, bookID):
        return self.books.find_one({'_id': bookID})
    
    def getSnippet(self, bookID, chapterID, snippetID):
        book = self.books.find_one({'_id': bookID})
        return book['chapters'][chapterID]['snippets'][snippetID]
    
    def changeChapterOrder(self, bookID, chapterOrder):
        self.books.update_one(
            {'_id': bookID}, {'$set': {'chapterOrder': chapterOrder}})
    
    def changeSnippetOrder(self, bookID, chapterID, snippetOrder):
        self.books.update_one({'_id': bookID}, {'$set': {'chapters.' + chapterID + '.snippetOrder': snippetOrder}})