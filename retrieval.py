from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX

from classification import pbac_prompt_classification_llm
from config import PURPOSE_CODES

RETRIEVAL_PRE_SUFFIX = """You must always filter the query results to only include data where "Intended Purpose" contains: """

def pbac_retrieval_prompt(db, purpose):
    if db.dialect in SQL_PROMPTS:
        prompt = SQL_PROMPTS[db.dialect]
    else:
        prompt = PROMPT
    custom_prompt_suffix = RETRIEVAL_PRE_SUFFIX + purpose + '\n\n' + PROMPT_SUFFIX
    prompt.template = str.replace(prompt.template, PROMPT_SUFFIX, custom_prompt_suffix)

    return prompt

class RetrievalChainInput(BaseModel):
    user_prompt: str = Field(description="the original user prompt")
    #chat_history: str = Field(description="the chat history")

@tool(args_schema=RetrievalChainInput)
def sql_retrieval_chain_tool(user_prompt: str) -> str:
    """SQL chain that writes and executes sql queries on a private database. The tool takes the original input and relevant instructions as context."""  
    pbac_prompt_classification_response = pbac_prompt_classification_llm(user_prompt)
    if pbac_prompt_classification_response.get('error'):
        return pbac_prompt_classification_response
    if pbac_prompt_classification_response.get('purpose') == 'None':
        return pbac_prompt_classification_response

    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    user_prompt = pbac_retrieval_prompt(db, pbac_prompt_classification_response['purpose'])
    chain = create_sql_query_chain(llm, db, k=5, prompt=user_prompt)
    query = chain.invoke({"question": user_prompt})
    results = db.run(query)
    response = f'Prompt Classification: {pbac_prompt_classification_response}\nQuery: {query}\nResults: {results}'
    return response

class RetrievalToolInput(BaseModel):
    user_prompt: str = Field(description="the original user prompt")
    access_purpose: str = Field(description="the access purpose of the retrieval request")

@tool(args_schema=RetrievalToolInput)
def sql_retrieval_tool(user_prompt: str, access_purpose: str) -> str:
    """SQL chain that writes and executes sql queries on a private database. The tool takes the original user input and the access purpose as arguments. Always identify the access purposes using pbac_prompt_classification_tool before calling this tool."""  
    #@TODO add access purpose check

    if access_purpose not in PURPOSE_CODES:
        access_purpose = pbac_prompt_classification_llm(user_prompt)
        access_purpose = access_purpose['purpose']

    try:
        db_path = "sqlite:///sqlite_medical.db"
        db = SQLDatabase.from_uri(db_path)
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        prompt = pbac_retrieval_prompt(db, access_purpose)
        chain = create_sql_query_chain(llm, db, k=5, prompt=prompt)
        query = chain.invoke({"question": user_prompt})
        results = db.run(query)
        response = f'Query: {query}\nResults: {results}'
    except Exception as e:
        response = f'An error occured: {str(e)}. Query: {query}'
    return response

#print(sql_retrieval_chain_tool("Find all feamale patients with cancer that I can contact for marketing a new drug."))
#print(sql_retrieval_chain_tool("How many vists in the dataset?"))