from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from langchain.tools.render import render_text_description

from tools import sql_retrieval_chain_tool, pbac_prompt_classification_tool
from prompt_template import create_system_prompt

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
tools = [TavilySearchResults(max_results=5), sql_retrieval_chain_tool, pbac_prompt_classification_tool]
memory = ChatMessageHistory(session_id="session-id-placeholder")
system_prompt = create_system_prompt()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", "You are a helpful privacy-aware assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

""" prompt = prompt.partial(
    tools=render_text_description(list(tools)),
    tool_names=", ".join([t.name for t in tools]),
) """

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)
print(agent)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def test_agent_with_history():
    response = agent_with_chat_history.invoke(
        {"input": "Find all feamale patients with cancer that I can contact for the promotion of a new drug."},
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(response)

    response = agent_with_chat_history.invoke(
        {"input": "And how many in total?"},
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(response)

test_agent_with_history()