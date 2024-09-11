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
from backend.config.const import (
    DB_CONTEXT,
)
from backend.chat.prompt import (
    CHAT_SYSTEM
)


dotenv.load_dotenv()

logger = logging.getLogger()


def add_function_message(context: str, name: str, chat_history: list) -> list:
    """
    Adds a function message to the chat history.

    Parameters:
    - context (str): The content of the function message.
    - name (str): The name of the function message.
    - chat_history (list): The chat history to which the function message will be added.

    Returns:
    - list: The updated chat history with the added function message.
    """
    chat_history.append(FunctionMessage(content=context, name=name))
    return chat_history


def chat(user_prompt: str, chat_history: list = []) -> str:
    """
    Chat model using the given user prompt and chat history.

    Args:
        user_prompt (str): The user prompt for the chat.
        chat_history (list, optional): The chat history. Defaults to an empty list.

    Returns:
        str: The response from the language model.
    """
    pass
    chat = ChatOpenAI(temperature=0.2)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", CHAT_SYSTEM),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt | chat
    response = chain.invoke(
        {"input": user_prompt, "chat_history": chat_history, "db_context": DB_CONTEXT}).content

    logger.info(f"Chat Response: {response}")

    return response
