from db import execute_query
from llm import decide_retrieval, write_nosql_query, chat
from pbac import filter
from model import Context
import logging

logger = logging.getLogger()

def run(user_input: str, chat_history: list = [], access_purpose: str = None):
    logger.info(f"Start chat with user input: {user_input}, access purpose: {access_purpose}")
    if access_purpose is None:
        return "Please provide an access purpose.", chat_history, Context()

    # Decide if retrieval is necessary
    if decide_retrieval(user_input) == 'True':
        # Retrieve data
        nosql_context = write_nosql_query(user_input, access_purpose)
        nosql_result_context = execute_query(nosql_context)
        nosql_result_filtered_context = filter(nosql_result_context, access_purpose)
        response, chat_history, final_context = chat(user_input, [], nosql_result_filtered_context)
    else:
        response, chat_history, final_context = chat(user_input, chat_history)

    return response, final_context


if __name__ == "__main__":
    access_purpose = "Research"
    user_input_1 = "What is the most common age range of patients with diabetes?"
    user_input_2 = "Retrieve all records where the Diagnosis is 'Cancer'"
    _, _ = run(user_input_1, access_purpose)

    