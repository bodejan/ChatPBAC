from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger()


def connect() -> MongoClient:
    """
    Connects to the MongoDB server using the provided DB_URI environment variable.

    Returns:
        MongoClient: A client object representing the connection to the MongoDB server.

    Raises:
        PyMongoError: If there is an error connecting to the MongoDB server.
    """
    try:
        # Create a new client and connect to the server
        client = MongoClient(os.getenv("DB_URI"), server_api=ServerApi('1'))
        return client
    except PyMongoError as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


def test():
    """
    Function to test the connection to MongoDB.

    Raises:
        PyMongoError: If there is an error during the ping.

    Prints:
        - "Pinged your deployment. You successfully connected to MongoDB!" if the ping is successful.
        - "Error during ping: {error_message}" if there is an error during the ping.

    """
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


def find(query: dict, k: int) -> tuple[list[dict], str | None]:
    """
    Find documents in the database collection based on the given query.

    Args:
        query (dict): The query to filter the documents.
        k (int): The maximum number of documents to return.

    Returns:
        tuple[list[dict], str | None]: A tuple containing the list of found documents and an error message if an error occurred, otherwise None.
    """
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION"))
        results = collection.find(query).limit(k)
        results = list(results)
        return results, None
    except PyMongoError as e:
        logger.error(f"Error during find operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()


def count(query: dict) -> tuple[int, str | None]:
    """
    Counts the number of documents in a collection that match the given query.

    Args:
        query (dict): The query to filter the documents.

    Returns:
        tuple[int, str | None]: A tuple containing the count of matching documents and an error message if an error occurs, otherwise None.
    """
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION"))
        count = collection.count_documents(query)
        return count, None
    except PyMongoError as e:
        logger.error(f"Error during count operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()


def aggregate(pipeline: list) -> tuple[list[dict], str | None]:
    """
    Executes an aggregate operation on the database collection.

    Args:
        pipeline (list): The aggregation pipeline to be executed.

    Returns:
        tuple[list[dict], str | None]: A tuple containing the results of the aggregation operation
        and an error message if an error occurred, otherwise None.
    """
    client = None
    try:
        client = connect()
        db = client.get_database(os.getenv("DB_NAME"))
        collection = db.get_collection(os.getenv("DB_COLLECTION"))
        results = collection.aggregate(pipeline)
        results = list(results)
        return results, None
    except PyMongoError as e:
        logger.error(f"Error during aggregate operation: {e}")
        return [], str(e)
    finally:
        if client:
            client.close()


def execute_query(action: str, query: dict, k: int = 1) -> tuple[list[dict] | int, str | None]:
    """
    Executes a database query based on the given action.

    Args:
        action (str): The action to perform on the database. Possible values are 'find', 'countDocuments', and 'aggregate'.
        query (dict): The query parameters.
        k (int, optional): The number of documents to return. Defaults to 1.

    Returns:
        tuple[list[dict] | int, str | None]: A tuple containing the result of the query and an error message, if any.

    Raises:
        Exception: If an error occurs during query execution.
    """
    try:
        if action == 'find':
            return find(query, k)
        elif action == 'countDocuments':
            return count(query)
        elif action == 'aggregate':
            return aggregate(query)
    except Exception as e:
        logger.error(f"Error during query execution: {e}")
        return [], str(e)


if __name__ == "__main__":
    pass
