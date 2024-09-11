from backend.db import execute_query
from backend.chat.llm import add_function_message, chat
from backend.retrieval_decision.llm import decide_retrieval
from backend.text2query.llm import write_nosql_query_no_pbac
from backend.pbac import filter_results, verify_query, re_write_query
import logging
from typing import Literal

logger = logging.getLogger()


class Response:
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


def run_without_retrieval(user_input: str, chat_history: list = []):
    # If the retrieval is not needed, add empty message to avoid hallucinations.
    response = Response()
    response.retrieval = False
    chat_history = add_function_message('None', 'retrieval', chat_history)
    response.llm_response = chat(user_input, chat_history)
    return response


def run_with_retrieval(user_input: str, chat_history: list = [], access_purpose: str = None, attempt: int = 1, response: Response = Response()):
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
    response.valid, response.error_msg = verify_query(response.query)

    if response.valid:
        response.result, e = execute_query(
            response.action, response.query, response.limit)
        if e:
            response.error_msg = f"The retrieval failed due to an error with the database. {e}."
            response.valid = False
        else:
            response.result = filter_results(response.action,
                                             response.result, access_purpose)
            context = f'Query:{response.action}({response.query}).\nResult: {response.result}.'
            chat_history = add_function_message(
                context, 'retrieval', chat_history)
            response.llm_response = chat(user_input, chat_history)
            return response

    if not response.valid and attempt < 3:
        run_with_retrieval(user_input, chat_history,
                           access_purpose, attempt + 1, response)
    else:
        # If the retrieval fails twice, the chatbot will continue without retrieval.
        run_without_retrieval(user_input, chat_history)


def run_neo(user_input: str, chat_history: list = [], access_purpose: str = None):
    response = Response()
    response.retrieval = decide_retrieval(user_input)

    if not response.retrieval:
        return run_without_retrieval(user_input, chat_history)
    else:
        return run_with_retrieval(user_input, chat_history, access_purpose)


def run(user_input: str, chat_history: list = [], access_purpose: str = None):
    def run_with_retrieval(user_input: str, chat_history: list = [], access_purpose: str = None, retry: bool = False, response: Response = Response()):
        if response.query and response.error_msg is not None:
            hint = f"The previous retrieval failed.\n{str(response.error_msg)}\nQuery:{str(response.query)}\nTry to correct the query."
            hint = hint.replace("{", "{{").replace("}", "}}")
            response.action, response.query, response.limit = write_nosql_query_no_pbac(
                user_input, response.limit, hint)

        response.action, response.query, response.limit = write_nosql_query_no_pbac(
            user_input)
        response.query = re_write_query(
            response.query, response.action, access_purpose)
        response.valid, error = verify_query(response.query)

        if not response.valid:
            response.error_msg = f"The retrieval failed due to an invalid query. Error: {error}."

        if response.valid:
            response.result, e = execute_query(
                response.action, response.query, response.limit)
            if e:
                response.error_msg = f"The retrieval failed due to an error with the database. {e}."
            else:
                response.result = filter_results(response.action,
                                                 response.result, access_purpose)
                context = f'Query:{response.action} {response.query}.\nResult: {response.result}.'
                chat_history = add_function_message(
                    context, 'retrieval', chat_history)
                response.llm_response = chat(user_input, chat_history)
                return response

        if retry:
            logger.error(
                f"Retrieval failed. {response.error_msg}. Retrying...")
            return run_with_retrieval(user_input, chat_history, access_purpose, False, response)
        else:
            # If the retrieval fails twice, the chatbot will continue without retrieval.
            chat_history = add_function_message(
                'None', 'retrival', chat_history)
            response.llm_response = chat(user_input, chat_history)
            return response

    if access_purpose is None:
        return "Please provide an access purpose.", Response()

    response = Response()
    response.retrieval = decide_retrieval(user_input)

    if not response.retrieval:
        # If the retrieval is not needed, add empty message to avoid hallucinations.
        chat_history = add_function_message('None', 'retrieval', chat_history)
        response.llm_response = chat(user_input, chat_history)
        return response

    else:
        return run_with_retrieval(user_input, chat_history, access_purpose, True, response)


def test():
    print(run('Hi', [], 'Research'))


if __name__ == "__main__":
    test()
