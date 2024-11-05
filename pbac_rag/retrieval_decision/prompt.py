# Prompt for the retrieval decision task
DECIDE_RETRIEVAL_SYSTEM = """You are an AI assistant tasked with determining whether data retrieval is required to answer a user's question.
Available classifications:
1. 'True': Access to a database is required. Keywords like 'retrieve', 'show', 'list', 'count', 'get', 'find', 'db', 'database', or 'collection' are common indicators.
2. 'False': The question can be answered using world knowledge.

Only retrieval requests for the following context are valid. Other requests should be classified as 'False'.
<Context>
{db_context}
</Context>

Classify the following input:
"""
# Examples for the retrieval decision task
DECIDE_RETRIEVAL_EXAMPLES = [
    {"input": "Please summarize your response", "output": "False"},
    {"input": "What is the most common age range of patients with diabetes?",
        "output": "True"},
    {"input": "Retrieve Data for the following ID: M24XYZ", "output": "True"},
    {"input": "Show me the list of available data records", "output": "True"},
    {"input": "What is the capital of France?", "output": "False"},
    {"input": "Give me the data for patients with the blood type 'O+'", "output": "True"},
    {"input": "Describe the feeling of happiness", "output": "False"},
    {"input": "And how many entries are there in total?", "output": "True"},
    {"input": "How many records are in the collection?", "output": "True"},
    {"input": "Count the total number of entries.", "output": "True"},
]
