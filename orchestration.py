
from langchain_openai import OpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import (
    FewShotChatMessagePromptTemplate,
    PromptTemplate
)
from dotenv import load_dotenv
import logging

from classification import classification_function
from retrieval import retrieve_data, decide_retrieval
from config import CONTEXT, PURPOSE_CODES, PURPOSE_NAMES
from llm import extend_chat_history, format_chat_history, get_user_context_prompt

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
            chat_history, user_prompt, chatbot_response)
        return {'output': chatbot_response.content,
                'metadata': chatbot_response.response_metadata,
                'chat_history': chat_history}
