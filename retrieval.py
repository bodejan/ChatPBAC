from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX

from classification import pbac_prompt_classification, pbac_prompt_classification_llm



RETRIEVAL_PRE_SUFFIX = """You must always filter the query results to only include data where "Intended Purpose" contains: """

def pbac_retrieval_prompt(db, purpose):
    if db.dialect in SQL_PROMPTS:
        prompt = SQL_PROMPTS[db.dialect]
    else:
        prompt = PROMPT
    custom_prompt_suffix = RETRIEVAL_PRE_SUFFIX + purpose + '\n\n' + PROMPT_SUFFIX
    prompt.template = str.replace(prompt.template, PROMPT_SUFFIX, custom_prompt_suffix)

    return prompt

@tool
def sql_retrieval_chain_tool(input: str) -> str:
    """SQL chain that writes and executes sql queries on a private database."""  
    purpose = pbac_prompt_classification_llm(input)
    #@TODO handle errors etc.

    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = pbac_retrieval_prompt(db, purpose)
    chain = create_sql_query_chain(llm, db, k=5, prompt=prompt)
    query = chain.invoke({"question": input})
    results = db.run(query)
    response = f'Query: {query}\nResults: {results}'
    return response

#print(sql_retrieval_chain_tool("Find all feamale patients with cancer that I can contact for marketing a new drug."))

