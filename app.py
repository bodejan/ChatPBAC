from tool_agent import init_agent, init_chatbot
import gradio as gr

from config import PURPOSE_CODES, PURPOSE_NAMES
from classification import classification_function
from orchestration import orchestrate

purpose_llm = init_chatbot()
llm = init_chatbot()

with gr.Blocks(
    title="PBAC-enhanced Chatbot",
) as chat_app:

    gr.Markdown(
        "# PBAC-enhanced Chatbot\n" +
        "*This chatbot is designed to help you with your data access requests.*\n" +
        "*Remember to provide your data access purpose and signal a desired retrieval with keywords like 'retrieve', 'query', or 'search'.*\n",
        line_breaks=True
    )

    with gr.Tab(label="Access Purpose Identification"):

        access_purpose = gr.Dropdown(
            choices=PURPOSE_NAMES, interactive=True, label='Data Access Purpose')

        purpose_chatbot = gr.Chatbot(
            label="PBAC Identification Bot",
            show_label=True)

        purpose_msg = gr.Textbox(
            placeholder="Please describe your data access purpose. Alternatively, use the select-box above.")

        purpose_clear = gr.ClearButton(
            [purpose_msg, purpose_chatbot, access_purpose])

        def purpose_respond(message, chat_history):
            response = classification_function(message, chat_history)
            access_purpose_index = PURPOSE_CODES.index(
                response.get('access_purpose'))
            chat_history.append(
                (message,
                 f'Identified Access Purposes: {PURPOSE_NAMES[access_purpose_index]}\n' +
                 f'Justification: {response.get("justification", "Sorry, there is no justification available.")}\n' +
                 f'Confidence: {response.get("confidence", "Sorry, there is no confidence score available.")}\n' +
                 'If the identification was incorrect, please provide a more detailed description of your data access purpose.')
            )

            return "", chat_history, gr.update(value=PURPOSE_NAMES[access_purpose_index]), gr.update(value=PURPOSE_NAMES[access_purpose_index])

    with gr.Tab(label="RAG-based Chatbot"):

        access_purpose_mirror = gr.Dropdown(
            choices=PURPOSE_NAMES, interactive=False, label='Data Access Purpose')

        chatbot = gr.Chatbot(show_copy_button=True)
        msg = gr.Textbox()

        def respond(message, chat_history, access_purpose):
            response = orchestrate(message, llm, chat_history)
            if response.get('access_purpose', None) is not None:
                access_purpose_index = PURPOSE_CODES.index(
                    response.get('access_purpose'))
                # chat_history.append((message, f'Access purposes: {PURPOSE_NAMES[access_purpose_index]}\nJustification: {response.get(
                #    'justification', 'Sorry, there is no justification available.')}\nConfidence: {response.get('confidence', 'Sorry, there is no confidence score available.')}'))
                chat_history.append(
                    (message,
                     f'Access Purposes: {PURPOSE_NAMES[access_purpose_index]}\n' +
                     f'Justification: {response.get("justification", "Sorry, there is no justification available.")}\n' +
                     f'Confidence: {response.get("confidence", "Sorry, there is no confidence score available.")}\n' +
                     f'Query: {response.get(
                         "query", "Sorry, there is no query available.")}\n' +
                     f'Query Results: {response.get(
                         "results", "Sorry, there are no results available.")}'
                     )
                )
                chat_history.append((None, response.get('output')))
            else:
                access_purpose_index = PURPOSE_CODES.index(
                    'None')
                chat_history.append((message, response.get('output')))

            return "", chat_history, gr.update(value=PURPOSE_NAMES[access_purpose_index])

        msg.submit(respond, [msg, chatbot, access_purpose],
                   [msg, chatbot, access_purpose])

        clear = gr.ClearButton([msg, chatbot])

    # Purpose identification actions
    purpose_msg.submit(purpose_respond, [purpose_msg, purpose_chatbot],
                       [purpose_msg, purpose_chatbot, access_purpose, access_purpose_mirror])


if __name__ == "__main__":
    chat_app.launch()
