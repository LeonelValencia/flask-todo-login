import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

load_dotenv()
# Replace the placeholder with your Atlas connection string
MONGODB_URI = os.environ["MONGODB_URI"]

# Set the Stable API version when creating a new client
client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
                          
db = client["regulondb-flask"]
collection = db.users

def get_users():
    return collection.find()

def get_user(user_id):
    return collection.find_one({'user': user_id})

def put_user(user_data):
    collection.insert_one({"user": user_data.username, "password": user_data.password})

def get_todos(username):
    return collection.find_one({'user': username}).get('todos')

def put_todo(description, username):
    nuevo_todo = {'_id': ObjectId(), 'description': description, 'done': False}
    collection.update_one({'user': username}, {'$push': {'todos': nuevo_todo}})

def delete_todo(todo_id, username):
    id_object = ObjectId(todo_id)
    collection.update_one({'user': username}, {'$pull': {'todos': {'_id': id_object}}})
