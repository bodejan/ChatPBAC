from collections import OrderedDict
from backend.config.const import KEYS, KEYS_IP
import logging
import re

logger = logging.getLogger()


def filter_results(action: str, result: list, access_purpose: str) -> list:
    """
    Filter the result based on the given action and access purpose.

    Args:
        action (str): The action to perform.
        result (list): The list of documents to filter.
        access_purpose (str): The access purpose to filter by.

    Returns:
        list: The filtered result based on the action and access purpose.
    """

    if action == 'find':
        ip_keys_include = []
        filtered_result = []
        for doc in result:
            filtered_doc = {}
            for key in KEYS_IP:
                if access_purpose in doc.get(key):
                    ip_keys_include.append(key)
            print(f"IP keys include: {ip_keys_include}")
            for key in ip_keys_include:
                key = key.replace('_IP', '')
                filtered_doc[key] = doc.get(key)
            print(f"Filtered doc: {filtered_doc}")
            filtered_result.append(filtered_doc)
        return filtered_result
    else:
        return result


def verify_query(query: dict) -> bool:
    """
    Verifies that a query includes fields along with their corresponding _IP fields documenting the intended purposes.

    Args:
        query (dict): The query dictionary to verify.

    Returns:
        bool: True if the query passes the verification, False otherwise.
    """
    query_str = str(query)
    relevant_keys = []

    for key in KEYS:
        if re.search(r'\b' + re.escape(key) + r'\b', query_str):
            relevant_keys.append(key)

    for key in relevant_keys:
        ip_key = f"{key}_IP"
        if re.search(r'\b' + re.escape(ip_key) + r'\b', query_str):
            pass
        else:
            error = f"Missing IP key for {key}."
            logger.error(error)
            return False, error

    return True, None


def re_write_query(query: dict, action: str, access_purpose: str) -> dict:
    """
    Rewrites the given query based on the action and access purpose.

    Args:
        query (dict): The original query.
        action (str): The action to perform on the query. Possible values are 'find', 'countDocuments', or 'aggregate'.
        access_purpose (str): The access purpose to be applied to the query.

    Returns:
        dict: The modified query based on the action and access purpose.

    Raises:
        ValueError: If the action is not one of the valid options or if the query is not a list for the 'aggregate' action.
    """

    relevant_keys = []
    query_str = str(query)

    for key in KEYS:
        if re.search(r'\b' + re.escape(key) + r'\b', query_str):
            relevant_keys.append(key)

    if action == 'find' or action == 'countDocuments' or action == 'findOne':
        modified_query = OrderedDict()
        for key in relevant_keys:
            ip_key = f"{key}_IP"
            modified_query[ip_key] = access_purpose

        modified_query.update(query)
        modified_query = dict(modified_query)

        logger.info(f"Modified NoSQL Query: {modified_query}")
        return modified_query

    elif action == 'aggregate':
        if not isinstance(query, list):
            raise ValueError(
                f"For '{action}', the query should be a list of pipeline stages.")

        match_stage = OrderedDict()
        modified_pipeline = []

        for key in relevant_keys:
            ip_key = f"{key}_IP"
            match_stage[ip_key] = access_purpose

        if match_stage:
            # Add the _IP fields in a $match stage
            modified_pipeline.append({"$match": dict(match_stage)})

        # Append the original pipeline stages
        modified_pipeline.extend(query)

        logger.info(f"Modified NoSQL Query: {modified_pipeline}")
        return modified_pipeline

    else:
        raise ValueError(f"Invalid action: {action}.")


if __name__ == "__main__":
    pass
