from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

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
    collection = db.get_collection(os.getenv("DB_COLLECTION"))

    results = collection.find(query, {"_id": 0}).limit(k)
    results = list(results)
    client.close()

    return results


def count(query):
    client = connect()
    db = client.get_database(os.getenv("DB_NAME"))
    collection = db.get_collection(os.getenv("DB_COLLECTION"))

    count = collection.count_documents(query)
    client.close()

    return count


def close(client):
    client.close()


if __name__ == "__main__":
    pass