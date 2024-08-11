from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
import logging
import dotenv
from config import (
    DB_CONTEXT,
    DB_DIALECT,
    DB_COLLECTION_INFO
)

from prompts import (
    DECIDE_RETRIEVAL_EXAMPLES, 
    DECIDE_RETRIEVAL_SYSTEM, 
    RETRIEVAL_SYSTEM,
    RETRIEVAL_EXAMPLES
)
import ast

dotenv.load_dotenv()

logger = logging.getLogger()


def decide_retrieval(user_prompt: str):
    """Decide if a data retrieval request is present in the user prompt."""

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=DECIDE_RETRIEVAL_EXAMPLES,
    )

    system_prompt = PromptTemplate(
        template=DECIDE_RETRIEVAL_SYSTEM, partial_variables={"db_context": DB_CONTEXT}
    ).format()

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0.1, model='gpt-4o-mini')
    chain = final_prompt | llm
    response = chain.invoke(user_prompt).content
    logger.info(f"Retrieval Decision: {response}")
    return response

def write_nosql_query(user_prompt: str):
    def parse(output: str):
        output_dict = ast.literal_eval(output)
        return output_dict
    
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=RETRIEVAL_EXAMPLES,
    )
    system_prompt = PromptTemplate(
        template=RETRIEVAL_SYSTEM, partial_variables={"dialect": DB_DIALECT, "collection_info": DB_COLLECTION_INFO}
    ).format()

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model='gpt-4o', model_kwargs={"response_format": {"type": "json_object"}})
    chain = final_prompt | llm
    output = chain.invoke(user_prompt).content
    output_dict = parse(output)

    return output_dict.get('action'), output_dict.get('query')



#print(decide_retrieval("Please summarize your response"))
#print(write_nosql_query("Retrieve all records where the Diagnosis is 'Cancer'"))