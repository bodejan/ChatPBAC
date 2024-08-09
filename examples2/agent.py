from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

tools = [multiply]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Construct the Tools agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "What is 5 by 3?"})

print(response)

"""
> Entering new AgentExecutor chain...

Invoking: `multiply` with `{'a': 5, 'b': 3}`


15 5 multiplied by 3 is 15.

> Finished chain.

{'input': 'What is 5 by 3?', 'output': '5 multiplied by 3 is 15.'}
"""