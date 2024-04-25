from langchain.agents.mrkl import prompt as react_prompt
from langchain_core.prompts import BasePromptTemplate, PromptTemplate

from prompt import *

def create_custom_sql_agent_prompt(table_info):
    """Create a custom prompt for the sql retrieval agent. Prompts are based on react_prompt.PREFIX, FORMAT_INSTRUCTIONS, and SUFFIX."""

    template = "\n\n".join(
        [
            CUSTOM_PREFIX,
            CUSTOM_METADATA_INSTRUCTIONS,
            table_info,
            CUSTOM_FORMAT_INSTRUCTIONS,
            CUSTOM_SUFFIX,
        ]
    )

    prompt = PromptTemplate.from_template(template)

    return prompt

def create_system_prompt():
    template = "\n\n".join(
        [
            SYSTEM_PREFIX,
            SYSTEM_FORMAT_INSTRUCTIONS,
            SYSTEM_SUFFIX
        ]
    )
    return template

