from backend.pbac import re_write_query, filter_results
from backend.db import execute_query
from collections import OrderedDict

import time
from backend.text2query.llm import write_nosql_query, write_nosql_query_no_pbac

start = time.time()
ap = "Third-Party"
a, q, l = write_nosql_query_no_pbac(
    "Provide the first two records", ap, 2)
print(time.time() - start)

re_written = re_write_query(q, a, ap)
print(re_written)

response, _ = execute_query(a, re_written, l)

print(filter_results(a, response, ap))
