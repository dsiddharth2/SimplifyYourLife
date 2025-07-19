import gradio as gr
import os
import sys
sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)
from src.ui.tools_list import TOOLS, get_tool_function
from src.ui.message_handler import prepare_message

# Gradio ChatInterface handler
def syl_chat_fn(message, history, tool):
    tools_method = get_tool_function(tool)
    if tools_method is None:
        yield prepare_message("No tool selected or tool not found.")
        return

    response_history = []
    tool_result = tools_method(message)
    if hasattr(tool_result, '__iter__') and not isinstance(tool_result, str):
        for msg in tool_result:
            response_history.append(msg)
            yield response_history
    yield response_history

# Build UI
with gr.Blocks(title="SYL") as demo:
    gr.ChatInterface(
        syl_chat_fn,
        type="messages",
        chatbot=gr.Chatbot(height="70vh"),
        additional_inputs=[
            gr.Dropdown(choices=list(TOOLS.keys()), label="Select a Tool")
        ]
    )
# #For Debugging and direct runs
# demo.launch(show_api=False, show_error=False)

if __name__ == "__main__":
    demo.launch()