from backend.db import execute_query
from backend.llm import decide_retrieval, write_nosql_query, chat
from backend.pbac import filter, verify_query
from backend.model import Context
import logging

logger = logging.getLogger()

def run(user_input: str, chat_history: list = [], access_purpose: str = None):
    def run_with_retrieval(user_input: str, chat_history: list = [], access_purpose: str = None, retry: bool = False, hint: str = ''):
        nosql_context = write_nosql_query(user_input, access_purpose)
        valid = nosql_context is not None and verify_query(nosql_context.query)

        if not valid:
            hint = f"The previous retrieval step failed. {nosql_context.query} is not valid."

        if valid:
            nosql_result_context, e = execute_query(nosql_context)
            if e:
                hint = f"The previous retrieval step failed. Query {nosql_context.query}\nError: {e}."
            else:
                nosql_result_filtered_context = filter(nosql_result_context, access_purpose)
                response, context = chat(user_input, chat_history, nosql_result_filtered_context)
                return response, context
            
        if retry:
            logger.error(f"Retrieval failed. Hint: {hint}. Retrying...")
            return run_with_retrieval(user_input, chat_history, access_purpose, False, hint)
        else:
            return chat(user_input, chat_history)

    if access_purpose is None:
        return "Please provide an access purpose.", Context()

    retrive = decide_retrieval(user_input) == 'True'

    if not retrive:
        return chat(user_input, chat_history)
    else:
        return run_with_retrieval(user_input, chat_history, access_purpose, True)



def test():
    print(run('Hi', [], 'Research'))


if __name__ == "__main__":
   test()

    