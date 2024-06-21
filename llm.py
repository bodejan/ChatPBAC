from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from dotenv import load_dotenv
import logging

from config import DB_CONTEXT

logger = logging.getLogger()

load_dotenv()


def init_chat():
    chat = ChatOpenAI(temperature=0.2)

    system_prompt = (
        "You are a helpful assistant. Answer all questions to the best of your ability. "
        "You have access to an SQL database. "
        f"Database description: {DB_CONTEXT}"
        # "If you include query results in your response, please format them as a table and make the table scrollable."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    chain = prompt | chat
    return chain


def format_chat_history(chat_history, user_prompt):
    history_langchain_format = []
    for human, ai in chat_history:
        if human is None:
            human = ""
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=user_prompt))

    return history_langchain_format


def extend_chat_history(chat_history, user_prompt, chatbot_response):
    chat_history.append((user_prompt, chatbot_response.content))
    return chat_history


def get_user_context_prompt(user_prompt, query, results):
    def get_context(query, results):
        context = f"""

-----------------

SQL Retrieval Context:
```sql
{query}
```
```
{results}
```
"""
        return context
    context = get_context(query, results)
    user_context_prompt = user_prompt + context
    return user_context_prompt


if __name__ == '__main__':
    chat = init_chat()
