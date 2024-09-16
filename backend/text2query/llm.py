from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

import logging
import dotenv
from backend.const import (
    DB_DIALECT,
    DB_COLLECTION_INFO,
)

from backend.text2query.prompt import (
    RETRIEVAL_SYSTEM_NO_PBAC,
    RETRIEVAL_EXAMPLES_NO_PBAC,
)

import json

dotenv.load_dotenv()

logger = logging.getLogger()


def write_nosql_query_no_pbac(user_prompt: str, k: int = 1, hint: str = '', debug: bool = False) -> tuple[str, str, int]:
    """
    Generates a NoSQL query based on the given user prompt.

    Args:
        user_prompt (str): The user prompt for generating the query.
        k (int, optional): The number of results to retrieve. Defaults to 1.
        hint (str, optional): A hint to guide the query generation. Defaults to ''.
        debug (bool, optional): Whether to return the llm response. Defaults to False.

    Returns:
        tuple[str, str, int]: A tuple containing the action, query, and limit of the generated query.

    """

    def parse(output: str) -> dict:
        """
        Parses the given output string and returns a dictionary.

        Args:
            output (str): The output string to be parsed.

        Returns:
            dict: The parsed output as a dictionary.
        """
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

    logger.info(f"Action: {action}")
    logger.info(f"Query: {query}")
    logger.info(f"Limit: {limit}")

    if debug:
        return action, query, limit, response

    return action, query, limit
