from retrieval_decision.llm import decide_retrieval
from text2query.llm import write_nosql_query


def eval_input(test: dict):
    access_purpose = 'Clinical-Care'

    test['retrieval_decision'] = decide_retrieval(test.get('input'))
    action, query, limit = write_nosql_query(
        test.get('input'), access_purpose)
    test['pbac_query'] = f'{action} {query} {limit}'
