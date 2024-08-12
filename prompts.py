from config import DB_CONTEXT

DECIDE_RETRIEVAL_SYSTEM = """You are an AI model trained to identify whether a given text input contains a request for data retrieval.
A data retrieval request is any inquiry that seeks to obtain specific information, facts, or data.
Your task is to analyze each input and classify it as either "True" for retrieval requests or "False" if no retrieval request is present.

Only retrieval requests for the following context are valid. Other retrieval requests should be classified as "False".

Context: {db_context}

Classify the following input:
"""

DECIDE_RETRIEVAL_EXAMPLES = [
    {"input": "Please summarize your response", "output": "False"},
    {"input": "Retrieve Data for the following ID", "output": "True"},
    {"input": "What is the capital of France?", "output": "False"},
    {"input": "Describe the feeling of happiness", "output": "False"},
    {"input": "Show me the list of available data records", "output": "True"},
    {"input": "And how many entries are there in total?", "output": "True"},
]

RETRIEVAL_SYSTEM = """Given an input question, create syntactically correct {dialect} NoSQL query. 
You can order the results to return the most interesting examples in the database.
Never query for all the keys from a specific collection, only retrieve relevant keys given the question.
Pay attention to use only the keys that you can see in the schema description. 
Be careful to not query for keys that do not exist. 

Only use the following collection:
{collection_info}

Provide a NoSQL action: 'find', 'countDocuments', or 'aggregate' and a query.
Use JSON format. Use double quotation marks for keys and values.
"""

RETRIEVAL_EXAMPLES = [
    {
        "input": "Retrieve all records where the Diagnosis is 'Cancer'", 
        "output": "{\"action\": \"find\", \"query\": {\"DiagnosisCategory\": \"Cancer\"}}"
    },
    {
        "input": "Fetch the record with ID 'MN02-2799'", 
        "output": "{\"action\": \"find\", \"query\": {\"ReferenceID\": \"MN02-2799\"}}"
    },
    {
        "input": "What is the most common age range in the dataset?", 
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$group\": {\"_id\": \"$AgeRange\", \"count\": {\"$sum\": 1}}}, {\"$sort\": {\"count\": -1}}, {\"$limit\": 1}]}"
    },
    {
        "input": "Show me all records where the Treatment is 'Pharmacy'", 
        "output": "{\"action\": \"find\", \"query\": {\"TreatmentCategory\": \"Pharmacy\"}}"
    },
    {
        "input": "How many patients are covered by Medicaid?", 
        "output": "{\"action\": \"countDocuments\", \"query\": {\"PatientInsuranceProvider\": \"Medicaid\"}}"
    },
    {
        "input": "How many records are there for patients aged 51 to 64?", 
        "output": "{\"action\": \"countDocuments\", \"query\": {\"AgeRange\": \"51 to 64\"}}"
    },
    {
        "input": "Retrieve all entries where the Determination is Overturned", 
        "output": "{\"action\": \"find\", \"query\": {\"Determination\": \"Overturned Decision of Health Plan\"}}"
    },
    {
        "input": "Show the count of records for each ReportYear", 
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$group\": {\"_id\": \"$ReportYear\", \"count\": {\"$sum\": 1}}}]}"
    },
    {
        "input": "Give me the data for patients with the blood type 'O+'", 
        "output": "{\"action\": \"find\", \"query\": {\"PatientBloodType\": \"O+\"}}"
    }
]



