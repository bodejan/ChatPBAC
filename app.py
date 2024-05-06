from tool_agent import init_agent
import gradio as gr

from config import PURPOSE_CODES, PURPOSE_NAMES
from classification import classification_function, validate_access_purpose

llm = init_agent()

with gr.Blocks() as chat_app:
    access_purpose = gr.Dropdown(choices=PURPOSE_NAMES, value='None', interactive=True, label='Data Access Purpose')
    temp = gr.Slider(0, 1, 0.1, interactive=True, label='LLM Temperature')
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history, access_purpose):
        classification_response = classification_function(message, chat_history)
        """ response = llm.invoke(
            {"input": message},
            config={"configurable": {"session_id": "<foo>"}}
        ) """
        response = {}
        response['output'] = 'Hi'
        #print(response.get('intermediate_steps'))
        output = response.get('output')
        access_purpose_index = PURPOSE_CODES.index(classification_response.get('access_purpose'))
        chat_history.append((message, f'Access purposes: {PURPOSE_NAMES[access_purpose_index]}\nJustification: {classification_response.get('justification', 'Sorry, there is no justification available.')}\nConfidence: {classification_response.get('confidence', 'Sorry, there is no confidence score available.')}'))
        chat_history.append((None, output))

        return "", chat_history, gr.update(value=PURPOSE_NAMES[access_purpose_index])

    msg.submit(respond, [msg, chatbot, access_purpose], [msg, chatbot, access_purpose])

if __name__ == "__main__":
    chat_app.launch()
