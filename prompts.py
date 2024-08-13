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
    {"input": "What is the most common age range of patients with diabetes?", "output": "True"},
    {"input": "Retrieve Data for the following ID", "output": "True"},
    {"input": "Show me the list of available data records", "output": "True"},
    {"input": "What is the capital of France?", "output": "False"},
    {"input": "Give me the data for patients with the blood type 'O+'", "output": "True"},
    {"input": "Describe the feeling of happiness", "output": "False"},
    {"input": "And how many entries are there in total?", "output": "True"},
]

RETRIEVAL_SYSTEM = """Given an input question, create syntactically correct {dialect} NoSQL query. 
You can order the results to return the most interesting examples in the database.
Unless otherwise limit results to k={k} entry/entries.
Pay attention to use only the keys that you can see in the schema description. 
Be careful to not query for keys that do not exist.
Each key has an assosicated list of intnded purposes (IP).
Always include the access purpose in the query and make sure it matches the intended purpose of the key.


Only use the following collection:
{collection_info}

Provide a NoSQL action: Literal['find', 'countDocuments', 'aggregate'].
Provide a NoSQL query.
Provide a limit if the user asks for a specific number of results.
Use JSON format. Use double quotation marks for keys and text values.
Let's think step by step
"""

RETRIEVAL_EXAMPLES = [
    {
        "input": "Retrieve all records where the Diagnosis is 'Cancer'. Access Purpose: 'Research'", 
        "output": "{\"action\": \"find\", \"query\": {\"DiagnosisCategory\": \"Cancer\", \"DiagnosisCategory_IP\": \"Research\"}, \"limit\": k}"
    },
    {
        "input": "Fetch the record with ID 'MN02-2799'. Access Purpose: 'Billing'", 
        "output": "{\"action\": \"find\", \"query\": {\"ReferenceID\": \"MN02-2799\"}, \"limit\": 1}"
    },
    {
        "input": "What is the most common age range in the dataset? Access Purpose: 'Clinical-Care'", 
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$match\": {\"AgeRange_IP\": \"Clinical-Care\"}}, {\"$group\": {\"_id\": \"$AgeRange\", \"count\": {\"$sum\": 1}}}, {\"$sort\": {\"count\": -1}}, {\"$limit\": 1}]}"
    },
    {
        "input": "Show me all records where the Treatment is 'Pharmacy'. Access Purpose: 'Public-Research'", 
        "output": "{\"action\": \"find\", \"query\": {\"TreatmentCategory\": \"Pharmacy\", \"TreatmentCategory_IP\": \"Public-Research\"}, \"limit\": k}"
    },
    {
        "input": "How many patients are covered by Medicaid? Access Purpose: 'Patient-Support-Service'", 
        "output": "{\"action\": \"countDocuments\", \"query\": {\"PatientInsuranceProvider\": \"Medicaid\", \"PatientInsuranceProvider_IP\": \"Patient-Support-Service\"}, \"limit\": 1}"
    },
    {
        "input": "How many records are there for patients aged 51 to 64? Access Purpose: 'Private-Research'", 
        "output": "{\"action\": \"countDocuments\", \"query\": {\"AgeRange\": \"51 to 64\", \"AgeRange_IP\": \"Private-Research\"}}"
    },
    {
        "input": "Retrieve two entries where the Determination is Overturned. Access Purpose: 'Clinical-Care'", 
        "output": "{\"action\": \"find\", \"query\": {\"Determination\": \"Overturned Decision of Health Plan\", \"Determination_IP\": \"Clinical-Care\"}, \"limit\": 2}"
    },
    {
        "input": "Show the count of records for each ReportYear. Access Purpose: 'Research'", 
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$match\": {\"ReportYear_IP\": \"Research\"}}, {\"$group\": {\"_id\": \"$ReportYear\", \"count\": {\"$sum\": 1}}}]}"
    },
    {
        "input": "Give me the data seven patients with the blood type 'O+'. Access Purpose: 'Non-Military-Research'", 
        "output": "{\"action\": \"find\", \"query\": {\"PatientBloodType\": \"O+\", \"PatientBloodType_IP\": \"Non-Military-Research\"}, \"limit\": 7}"
    },
    {
        "input": "Get the first two entries of female patients for the year 2020. Access Purpose: 'Clinical-Care'", 
        "output": "{\"action\": \"find\", \"query\": {\"PatientGender\": \"Female\", \"PatientGender_IP\": \"Clinical-Care\", \"ReportYear\": 2012, \"ReportYear_IP\": \"Clinical-Care\"}, \"limit\": 2}"
    },
]


CHAT_SYSTEM = """You are an assistant with chat and question-answering capabilities. \
Answer all questions to the best of your ability. \
If you don't know the answer, just say that you don't know and ask for more precise instructions. \
You have acces to a database. Description: {db_context}. \

If provided, use retrieval results to answer questions.\
Retrieval results: {context}
"""