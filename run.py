from db import execute_query
from llm2 import decide_retrieval, write_nosql_query
from pbac import run_pbac

import ast

user_input_1 = "What is the average age of patients with diabetes?"
user_input_2 = "Retrieve all records where the Diagnosis is 'Cancer'"

if decide_retrieval(user_input_2):
    action, query = write_nosql_query(user_input_2)
    results = execute_query(query, action, 2)
    filtered = run_pbac(results, 2, query)
    print(filtered)

""" output = r'{"action": "aggregate", "query": [{"$match": {"DiagnosisSubCategory": "Diabetes"}}, {"$group": {"_id": null, "averageAge": {"$avg": "$PatientAge"}}}]}'
output_dict = ast.literal_eval(output)
print(output_dict) """