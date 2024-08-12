from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from model import Context
import logging

load_dotenv()
logger = logging.getLogger()

def connect():
    # Create a new client and connect to the server
    client = MongoClient(os.getenv("DB_URI"), server_api=ServerApi('1'))

    return client

def test():
    client = connect()
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    close(client)


def find(query, k: int = 10):
    client = connect()
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))

    results = collection.find(query, {"_id": 0}).limit(k)
    results = list(results)
    client.close()

    return results


def count(query):
    client = connect()
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))

    count = collection.count_documents(query)
    client.close()

    return count

def aggregate(pipeline):
    client = connect()
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))

    results = collection.aggregate(pipeline)
    results = list(results)
    client.close()

    return results

def execute_query(context: Context, k: int = 5):
    if context.action == 'find':
        context.result = find(context.query, k)
    elif context.action == 'countDocuments':
        context.result = count(context.query)
    elif context.action == 'aggregate':
        context.result = aggregate(context.query)
    logger.info(f"Retrieval Result: {context.result}")
    return context


def close(client):
    client.close()


if __name__ == "__main__":
    pipeline= [{'$group': {'_id': '$ReportYear', 'count': {'$sum': 1}}}]
    print(aggregate(pipeline))