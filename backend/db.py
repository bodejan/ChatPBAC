from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os
from backend.model import Context
import logging

load_dotenv()
logger = logging.getLogger()

def connect():
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("DB_URI"), server_api=ServerApi('1'))
        return client
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise

def test():
    client = None
    try:
        client = connect()
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except PyMongoError as e:
        print(f"Error during ping: {e}")
    finally:
        if client:
            client.close()

def find(query: dict, k: int):
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))
        results = collection.find(query).limit(k)
        results = list(results)
        return results, None
    except PyMongoError as e:
        logger.error(f"Error during find operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()

def count(query: dict):
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))
        count = collection.count_documents(query)
        return count, None
    except PyMongoError as e:
        logger.error(f"Error during count operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()

def aggregate(pipeline: list):
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION_NAIVE"))
        results = collection.aggregate(pipeline)
        results = list(results)
        return results, None
    except PyMongoError as e:
        logger.error(f"Error during aggregate operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()

def execute_query(context: Context, k: int = 5):
    try:
        if context.action == 'find':
            if context.limit:
                k = context.limit
            result, error = find(context.query, k)
        elif context.action == 'countDocuments':
            result, error = count(context.query)
        elif context.action == 'aggregate':
            result, error = aggregate(context.query)
        context.result = result
        logger.info(f"Retrieval Results: {context.result}")
        return context, error
    except Exception as e:
        logger.error(f"Error during query execution: {e}")
        return context, str(e) 



if __name__ == "__main__":
    pass