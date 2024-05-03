from tool_agent import init_agent
import gradio as gr

from config import PURPOSE_NAMES
llm = init_agent()

with gr.Blocks() as chat_app:
    access_purpose = gr.Dropdown(choices=PURPOSE_NAMES, value='None', interactive=True, label='Data Access Purpose')
    temp = gr.Slider(0, 1, 0.1, interactive=True, label='LLM Temperature')
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history, access_purpose):
        response = llm.invoke(
            {"input": message},
            config={"configurable": {"session_id": "<foo>"}}
        )
        print(response.get('intermediate_steps'))
        output = response.get('output')
        chat_history.append((message, f'Identified access purposes: {access_purpose}'))
        chat_history.append((None, output))

        return "", chat_history, access_purpose

    msg.submit(respond, [msg, chatbot, access_purpose], [msg, chatbot])

if __name__ == "__main__":
    chat_app.launch()
