from backend.db import execute_query
from backend.chat.llm import add_function_message, chat
from backend.retrieval_decision.llm import decide_retrieval
from backend.text2query.llm import write_nosql_query
from backend.pbac import filter, verify_query
from backend.config.model import Response
import logging

logger = logging.getLogger()

def run(user_input: str, chat_history: list = [], access_purpose: str = None):
    def run_with_retrieval(user_input: str, chat_history: list = [], access_purpose: str = None, retry: bool = False, response: Response = Response()):
        if response.query and response.error_msg is not None:
            hint = f"The previous retrieval failed.\n{str(response.error_msg)}\nQuery:{str(response.query)}\nTry to correct the query."
            hint = hint.replace("{","{{").replace("}","}}")
            response.action, response.query, response.limit = write_nosql_query(user_input, access_purpose, response.limit, hint)

        response.action, response.query, response.limit = write_nosql_query(user_input, access_purpose)
        response.valid, error = verify_query(response.query)

        if not response.valid:
            response.error_msg = f"The retrieval failed due to an invalid query. Error: {error}."

        if response.valid:
            response.result, e = execute_query(response.action, response.query, response.limit)
            if e:
                response.error_msg = f"The retrieval failed due to an error with the database. {e}."
            else:
                result = filter(response.action, response.result, access_purpose)
                context = f'Query:{response.action} {response.query}.\nResult: {result}.'
                chat_history = add_function_message(context,'retrival', chat_history)
                response.llm_response = chat(user_input, chat_history)
                return response
            
        if retry:
            logger.error(f"Retrieval failed. {response.error_msg}. Retrying...")
            return run_with_retrieval(user_input, chat_history, access_purpose, False, response)
        else:
            response.llm_response = chat(user_input, chat_history)
            return response

    if access_purpose is None:
        return "Please provide an access purpose.", Response()
    
    response = Response()
    response.retrival = decide_retrieval(user_input) == 'True'

    if not response.retrival:
        response.llm_response = chat(user_input, chat_history)
        return response
        
    else:
        return run_with_retrieval(user_input, chat_history, access_purpose, True, response)



def test():
    print(run('Hi', [], 'Research'))


if __name__ == "__main__":
   test()

    