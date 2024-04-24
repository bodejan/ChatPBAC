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

from sql_agent import create_custom_sql_agent
from prompt_template import create_custom_sql_agent_prompt

import sqlite3

@tool
def example_search_tool(query: str) -> str:
    """Look up things online."""
    return "LangChain"

@tool
def sql_retrieval_chain_tool(input: str) -> str:
    """SQL chain that writes and executes sql queries on a private database."""
    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    chain = create_sql_query_chain(llm, db, k=5)
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
    db_path = "sqlite:///sqlite_medical.db"
    db = SQLDatabase.from_uri(db_path)
    llm = OpenAI(temperature=0)
    prompt = create_custom_sql_agent_prompt(db.get_table_info())
    agent_executor = create_sql_agent(llm, db=db, verbose=True, prompt=prompt)
    response = agent_executor.invoke(input)

    return response


@tool
def pbac_prompt_classification_tool(query: str) -> str:
    """Classifies the access purpose of the input prompt."""

    pc_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    pc_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a helpful assistant that classifies a text input into a predefined access purpose category.

                The following categories exist:

                1. Clinical Care
                Description: Facilitates ongoing patient care by providing healthcare providers with comprehensive access to patient histories, diagnoses, treatments, and contact information. This purpose supports informed clinical decisions and personalized care plans.
                Category code: 'Care'

                2. Research:
                Description: Supports medical research by allowing access to anonymized patient data, focusing on diagnosis and treatment outcomes. Researchers can study patterns, effectiveness, and potential improvements in healthcare delivery and treatments.
                Category code: 'Research'

                3. Billing and Insurance Claims Processing:
                Description: Enables the processing of billing and insurance claims through access to patient insurance information, treatment categories, and patient identifiers. This purpose assists in verifying coverage and submitting claims to insurance providers.
                Category code: 'Insurance'

                4. Patient Support Services:
                Description: Facilitates the provision of support services to patients, including appointment scheduling, follow-up arrangements, and emergency contact communication. Ensures patients receive timely care and information.
                Category code: 'Support'

                5. Public Health Monitoring and Response:
                Description: Allows for the monitoring of public health trends and the management of health crises by analyzing aggregated data on diagnoses, treatments, and patient demographics. Supports public health initiatives and emergency response planning.
                Category code: 'Public'

                6. Clinical Trial Recruitment:
                Description: Supports the identification and recruitment of potential clinical trial participants by matching patient diagnoses and treatments with trial eligibility criteria. Facilitates advancements in medical research and treatment development.
                Category code: 'Trial'

                7. Product Development:
                Description: Informs the development of medical products and services by analyzing treatment outcomes, patient demographics, and health conditions. Drives innovation in healthcare solutions tailored to patient needs. Data will be shared with third parties.
                Category code: 'Product'

                8. Marketing:
                Description: Tailors health-related marketing initiatives to patient demographics and conditions, promoting relevant healthcare services, products, and wellness programs. Aims to enhance patient engagement and healthcare outcomes.
                Category code: 'Marketing'
                
                Classify the input into one of the described categories. 
                Use the defined category code.
                If none of the categories matches, return 'None'. 
                Only return the category code or 'None'. 

                """
            ),
            (
                "human", 
                "{input}"),
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


print(sql_retrieval_agent_as_tool(queries[2]))"""
print(sql_retrieval_chain_tool(queries[3]))
