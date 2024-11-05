from pbac_rag.db import execute_query
from pbac_rag.chat.llm import format_retrieval_context, chat
from pbac_rag.retrieval_decision.llm import decide_retrieval
from pbac_rag.query_generation.llm import write_nosql_query_no_pbac
from pbac_rag.pbac import filter_results, validate_query, re_write_query
import logging
from typing import Literal

logger = logging.getLogger()


class Response:
    """
    Represents a response object.

    Attributes:
        retrieval (bool): Indicates whether the response is a retrieval.
        action (Literal['find', 'countDocuments', 'aggregate']): The action performed.
        query (dict): The query used.
        limit (int): The limit applied.
        result (list | int): The result of the action.
        error_msg (str): The error message, if any.
        llm_response (str): The LLM response.
        valid (bool): Indicates whether the query is valid.

    Methods:
        __repr__(self) -> dict: Returns a string representation of the response object.
    """

    retrieval: bool
    action: Literal['find', 'countDocuments', 'aggregate']
    query: dict
    limit: int
    result: list | int
    error_msg: str
    llm_response: str
    valid: bool

    def __repr__(self) -> dict:
        return str(self.__dict__)


def run(user_input: str, chat_history: list = [], access_purpose: str = None) -> Response:
    """
    Executes the main logic of the program.

    Args:
        user_input (str): The user's input.
        chat_history (list, optional): The chat history. Defaults to an empty list.
        access_purpose (str, optional): The purpose of accessing the data. Defaults to None.

    Returns:
        The result of the PBAC-RAG chat interaction.
    """

    response = Response()
    response.retrieval = decide_retrieval(user_input)

    if not response.retrieval:
        return run_without_retrieval(user_input, chat_history)
    else:
        return run_with_retrieval(user_input, chat_history, access_purpose)


def run_without_retrieval(user_input: str, chat_history: list = []) -> Response:
    """
    Run the chatbot without retrieval.
    Args:
        user_input (str): The user's input.
        chat_history (list, optional): The chat history. Defaults to [].
    Returns:
        Response: The chatbot response.
    """
    # If the retrieval is not needed, add empty message to avoid hallucinations.
    response = Response()
    response.retrieval = False
    response.llm_response = chat(user_input, chat_history)
    return response


def run_with_retrieval(user_input: str, chat_history: list = [], access_purpose: str = None, attempt: int = 1, response: Response = Response()) -> Response:
    """
    Runs the RAG with the given parameters.

    Args:
        user_input (str): The user input for the retrieval process.
        chat_history (list, optional): The chat history. Defaults to an empty list.
        access_purpose (str, optional): The access purpose. Defaults to None.
        attempt (int, optional): The number of attempts. Defaults to 1.
        response (Response, optional): The response object. Defaults to an instance of Response.

    Returns:
        Response: The response object containing the retrieval results.
    """
    response.retrieval = True

    if attempt > 1:
        hint = f"The previous retrieval failed.\n{str(response.error_msg)}\nQuery:{str(response.query)}\nTry to correct the query."
        response.action, response.query, response.limit = write_nosql_query_no_pbac(
            user_input, hint=hint)
    else:
        response.action, response.query, response.limit = write_nosql_query_no_pbac(
            user_input)

    response.query = re_write_query(
        response.query, response.action, access_purpose)
    response.valid, response.error_msg = validate_query(response.query)

    if response.valid:
        response.result, e = execute_query(
            response.action, response.query, response.limit)
        if e:
            response.error_msg = f"The retrieval failed due to an error with the database. {e}."
            response.valid = False
        else:
            response.result = filter_results(response.action,
                                             response.result, access_purpose)
            context = format_retrieval_context(response.action, response.query, response.result)
            response.llm_response = chat(user_input, chat_history, context)
            return response

    if not response.valid and attempt < 3:
        run_with_retrieval(user_input, chat_history,
                           access_purpose, attempt + 1, response)
    else:
        # If the retrieval fails twice, the chatbot will continue without retrieval.
        run_without_retrieval(user_input, chat_history)


if __name__ == "__main__":
    pass
