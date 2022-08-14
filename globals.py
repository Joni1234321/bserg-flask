from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
import os
import certifi

load_dotenv()

ca = certifi.where()

uri = os.getenv("MONGO_URI")
name = os.getenv("MONGO_DB_NAME")
mil_db_name = os.getenv("MIL_DB_NAME")

client = MongoClient(uri, tlsCAFile=ca)
db = client[name]
mil_db = client[mil_db_name]


def id_query(object_id):
    return {"_id": ObjectId(object_id)}
