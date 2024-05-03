from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

from sql_agent import create_custom_sql_agent
from prompt_template import create_custom_sql_agent_prompt
from prompt import RETRIEVAL_PRE_SUFFIX
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX

import sqlite3

@tool
def example_search_tool(query: str) -> str:
    """Look up things online."""
    return "LangChain"

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
    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    purpose = 'Marketing'
    prompt = pbac_retrieval_prompt(db, purpose)
    chain = create_sql_query_chain(llm, db, k=5, prompt=prompt)
    query = chain.invoke({"question": input})
    results = db.run(query)
    response = f'Query: {query}\nResults: {results}'
    return response

@tool
def sql_retrieval_agent_as_tool(input: str) -> str:
    """SQL agent that retrieves data from a database."""
    # SQL retrieval agent with advanced error handling capabilities.
    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, verbose=True)
    response = agent_executor.invoke(input)

    return response

@tool
def sql_retrieval_agent_as_tool_2(input: str) -> str:
    """SQL agent that retrieves data from a database."""
    # SQL retrieval agent with advanced error handling capabilities. Added custom prompt.
    # Still does not work as intended.
    # Agent supposed to be used as standalone
    # Retrieval chain is better.
    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = OpenAI(temperature=0)
    prompt = create_custom_sql_agent_prompt(db.get_table_info())
    agent_executor = create_sql_agent(llm, db=db, verbose=True, prompt=prompt)
    response = agent_executor.invoke(input)

    return response


@tool
def pbac_prompt_classification_tool(query: str) -> str:
    """You must always use this tool first. This tool classifies the access purpose of the input prompt. Remeber to always use the tool before retrieving data."""

    pc_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

    pbac_examples = [
        {"input": "Summarize the medical history of patient PAP587444 for medical purposes. Only consider the first two vists.", "output": "Care"},
        {"input": "Get all patients that came in third of January, 2017 to process payments.", "output": "Insurance"},
        {"input": "Analyze the medical history of patient PAP587764.", "output": "None"},
        {"input": "How many available records do I have that can be used for research?", "output": "Research"},
        {"input": "Give me the data for patient PAP249364 to schedule a follow-up appointment.", "output": "Support"},
        {"input": "How many people were sick in Q1, 2017. For the analysis of public health trends.", "output": "Public"},
        {"input": "I research cancer. Are there any patients I can contact for a trial program?", "output": "Trial"},
        {"input": "I want to improve obesity therapies. Are there any patients I can contact to improve our current offering?", "output": "Product"},
        {"input": "How many patients can I contact to promote our new drug?", "output": "Marketing"},
    ]

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=pbac_examples,
    )

    pc_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", PBAC_SYSTEM
            ),
            few_shot_prompt,
            (
                "human", "{input}"),
        ]
    )
    chain = pc_prompt | pc_llm
    response = chain.invoke(query)
    #print(f"'{query}' classified as '{response.content}'.")

    return response.content

queries = [
    "Summarize the medical history of patient PAP587444 for medical purposes. Only consider the first two vists.",
    "Get all patients that came in third of January, 2017 to process payments.",
    "How many available records do I have that can be used for research?",
    "How many visits are there?"
]

""" for query in queries:
    print(pbac_prompt_classification_tool(query))


#print(sql_retrieval_agent_as_tool(queries[2]))"""
print(sql_retrieval_chain_tool("Find all feamale patients with cancer that I can contact for the promotion of a new drug."))
