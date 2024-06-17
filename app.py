from llm import init_chat
import gradio as gr

from config import PURPOSES_v2
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
        choices=list(PURPOSES_v2.keys()), interactive=True, label='Data Access Purpose')

    def update(access_purpose):
        create_temp_pbac_table(access_purpose)

    access_purpose.change(update, access_purpose)

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


if __name__ == "__main__":
    chat_app.launch()
