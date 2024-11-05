from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

import logging
import dotenv
from pbac_rag.const import (
    DB_CONTEXT,
)

from pbac_rag.retrieval_decision.prompt import (
    DECIDE_RETRIEVAL_EXAMPLES,
    DECIDE_RETRIEVAL_SYSTEM,
)


dotenv.load_dotenv()

logger = logging.getLogger()


def decide_retrieval(user_prompt: str, debug: bool = False) -> bool:
    """
    Decide if the user prompt necessitates a retrieval action.

    Args:
        user_prompt (str): The user prompt to be evaluated.
        debug (bool, optional): Whether to return the llm response. Defaults to False.

    Returns:
        bool: The retrieval decision response, True or False.

    """

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
        template=DECIDE_RETRIEVAL_SYSTEM, partial_variables={
            "db_context": DB_CONTEXT}
    ).format()

    final_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    llm = ChatOpenAI(temperature=0, model='gpt-4o-mini', max_tokens=1)
    chain = final_prompt | llm
    response = chain.invoke(user_prompt)
    content = response.content
    logger.info(f"Retrieval Decision: {content}")
    decision = content == "True"

    if debug:
        return decision, response

    return decision