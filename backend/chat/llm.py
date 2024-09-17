from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain_core.messages import (
    FunctionMessage
)
import logging
import dotenv
from backend.const import (
    DB_CONTEXT,
)
from backend.chat.prompt import (
    CHAT_SYSTEM
)


dotenv.load_dotenv()

logger = logging.getLogger()

def format_retrieval_context(action: str, query: str, result: str) -> str:
    """
    Formats the retrieval context.

    Parameters:
    - action (str): The action performed.
    - query (str): The query used.
    - result (str): The result of the action.

    Returns:
    - str: The formatted retrieval context.
    """
    return f"Use the use the following information to answer the question:\nAction: {action}\nQuery: {query}\nResult: {result}"


def chat(user_prompt: str, chat_history: list = [], retrieval_context: str ='', debug: bool = False) -> str:
    """
    Chat model using the given user prompt and chat history.

    Args:
        user_prompt (str): The user prompt for the chat.
        chat_history (list, optional): The chat history. Defaults to an empty list.
        debug (bool, optional): Whether to return the llm response. Defaults to False.

    Returns:
        str: The response from the language model.
    """
    pass
    chat = ChatOpenAI(temperature=0.3)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CHAT_SYSTEM),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt | chat
    response = chain.invoke(
        {"input": user_prompt, "chat_history": chat_history, 'retrieval_context': retrieval_context})

    content = response.content

    logger.info(f"Chat Response: {content}")

    if debug:
        return content, response

    return content
