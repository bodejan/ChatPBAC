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
            "{tools}",
            CUSTOM_FORMAT_INSTRUCTIONS,
            CUSTOM_SUFFIX,
        ]
    )

    prompt = PromptTemplate.from_template(template)

    return prompt