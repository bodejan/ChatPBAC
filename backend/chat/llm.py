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
from backend.config.config import (
    DB_CONTEXT,
)

from backend.chat.prompt import (
    CHAT_SYSTEM
)


dotenv.load_dotenv()

logger = logging.getLogger()

def add_function_message(context: str, name: Literal['retrival', 'validation'], chat_history: list):
    chat_history.append(FunctionMessage(content=context, name=name))
    return chat_history

def chat(user_prompt: str, chat_history: list = []):
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