# Retrieval prompt for the NoSQL query generation system.
RETRIEVAL_SYSTEM_NO_PBAC = """Given an input question, create syntactically correct {dialect} NoSQL query. 
You can order the results to return the most interesting examples in the database.
Use 'aggregate' when sorting, or skipping.
Pay attention to use only the keys that you can see in the collection description tag. 
Be careful to not query for keys that do not exist.

<Collection-Description>
{collection_info}
</Collection-Description>

Return your answer in JSON format. Use double quotation marks for keys and text values. Include the following keys:

"step_by_step": Analyze which fields need to be included. Analyze the type of action needed. Write the query. Analyze if the user mentions a specific limit. Let's think step-by-step. 
"action": The type of query action; one of Literal['find', 'countDocuments', 'aggregate']
"query": The query in curly brackets; Dict[str, Any].
"limit": The limit as specified by the user otherwise do not include it.

{hint}

"""

# Examples for the NoSQL query generation system.
RETRIEVAL_EXAMPLES_NO_PBAC = [
    {
        "input": "Retrieve all records where the Diagnosis is 'Cancer'.",
        "output": "{\"step_by_step\": \"To retrieve all records where the DiagnosisCategory is 'Cancer', the following steps are needed: 1. Identify the field to query: DiagnosisCategory. 2. Determine the action needed: find. 3. Construct the query to match documents where DiagnosisCategory equals 'Cancer'. 4. Apply the limit as specified or use the default if not mentioned.\", \"action\": \"find\", \"query\": {\"DiagnosisCategory\": \"Cancer\"}}"
    },
    {
        "input": "Fetch the record with ID 'MN02-2799'.",
        "output": "{\"step_by_step\": \"To fetch the record with ID 'MN02-2799', the following steps are needed: 1. Identify the field to query: ReferenceID. 2. Determine the action needed: find. 3. Construct the query to match the document where ReferenceID equals 'MN02-2799'. 4. Apply the limit as specified or use the default if not mentioned.\", \"action\": \"find\", \"query\": {\"ReferenceID\": \"MN02-2799\"}, \"limit\": 1}"
    },
    {
        "input": "What is the most common age range in the dataset?",
        "output": "{\"step_by_step\": \"To determine the most common age range in the dataset, the following steps are needed: 1. Identify the field to analyze: AgeRange. 2. Determine the action needed: aggregate. 3. Construct the aggregation pipeline to group by AgeRange and count occurrences. 4. Sort the results to find the most common age range. 5. Apply the limit to retrieve the top result.\", \"action\": \"aggregate\", \"query\": [{\"$group\": {\"_id\": \"$AgeRange\", \"count\": {\"$sum\": 1}}}, {\"$sort\": {\"count\": -1}}, {\"$limit\": 1}]}"
    },
    {
        "input": "Show me all records where the Treatment is 'Pharmacy'.",
        "output": "{\"step_by_step\": \"To retrieve all records where the TreatmentCategory is 'Pharmacy', the following steps are needed: 1. Identify the field to query: TreatmentCategory. 2. Determine the action needed: find. 3. Construct the query to match documents where TreatmentCategory equals 'Pharmacy'. 4. Apply the limit as specified or use the default if not mentioned.\", \"action\": \"find\", \"query\": {\"TreatmentCategory\": \"Pharmacy\"}}"
    },
    {
        "input": "How many patients are covered by Medicaid?",
        "output": "{\"step_by_step\": \"To determine the number of patients covered by Medicaid, the following steps are needed: 1. Identify the field to query: PatientInsuranceProvider. 2. Determine the action needed: countDocuments. 3. Construct the query to count documents where PatientInsuranceProvider equals 'Medicaid'.\", \"action\": \"countDocuments\", \"query\": {\"PatientInsuranceProvider\": \"Medicaid\"}}"
    },
    {
        "input": "How many records are there for patients aged 51 to 64?",
        "output": "{\"step_by_step\": \"To determine the number of records for patients aged 51 to 64, the following steps are needed: 1. Identify the field to query: AgeRange. 2. Determine the action needed: countDocuments. 3. Construct the query to count documents where AgeRange equals '51 to 64'.\", \"action\": \"countDocuments\", \"query\": {\"AgeRange\": \"51 to 64\"}}"
    },
    {
        "input": "Retrieve two entries where the Determination is Overturned.",
        "output": "{\"step_by_step\": \"To retrieve two entries where the Determination is 'Overturned Decision of Health Plan', the following steps are needed: 1. Identify the field to query: Determination. 2. Determine the action needed: find. 3. Construct the query to match documents where Determination equals 'Overturned Decision of Health Plan'. 4. Apply the limit to retrieve two entries.\", \"action\": \"find\", \"query\": {\"Determination\": \"Overturned Decision of Health Plan\"}, \"limit\": 2}"
    },
    {
        "input": "Show the count of records for each ReportYear.",
        "output": "{\"step_by_step\": \"To show the count of records for each ReportYear, the following steps are needed: 1. Identify the field to analyze: ReportYear. 2. Determine the action needed: aggregate. 3. Construct the aggregation pipeline to group by ReportYear and count occurrences. 4. Sort the results if needed.\", \"action\": \"aggregate\", \"query\": [{\"$match\": {}}, {\"$group\": {\"_id\": \"$ReportYear\", \"count\": {\"$sum\": 1}}}]}"
    },
    {
        "input": "Give me the data seven patients with the blood type 'O+'.",
        "output": "{\"step_by_step\": \"To retrieve data for seven patients with the blood type 'O+', the following steps are needed: 1. Identify the field to query: PatientBloodType. 2. Determine the action needed: find. 3. Construct the query to match documents where PatientBloodType equals 'O+'. 4. Apply the limit to retrieve seven entries.\", \"action\": \"find\", \"query\": {\"PatientBloodType\": \"O+\"}, \"limit\": 7}"
    },
    {
        "input": "Get the first two entries of female patients for the year 2020.",
        "output": "{\"step_by_step\": \"To retrieve the first two entries for female patients for the year 2020, the following steps are needed: 1. Identify the fields to query: PatientGender and ReportYear. 2. Determine the action needed: find. 3. Construct the query to match documents where PatientGender equals 'Female' and ReportYear equals 2020. 4. Apply the limit to retrieve two entries.\", \"action\": \"find\", \"query\": {\"PatientGender\": \"Female\", \"ReportYear\": 2020}, \"limit\": 2}"
    },
]
