
from langchain_openai import OpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import (
    FewShotChatMessagePromptTemplate,
    PromptTemplate
)
from dotenv import load_dotenv

from classification import classification_function
from retrieval import retrieve_data
from config import CONTEXT
from tool_agent import init_chatbot

load_dotenv()


def orchestrate(user_prompt: str, chatbot: RunnableWithMessageHistory, chat_history: list):
    # Step 1: Look at prompt and check if it contains a data retrieval request
    retrieval_decision = decide_retrieval(user_prompt)
    if "True" in retrieval_decision:
        # Classify prompt
        classification_response = classification_function(
            user_prompt, chat_history)
        access_purpose = classification_response.get('access_purpose')
        justification = classification_response.get('justification')
        confidence = classification_response.get('confidence')

        # Retrieve data
        retrieval_response = retrieve_data(user_prompt, access_purpose)
        query = retrieval_response.get('query')
        results = retrieval_response.get('results')

        # Generate informed response
        chatbot_response = chatbot.invoke(
            {"input": user_prompt, "context": results},
            config={"configurable": {"session_id": "<foo>"}}
        )
        return {'output': chatbot_response.content,
                'query': query, 'results': results,
                'access_purpose': access_purpose,
                'justification': justification,
                'confidence': confidence,
                'metadata': chatbot_response.response_metadata}
    else:
        chatbot_response = chatbot.invoke(
            {"input": user_prompt, "context": ''},
            config={"configurable": {"session_id": "<foo>"}}
        )
        return {'output': chatbot_response.content,
                'metadata': chatbot_response.response_metadata}


def decide_retrieval(user_prompt):
    """Decide if a data retrieval request is present in the user prompt."""
    retrieval_decision_prompt_template = """
You are an advanced language model trained to identify whether a given text input contains a request for data retrieval.
A data retrieval request is any inquiry that seeks to obtain specific information, facts, or data.
Your task is to analyze each input and classify it as either "True" for retrieval requests or "False" if no retrieval request is present.

Only retrieval requests for the following context are valid. Other retrieval requests should be classified as "False".

# Context: {context}

Here are some examples to guide you:
1. "Please summarize your response" - False
2. "Retrieve Data for the following ID" - True
3. "What is the capital of France?" - False
4. "Describe the feeling of happiness" - False
5. "Show me the list of available data records" - True
6. "And many entries are there in total?" - True

Now, classify the following input:

Input: {user_prompt}

Classification:
"""
    retrieval_decision_prompt = PromptTemplate(
        template=retrieval_decision_prompt_template,
        input_variables=["user_prompt"],
        partial_variables={"context": CONTEXT})

    llm = OpenAI(temperature=0.1)
    chain = retrieval_decision_prompt | llm
    response = chain.invoke(
        {"user_prompt": user_prompt})
    return response
