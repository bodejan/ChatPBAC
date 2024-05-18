
from langchain_openai import OpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import (
    FewShotChatMessagePromptTemplate,
    PromptTemplate
)
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv
import logging

from classification import classification_function
from retrieval import retrieve_data
from config import CONTEXT, PURPOSE_CODES, PURPOSE_NAMES
from llm import init_chatbot

load_dotenv()
logger = logging.getLogger()


def orchestrate(user_prompt: str, chatbot: RunnableWithMessageHistory, chat_history: list, access_purpose_name: str = None):
    # Step 1: Look at prompt and check if it contains a data retrieval request
    logger.info(f"Gradio chat history: {chat_history}")
    retrieval_decision = decide_retrieval(user_prompt, chat_history)
    if "True" in retrieval_decision:
        if access_purpose_name is not None:
            logger.info(f'Access purpose provided by user: {
                        access_purpose_name}')
            access_purpose = PURPOSE_CODES[PURPOSE_NAMES.index(
                access_purpose_name)]
            justification = 'User-provided access purpose'
            confidence = 1.0
        else:
            # Classify prompt
            classification_response = classification_function(
                user_prompt)
            access_purpose = classification_response.get('access_purpose')
            justification = classification_response.get('justification')
            confidence = classification_response.get('confidence')

        # Retrieve data
        retrieval_response = retrieve_data(user_prompt, access_purpose)
        query = retrieval_response.get('query')
        results = retrieval_response.get('results')
        user_context_prompt = get_user_context_prompt(
            user_prompt, query, results)

        lang_chat_history = format_chat_history(
            chat_history, user_context_prompt)

        chatbot_response = chatbot.invoke(lang_chat_history)
        chat_history = extend_chat_history(
            chat_history, user_context_prompt, chatbot_response)
        logger.info(f"Chatbot response: {chatbot_response}")

        return {'output': chatbot_response.content,
                'query': query, 'results': results,
                'access_purpose': access_purpose,
                'justification': justification,
                'confidence': confidence,
                'metadata': chatbot_response.response_metadata,
                'chat_history': chat_history}
    else:
        lang_chat_history = format_chat_history(chat_history, user_prompt)
        chatbot_response = chatbot.invoke(lang_chat_history)
        chat_history = extend_chat_history(
            chat_history, user_prompt, chatbot_response.content)
        return {'output': chatbot_response.content,
                'metadata': chatbot_response.response_metadata,
                'chat_history': chat_history}


def format_chat_history(chat_history, user_prompt):
    history_langchain_format = []
    for human, ai in chat_history:
        if human is None:
            human = ""
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=user_prompt))

    return history_langchain_format


def extend_chat_history(chat_history, user_prompt, chatbot_response):
    chat_history.append((user_prompt, chatbot_response.content))
    return chat_history


def get_user_context_prompt(user_prompt, query, results):
    def get_context(query, results):
        context = f"""SQL Retrieval Context:
Query:
```sql
{query}
```
Results:
```
{results}
```
"""
        return context
    context = get_context(query, results)
    user_context_prompt = user_prompt + "\n\n" + context
    return user_context_prompt


def decide_retrieval(user_prompt, chat_history):
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

Chat history: {chat_history}
Input: {user_prompt}

Classification:
"""
    retrieval_decision_prompt = PromptTemplate(
        template=retrieval_decision_prompt_template,
        input_variables=["user_prompt", "chat_history"],
        partial_variables={"context": CONTEXT})

    llm = OpenAI(temperature=0.1)
    chain = retrieval_decision_prompt | llm
    response = chain.invoke(
        {"user_prompt": user_prompt, "chat_history": chat_history})
    logger.info(f"Retrieval Decision: {response}")
    return response
