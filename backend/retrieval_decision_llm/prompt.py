DECIDE_RETRIEVAL_SYSTEM = """You are an AI model trained to identify whether a given text input contains a request for data retrieval.
A data retrieval request is any inquiry that seeks to obtain specific information, facts, or data.
Your task is to analyze each input and classify it as either "True" for retrieval requests or "False" if no retrieval request is present.

Only retrieval requests for the following context are valid. Other retrieval requests should be classified as "False".

Context: {db_context}

Classify the following input:
"""

DECIDE_RETRIEVAL_EXAMPLES = [
    {"input": "Please summarize your response", "output": "False"},
    {"input": "What is the most common age range of patients with diabetes?", "output": "True"},
    {"input": "Retrieve Data for the following ID", "output": "True"},
    {"input": "Show me the list of available data records", "output": "True"},
    {"input": "What is the capital of France?", "output": "False"},
    {"input": "Give me the data for patients with the blood type 'O+'", "output": "True"},
    {"input": "Describe the feeling of happiness", "output": "False"},
    {"input": "And how many entries are there in total?", "output": "True"},
]