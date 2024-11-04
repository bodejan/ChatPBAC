from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import time

import os

start = time.time()

client = MongoClient(os.getenv("DB_URI"), server_api=ServerApi('1'))
query = {}
k = 1
db = client.get_database(os.getenv("DB_NAME"))
collection = db.get_collection(os.getenv("DB_COLLECTION"))
print(f"Before execution: {time.time() - start}")
results = collection.find(query).limit(k)
print(list(results))
print(f"Final: {time.time() - start}")

client.close()


