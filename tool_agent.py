from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory

from retrieval import sql_retrieval_chain_tool, sql_retrieval_tool
from classification import classification_tool

from dotenv import load_dotenv

load_dotenv()

def init_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    tools = [TavilySearchResults(max_results=5), sql_retrieval_tool, classification_tool]
    memory = ChatMessageHistory(session_id="session-id-placeholder")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system", "You are a helpful privacy-aware assistant. You have access to the following tools: sql_retrieval_tool, pbac_prompt_classification_tool. Always use the pbac_prompt_classification_tool before the sql_retrieval_tool.",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    # Construct the Tools agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, return_intermediate_steps=True)

    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        # This is needed because in most real world scenarios, a session id is needed
        # It isn't really used here because we are using a simple in memory ChatMessageHistory
        lambda session_id: memory,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return agent_with_chat_history


def test_agent_with_history(agent_with_chat_history):
    response = agent_with_chat_history.invoke(
        {"input": "Find all feamale patients with cancer that I can contact for the promotion of a new drug."},
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(response, '\n---------------------')

    response = agent_with_chat_history.invoke(
        {"input": "And how many in total?"},
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(response, '\n---------------------')

    response = agent_with_chat_history.invoke(
        {"input": "Now give me the names for the top 10 results I can use for patient care."},
        config={"configurable": {"session_id": "<foo>"}},
    )
    print(response, '\n---------------------')

if __name__ == '__main__':
    agent_with_chat_history = init_agent()
    test_agent_with_history(agent_with_chat_history)