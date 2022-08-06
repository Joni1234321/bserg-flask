from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

uri = os.getenv("MONGO_URI")
name = os.getenv("MONGO_DB_NAME")

client = MongoClient(uri)
db = client[name]


def id_query(object_id):
    return {"_id": ObjectId(object_id)}
