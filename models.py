from pymongo import MongoClient
from bson.objectid import ObjectId

class Question:
   client = MongoClient('mongodb+srv://testdb:testdb@cluster0.ovrarc4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
   db = client['exam_database']
   collection = db['exam_questions']

@staticmethod
def insert_question(question_data):
    return Question.questions_collection.insert_one(question_data).inserted_id

@staticmethod
def get_all_questions():
    return list(Question.questions_collection.find())

@staticmethod
def update_question(question_id, updated_data):
    Question.questions_collection.update_one({'_id': ObjectId(question_id)}, {'$set': updated_data})

@staticmethod
def delete_question(question_id):
    Question.questions_collection.delete_one({'_id': ObjectId(question_id)})
