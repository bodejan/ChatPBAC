import json
from langchain.pydantic_v1 import BaseModel, Field
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.output_parsers import OutputFixingParser

from dotenv import load_dotenv

from config import get_purpose_names, PURPOSES_v2

import logging

logger = logging.getLogger()

PBAC_CLASSIFICATION_TEMPLATE = """You are a helpful assistant that classifies a text input into a predefined hierarchical access purpose category. 

The following categories exist:

{purpose_description}

{format_instructions}

Classify the input into one of the described categories. Use the most specific category.

Input: {user_prompt}

Output:"""


def filter_json(input: str) -> str:
    """
    Filter a JSON object from a string.

    Args:
        input (str): The input string possibly containing a JSON object.

    Returns:
        str: The extracted JSON object if found, otherwise the input string unchanged.

    Example:
        >>> input = "This is some text before {'key': 'value'} and more text after."
        >>> filtered_json = filter_json(input)
        >>> print(filtered_json)
        {'key': 'value'}
    """
    # Find the index of the first opening bracket
    start_index = input.find('{')
    if start_index == -1:
        return input

    # Find the index of the last closing bracket
    end_index = input.rfind('}')
    if end_index == -1:
        return input

    # Extract the JSON object between the first opening bracket and the last closing bracket
    json_string = input[start_index:end_index+1]

    return json_string


def validate_access_purpose(input):
    """
    Validate if the input dictionary contains access_purpose, confidence, and justification,
    where access_purpose must be one of the PURPOSE_CODES.

    Args:
        input (dict): The dictionary to be validated. It should have the following structure:
            {
                "access_purpose": str,  # One of the PURPOSE_CODES
                "confidence": float,
                "justification": str
            }

    Returns:
        bool: True if the input dictionary is valid, False otherwise.

    Example:
        >>> input_dict1 = {"access_purpose": "Research", "confidence": 0.9, "justification": "Lorem ipsum"}
        >>> validate_dict(input_dict1)
        True

        >>> input_dict2 = {"access_purpose": "Marketing", "confidence": 0.8}
        >>> validate_dict(input_dict2)
        False

        >>> input_dict3 = {"access_purpose": "Development", "confidence": 0.7, "justification": "Lorem ipsum"}
        >>> validate_dict(input_dict3)
        False
    """
    # Check if input is a dictionary
    if not isinstance(input, dict):
        return False

    # Check if required keys are present
    required_keys = {"access_purpose", "confidence", "justification"}
    if not required_keys.issubset(input.keys()):
        return False

    # Check if access_purpose is one of the PURPOSE_CODES
    if input["access_purpose"] not in get_purpose_names():
        return False

    return True


class Classification(BaseModel):
    access_purpose: str = Field(
        description="the identified access purpose", enum=get_purpose_names())
    confidence: float = Field(description="the confidence at which the access purpose was identified", enum=[
        x / 10 for x in range(1, 11)])
    justification: str = Field(
        description="the justification why the access purpose was identified")


def classification_function(user_prompt):
    """Prompt classification function."""
    llm = OpenAI(temperature=0.1)
    parser = JsonOutputParser(pydantic_object=Classification)
    format_instructions = parser.get_format_instructions()
    format_instructions += "\nDo not use quotation marks in your justification to avoid json formatting errors."
    purpose_description = [(key, value['description'])
                           for key, value in PURPOSES_v2.items()]
    prompt = PromptTemplate(
        template=PBAC_CLASSIFICATION_TEMPLATE,
        input_variables=["user_prompt"],
        partial_variables={"format_instructions": format_instructions,
                           "purpose_description": purpose_description},
    )

    chain = prompt | llm | filter_json | parser

    try:
        response = chain.invoke({"user_prompt": user_prompt})
        if not validate_access_purpose(response):
            raise OutputParserException(llm_output=response)

    except OutputParserException as ope:
        output_fixing_parser = OutputFixingParser.from_llm(
            parser=parser, llm=llm)
        response = output_fixing_parser.parse(ope.llm_output)
        if not validate_access_purpose(response):
            raise Exception
    except Exception as e:
        response = {}
        response['access_purpose'] = "None"
        response['justification'] = "An error occurred during the access purpose classification of the user prompt. Please specify the access purpose. Describe the access purpose in more detail or state it explicitly."
        response['error_msg'] = str(e)

    logger.info(f"Classification response: {response}")
    return response


if __name__ == '__main__':
    load_dotenv()
    print(classification_function(
        "I want to use the data for public research purposes."))
