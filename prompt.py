# flake8: noqa

CUSTOM_PREFIX = """Retrieve data relevant for the following intput prompt. Write a query and execute it. Always return the executed query along with the final answer. You have access to the following tools: {tools}"""

CUSTOM_METADATA_INSTRUCTIONS = """Use the following infromation about the database: """

CUSTOM_FORMAT_INSTRUCTIONS = """Use the following format:

Prompt: the input prompt you must retrieve data for
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final data relevant for the original input prompt"""

CUSTOM_SUFFIX = """Begin!

Prompt: {input}
Thought:{agent_scratchpad}"""


SYSTEM_PREFIX = """You are a helpful privacy-aware assistant. You have access to the following tools: {tools}"""

SYSTEM_FORMAT_INSTRUCTIONS = """Use the following format:

Classification: you must always classify the access purpose of the input first
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""

SYSTEM_SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""

RETRIEVAL_PRE_SUFFIX = """You must always filter the query results to only include data where "Intended Purpose" contains: """