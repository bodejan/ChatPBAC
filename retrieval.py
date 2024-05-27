from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX
from langchain_core.prompts import PromptTemplate

import pandas as pd
import logging

from config import DB_CONTEXT, PURPOSE_CODES, DB_PATH

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


def decide_retrieval(user_prompt, chat_history):
    """Decide if a data retrieval request is present in the user prompt."""
    retrieval_decision_prompt_template = """
You are an advanced language model trained to identify whether a given text input contains a request for data retrieval.
A data retrieval request is any inquiry that seeks to obtain specific information, facts, or data.
Your task is to analyze each input and classify it as either "True" for retrieval requests or "False" if no retrieval request is present.

Only retrieval requests for the following context are valid. Other retrieval requests should be classified as "False".

# Context: {context}

Here are some examples to guide you:
1. "Please summarize your response" - False
2. "Retrieve Data for the following ID" - True
3. "What is the capital of France?" - False
4. "Describe the feeling of happiness" - False
5. "Show me the list of available data records" - True
6. "And many entries are there in total?" - True

Now, classify the following input:

Chat history: {chat_history}
Input: {user_prompt}

Classification:
"""
    retrieval_decision_prompt = PromptTemplate(
        template=retrieval_decision_prompt_template,
        input_variables=["user_prompt", "chat_history"],
        partial_variables={"context": DB_CONTEXT})

    llm = OpenAI(temperature=0.1)
    chain = retrieval_decision_prompt | llm
    response = chain.invoke(
        {"user_prompt": user_prompt, "chat_history": chat_history})
    logger.info(f"Retrieval Decision: {response}")
    return response
