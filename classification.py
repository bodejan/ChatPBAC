import json
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_openai import ChatOpenAI, OpenAI
from langchain.chains import create_sql_query_chain
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    PromptTemplate
)
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain.output_parsers import OutputFixingParser

from config import PURPOSE_CODES, get_purpose_data

import logging

logger = logging.getLogger()

PBAC_SYSTEM = f"""You are a helpful assistant that classifies a text input into a predefined access purpose category.

The following categories exist:

{get_purpose_data()}

Classify the input into one of the described categories.
Use the defined category code.
Always return your answer in a json format.
Remember to only return a json string.
"""


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
    if input["access_purpose"] not in PURPOSE_CODES:
        return False

    return True


class Classification(BaseModel):
    access_purpose: str = Field(
        description="the identified access purpose", enum=PURPOSE_CODES)
    confidence: float = Field(description="the confidence at which the access purpose was identified", enum=[
                              x / 10 for x in range(1, 11)])
    justification: str = Field(
        description="the justification why the access purpose was identified")


def classification_function(user_prompt, chat_history):
    """Prompt classification function."""
    classification_template = PBAC_SYSTEM + \
        """\n\n{format_instructions}""" + """\n\nInput: {user_prompt}"""
    llm = OpenAI(temperature=0.1)
    parser = JsonOutputParser(pydantic_object=Classification)
    prompt = PromptTemplate(
        template=classification_template,
        input_variables=["user_prompt"],
        partial_variables={"format_instructions": parser.get_format_instructions(
        ) + "\nDo not use quotation marks in your justification to avoid json formatting errors."},
    )

    chain = prompt | llm | filter_json | parser

    try:
        response = chain.invoke({"user_prompt": user_prompt})
        if 'access_purpose' in response and response['access_purpose'] == 'None':
            response = history_classification_function(chat_history)

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

    return response


class ClassificationInput(BaseModel):
    user_prompt: str = Field(description="the original user prompt")
    chat_history: str = Field(description="the chat history as a string")


@tool(args_schema=ClassificationInput)
def classification_tool(user_prompt: str, chat_history: str):
    """Prompt classification tool. Always use this tool before information retrieval. This tool classifies the access purposes of the user."""
    response = classification_function(user_prompt, chat_history)

    return response


def history_classification_function(chat_history: str):
    """History classification function."""
    logger.info(f'No access purpose in prompt identified, analyzing chat history: {
                chat_history}')
    classification_template = PBAC_SYSTEM + \
        '\n\n{format_instructions}' + '\n\Input: {chat_history}'
    llm = OpenAI(temperature=0.1)
    parser = JsonOutputParser(pydantic_object=Classification)
    prompt = PromptTemplate(
        template=classification_template,
        input_variables=["chat_history"],
        partial_variables={"format_instructions": parser.get_format_instructions(
        ) + "\nDo not use quotation marks in your justification to avoid formatting errors."},
    )

    chain = prompt | llm | filter_json | parser

    try:
        response = chain.invoke({"chat_history": chat_history})
    except OutputParserException as ope:
        output_fixing_parser = OutputFixingParser.from_llm(
            parser=parser, llm=llm)
        response = output_fixing_parser.parse(ope.llm_output)
    except Exception as e:
        response = {}
        response['access_purpose'] = "None"
        response['justification'] = "An error occurred during the access purpose classification of the user prompt. Please specify the access purpose. Describe the access purpose in more detail or state it explicitly."
        response['error_msg'] = str(e)

    return response
