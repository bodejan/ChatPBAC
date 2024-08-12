from db import execute_query
from llm2 import decide_retrieval, write_nosql_query
from pbac import run_pbac


user_input_1 = "What is the most common age range of patients with diabetes?"
user_input_2 = "Retrieve all records where the Diagnosis is 'Cancer'"

if decide_retrieval(user_input_1):
    access_purpose= 'Research'
    action, query = write_nosql_query(user_input_1, access_purpose)
    results = execute_query(query, action, 2)
    if action == 'find':
        filtered = run_pbac(results, access_purpose)
        print(filtered[1])
        for item in filtered[0]:
            print(item)
    else:
        print(results)
        