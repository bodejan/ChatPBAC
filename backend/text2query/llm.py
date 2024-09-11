from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

import logging
import dotenv
from backend.config.const import (
    DB_DIALECT,
    DB_COLLECTION_INFO,
)

from backend.text2query.prompt import (
    RETRIEVAL_SYSTEM,
    RETRIEVAL_SYSTEM_NO_PBAC,
    RETRIEVAL_EXAMPLES,
    RETRIEVAL_EXAMPLES_NO_PBAC,
)

import json

dotenv.load_dotenv()

logger = logging.getLogger()


def write_nosql_query(user_prompt: str, access_purpose: str, k: int = 1, hint: str = ''):

    def parse(output: str):
        output_dict = json.loads(output)
        return output_dict

    def append_access_purpose(user_prompt: str, access_purpose: str):
        return f"{user_prompt} Access Purpose: '{access_purpose}'"

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
        template=RETRIEVAL_SYSTEM, partial_variables={
            "dialect": DB_DIALECT, "collection_info": DB_COLLECTION_INFO, "k": str(k), "hint": hint}
    ).format()

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model='gpt-4o',
                     model_kwargs={"response_format": {"type": "json_object"}})
    chain = final_prompt | llm
    response = chain.invoke(
        {'input': append_access_purpose(user_prompt, access_purpose)})
    content = response.content
    content_dict = parse(content)

    logger.info(f"NoSQL Action: {content_dict.get('action')}")
    logger.info(f"NoSQL Query: {content_dict.get('query')}")
    if content_dict.get('limit'):
        logger.info(f"Limit: {content_dict.get('limit')}")

    return content_dict.get('action'), content_dict.get('query'), content_dict.get('limit')


def write_nosql_query_no_pbac(user_prompt: str, access_purpose: str, k: int = 1, hint: str = ''):

    def parse(output: str):
        output_dict = json.loads(output)
        return output_dict

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=RETRIEVAL_EXAMPLES_NO_PBAC,
    )
    system_prompt = PromptTemplate(
        template=RETRIEVAL_SYSTEM_NO_PBAC, partial_variables={
            "dialect": DB_DIALECT, "collection_info": DB_COLLECTION_INFO, "k": str(k), "hint": hint}
    ).format()

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model='gpt-4o',
                     model_kwargs={"response_format": {"type": "json_object"}})
    chain = final_prompt | llm
    response = chain.invoke({'input': user_prompt})
    content = response.content
    content_dict = parse(content)

    action = content_dict.get('action')
    query = content_dict.get('query')
    limit = content_dict.get('limit', None)

    if limit is None:
        limit = k

    logger.info(f"NoSQL Action: {action}")
    logger.info(f"NoSQL Query: {query}")
    logger.info(f"Limit: {limit}")

    return action, query, limit
