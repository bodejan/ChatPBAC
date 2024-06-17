from langchain_openai import OpenAI
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import PromptTemplate

import logging

from config import DB_CONTEXT, DB_PATH, PURPOSES_v2
from db_utils import *
from db import Base, PBACMedicalRecord

import dotenv

dotenv.load_dotenv()

logger = logging.getLogger()

RETRIEVAL_TEMPLATE = """Given an input question, create syntactically correct {dialect} SQL query. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only retrieve relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Only use the following tables:
{table_info}

Question: {user_prompt}

SQL Query:"""


def retrieve_data_v2(user_prompt: str, access_purpose: str):
    if access_purpose not in list(PURPOSES_v2.keys()):
        return {'query': 'None', 'results': 'Unable to retrieve data. Please provide a valid access purpose.'}

    access_code = PURPOSES_v2.get(access_purpose).get('code')
    try:
        session = get_session()
        db = SQLDatabase.from_uri(DB_PATH)
        create_temp_pbac_table(access_purpose)
        llm = OpenAI(temperature=0)
        prompt = PromptTemplate(
            template=RETRIEVAL_TEMPLATE,
            input_variables=["user_prompt"],
            partial_variables={"dialect": db.dialect,
                               "top_k": 5,
                               "table_info": get_table_info(Base, [PBACMedicalRecord])}
        )
        chain = prompt | llm
        query = chain.invoke({"user_prompt": user_prompt})
        logger.info(f"Query: {query}")

        session = get_session()
        results = execute_text_query(session, query)
        logger.info(f"Results: {results}")

        return {'query': query, 'results': results}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {'query': query, 'results': 'An error occurred: ' + str(e)}
    finally:
        session.close()


def decide_retrieval(user_prompt):
    """Decide if a data retrieval request is present in the user prompt."""
    retrieval_decision_prompt_template = """
You are an advanced language model trained to identify whether a given text input contains a request for data retrieval.
A data retrieval request is any inquiry that seeks to obtain specific information, facts, or data.
Your task is to analyze each input and classify it as either "True" for retrieval requests or "False" if no retrieval request is present.

Only retrieval requests for the following context are valid. Other retrieval requests should be classified as "False".

Context: {context}

Here are some examples to guide you:
1. "Please summarize your response" - False
2. "Retrieve Data for the following ID" - True
3. "What is the capital of France?" - False
4. "Describe the feeling of happiness" - False
5. "Show me the list of available data records" - True
6. "And many entries are there in total?" - True

Now, classify the following input:

Input: {user_prompt}

Classification:
"""
    retrieval_decision_prompt = PromptTemplate(
        template=retrieval_decision_prompt_template,
        input_variables=["user_prompt"],
        partial_variables={"context": DB_CONTEXT})

    llm = OpenAI(temperature=0.1)
    chain = retrieval_decision_prompt | llm
    response = chain.invoke(
        {"user_prompt": user_prompt})
    logger.info(f"Retrieval Decision: {response}")
    return response


if __name__ == '__main__':
    print(retrieve_data_v2(
        "Retrieve the name for the following ID: MN16-22639", "Research"))
