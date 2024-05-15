from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX

import pandas as pd
import logging

from config import PURPOSE_CODES, DB_PATH

logger = logging.getLogger()

RETRIEVAL_PRE_SUFFIX = """You must always filter the query results to only include data where "Intended Purpose" contains: """


def pbac_retrieval_prompt(db, purpose):
    if db.dialect in SQL_PROMPTS:
        prompt = SQL_PROMPTS[db.dialect]
    else:
        prompt = PROMPT
    custom_prompt_suffix = RETRIEVAL_PRE_SUFFIX + purpose + '\n\n' + PROMPT_SUFFIX
    prompt.template = str.replace(
        prompt.template, PROMPT_SUFFIX, custom_prompt_suffix)

    return prompt


def retrieve_data(user_prompt: str, access_purpose: str):
    if access_purpose not in PURPOSE_CODES:
        return {'query': 'None', 'results': 'Unable to retrieve data. Please provide a valid access purpose.'}

    try:
        db = SQLDatabase.from_uri(DB_PATH)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        prompt = pbac_retrieval_prompt(db, access_purpose)
        chain = create_sql_query_chain(llm, db, k=5, prompt=prompt)
        query = chain.invoke({"question": user_prompt})
        logger.info(f"Query: {query}")
        results = db.run(query)
        logger.info(f"Results: {results}")
        return {'query': query, 'results': results}
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {'query': query, 'results': 'An error occurred: ' + str(e)}
