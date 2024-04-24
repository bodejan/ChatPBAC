# flake8: noqa

CUSTOM_PREFIX = """Retrieve data relevant for the following intput prompt. Write a query and execute it. Always return the executed query along with the final answer. You have access to the following tools:"""

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






PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""

FORMAT_INSTRUCTIONS = """Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question"""

SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""