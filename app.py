from tool_agent import init_agent, init_chatbot
import gradio as gr

from config import PURPOSE_CODES, PURPOSE_NAMES
from classification import classification_function
from orchestration import orchestrate

llm = init_chatbot()

with gr.Blocks() as chat_app:
    access_purpose = gr.Dropdown(
        choices=PURPOSE_NAMES, value='None', interactive=True, label='Data Access Purpose')
    temp = gr.Slider(0, 1, 0.1, interactive=True, label='LLM Temperature')
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

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

if __name__ == "__main__":
    chat_app.launch()
