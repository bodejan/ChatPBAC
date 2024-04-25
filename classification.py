import json
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
from langchain_openai import OpenAI
from sql_agent import create_custom_sql_agent
from prompt_template import create_custom_sql_agent_prompt
from prompt import RETRIEVAL_PRE_SUFFIX
from langchain.chains.sql_database.prompt import PROMPT, SQL_PROMPTS, PROMPT_SUFFIX
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
import sqlite3

PBAC_SYSTEM = """You are a helpful privacy-aware assistant that classifies a text input into a predefined access purpose category.

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

# @TODO change to LLM
def pbac_prompt_classification(query: str) -> str:
    """You must always use this tool first. This tool classifies the access purpose of the input prompt. Remeber to always use the tool before retrieving data."""

    pc_llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.2)

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
    print(pc_prompt)
    chain = pc_prompt | pc_llm
    response = chain.invoke(query)
    print(f"'{query}' classified as '{response.content}'.")

    return response.content

class Classification(BaseModel):
    purpose: str = Field(description="the identified access purpose", enum=["Care", "Research", "Insurance", "Support", "Public", "Trial", "Product", "Marketing", "None"])
    confidence: float = Field(description="the confidence at which the access purpose was identified", enum=[x / 10 for x in range(1, 11)])
    justification: str = Field(description="the justification why the access purpose was identified")

def pbac_prompt_classification_llm(query):
    classification_template = PBAC_SYSTEM + '\n{format_instructions}\n' +'Input: {query}.'
    llm = OpenAI(temperature=0.1)
    parser = JsonOutputParser(pydantic_object=Classification)
    prompt = PromptTemplate(
        template=classification_template,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions() + "\nDo not use quotation marks in your justification."},
    )

    chain = prompt | llm | parser

    response = chain.invoke({"query": query})
    print(response)

    return response['purpose']

pbac_prompt_classification_llm("Find all feamale patients with cancer that I can contact for investigating a new drug.")
#pbac_prompt_classification_llm("Give me the data for patient PAP249364 to schedule a follow-up appointment.")

