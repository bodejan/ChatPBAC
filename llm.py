from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate

from dotenv import load_dotenv
import logging

logger = logging.getLogger()

load_dotenv()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def init_chatbot():
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You're a helpful assistant. If provided, use the <CONTEXT> to help with user requests.",
            ),
            MessagesPlaceholder(variable_name="history"),
            ("human", "<INPUT> {input}\n<CONTEXT> {context}\n "),
        ]
    )

    chain = prompt | llm

    with_message_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )

    return with_message_history


def init_naive_chat():
    chat = ChatOpenAI()
    return chat


if __name__ == '__main__':
    # agent_with_chat_history = init_agent()
    # test_agent_with_history(agent_with_chat_history)
    init_chatbot()
