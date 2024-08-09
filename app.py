from llm import init_chat
import gradio as gr
import asyncio

from config import PURPOSES
from orchestration import orchestrate
from retrieval import create_temp_pbac_table

llm = init_chat()

with gr.Blocks(
    title="PBAC-enhanced Chatbot",
) as chat_app:

    gr.Markdown(
        "# PBAC-enhanced Chatbot\n" +
        "This chatbot is designed to help you with your data access requests.\n" +
        "Remember to provide your data access purpose and signal a desired retrieval with keywords like *retrieve*, *query*, or *search*.\n",
        line_breaks=True
    )

    access_purpose = gr.Dropdown(
        choices=list(PURPOSES.keys()), interactive=True, label='Data Access Purpose')

    chatbot = gr.Chatbot(show_copy_button=True)
    msg = gr.Textbox()

    def respond(message, chat_history, access_purpose):
        if access_purpose is None:
            chat_history.append(
                (message, 'Please provide a "Data Access Purpose".'))
            return "", chat_history
        else:
            response = orchestrate(
                message, llm, chat_history, access_purpose)
            chat_history = response.get('chat_history')

        return "", chat_history

    msg.submit(respond, [msg, chatbot, access_purpose],
               [msg, chatbot])

    clear = gr.ClearButton(
        [msg, chatbot, access_purpose])

    async def update(access_purpose):
        asyncio.create_task(asyncio.to_thread(
            create_temp_pbac_table, access_purpose))
        return access_purpose, None, None

    async def create_temp_pbac_table_async(access_purpose):
        await asyncio.to_thread(create_temp_pbac_table, access_purpose)

    access_purpose.change(update, inputs=[access_purpose], outputs=[
                          access_purpose, msg, chatbot])


if __name__ == "__main__":
    chat_app.launch()
