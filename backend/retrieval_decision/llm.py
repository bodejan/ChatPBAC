from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)

import logging
import dotenv
from backend.config.config import (
    DB_CONTEXT,
)


from backend.retrieval_decision.prompt import (
    DECIDE_RETRIEVAL_EXAMPLES, 
    DECIDE_RETRIEVAL_SYSTEM, 
)


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