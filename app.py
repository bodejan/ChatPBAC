from langchain_community.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import openai
import gradio as gr

from tool_agent import init_agent

llm = init_agent()

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    response = llm.invoke(
        {"input": message},
        config={"configurable": {"session_id": "<foo>"}}
    )
    print(response)
    return response.get('output')

gr.ChatInterface(predict).launch()