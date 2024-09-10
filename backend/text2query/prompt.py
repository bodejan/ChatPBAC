
RETRIEVAL_SYSTEM = """Given an input question, create syntactically correct {dialect} NoSQL query. 
You can order the results to return the most interesting examples in the database.
Unless otherwise limit results to k={k} entry/entries.
Pay attention to use only the keys that you can see in the collection description tag. 
Be careful to not query for keys that do not exist.
Each key has an associated list of intended purposes (IP).
Always include the access purpose in the query and make sure it matches the intended purpose of the key.

<Collection-Description>
{collection_info}
</Collection-Description>

Return your answer in JSON format. Use double quotation marks for keys and text values. Include the following keys:

"step_by_step": Analyze which fields need to be included. Analyze the type of action needed. Write the query. Analyze if the user mentions a specific limit. Let's think step-by-step. 
"action": The type of query action; one of Literal['find', 'countDocuments', 'aggregate']
"query": The query in curly brackets; Dict[str, Any].
"limit": The limit as requested by the user, otherwise use the defaul kt={k}.

{hint}

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


RETRIEVAL_SYSTEM_NO_PBAC = """Given an input question, create syntactically correct {dialect} NoSQL query. 
You can order the results to return the most interesting examples in the database.
Unless otherwise limit results to k={k} entry/entries.
Pay attention to use only the keys that you can see in the collection description tag. 
Be careful to not query for keys that do not exist.

<Collection-Description>
{collection_info}
</Collection-Description>

Return your answer in JSON format. Use double quotation marks for keys and text values. Include the following keys:

"step_by_step": Analyze which fields need to be included. Analyze the type of action needed. Write the query. Analyze if the user mentions a specific limit. Let's think step-by-step. 
"action": The type of query action; one of Literal['find', 'countDocuments', 'aggregate']
"query": The query in curly brackets; Dict[str, Any].
"limit": The limit as requested by the user, otherwise use the defaul kt={k}.

{hint}

"""


RETRIEVAL_EXAMPLES_NO_PBAC = [
    {
        "input": "Retrieve all records where the Diagnosis is 'Cancer'.",
        "output": "{\"action\": \"find\", \"query\": {\"DiagnosisCategory\": \"Cancer\"}, \"limit\": k}"
    },
    {
        "input": "Fetch the record with ID 'MN02-2799'.",
        "output": "{\"action\": \"find\", \"query\": {\"ReferenceID\": \"MN02-2799\"}, \"limit\": 1}"
    },
    {
        "input": "What is the most common age range in the dataset?",
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$match\": {}}, {\"$group\": {\"_id\": \"$AgeRange\", \"count\": {\"$sum\": 1}}}, {\"$sort\": {\"count\": -1}}, {\"$limit\": 1}]}"
    },
    {
        "input": "Show me all records where the Treatment is 'Pharmacy'.",
        "output": "{\"action\": \"find\", \"query\": {\"TreatmentCategory\": \"Pharmacy\"}, \"limit\": k}"
    },
    {
        "input": "How many patients are covered by Medicaid?",
        "output": "{\"action\": \"countDocuments\", \"query\": {\"PatientInsuranceProvider\": \"Medicaid\"}, \"limit\": 1}"
    },
    {
        "input": "How many records are there for patients aged 51 to 64?",
        "output": "{\"action\": \"countDocuments\", \"query\": {\"AgeRange\": \"51 to 64\"}}"
    },
    {
        "input": "Retrieve two entries where the Determination is Overturned.",
        "output": "{\"action\": \"find\", \"query\": {\"Determination\": \"Overturned Decision of Health Plan\"}, \"limit\": 2}"
    },
    {
        "input": "Show the count of records for each ReportYear.",
        "output": "{\"action\": \"aggregate\", \"query\": [{\"$match\": {}}, {\"$group\": {\"_id\": \"$ReportYear\", \"count\": {\"$sum\": 1}}}]}"
    },
    {
        "input": "Give me the data seven patients with the blood type 'O+'.",
        "output": "{\"action\": \"find\", \"query\": {\"PatientBloodType\": \"O+\"}, \"limit\": 7}"
    },
    {
        "input": "Get the first two entries of female patients for the year 2020.",
        "output": "{\"action\": \"find\", \"query\": {\"PatientGender\": \"Female\", \"ReportYear\": 2020}, \"limit\": 2}"
    },
]
