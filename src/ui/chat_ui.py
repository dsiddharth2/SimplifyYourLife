import gradio as gr
from src.activities.daily_update_activity import DaillyUpdateActivity

# Define your tools as functions
def tool_daily_summary():
    project_dir = "C:\\2_WorkSpace\\BluB0X\\BBX_AI"
    activity = DaillyUpdateActivity(project_dir)
    summary = activity.run(since_date='2025-07-02')
    return summary

def tool_hello_world():
    return "Hello from the tool!"

TOOLS = {
    "Daily Summary": (tool_daily_summary, "Summarize daily project updates."),
    "Hello World": (tool_hello_world, "Say hello from a tool."),
}

initial_message = {
    "role": "assistant",
    "content": (
        "**About SYL: Simplify Your Life**\n\n"
        "SYL provides a suite of utilities and tools designed to simplify your daily workflow using Generative AI. "
        "It helps automate routine tasks, manage and track updates in your codebase, and more. The codebase is modular, "
        "allowing for easy extension as new activities and tools are added.\n\n"
        "- Automate daily updates and summaries from your codebase (e.g., Git repositories)\n"
        "- Use AI-powered tools to streamline repetitive or complex tasks\n"
        "- Modular structure: add new activities and tools as your needs grow\n"
        "- Designed to help you focus on what matters, letting AI handle the routine\n\n"
        "Chat with your local SYL assistant and use tools below!"
    )
}

def chat_fn(message, tool_name):
    if tool_name and tool_name in TOOLS:
        tool_func, _ = TOOLS[tool_name]
        tool_result = tool_func()
        return [{"role": "user", "content": message}, {"role": "assistant", "content": f"Tool [{tool_name}] output:\n{tool_result}"}]
    return [{"role": "user", "content": message}, {"role": "assistant", "content": "No tool selected or tool not found."}]

# Fix: Ensure all chat history is a list of dicts with 'role' and 'content'
with gr.Blocks(title="SYL") as demo:
    chatbot = gr.Chatbot(type="messages", value=[initial_message], height="80vh")
    with gr.Row():
        tool_selector = gr.Dropdown(
            choices=list(TOOLS.keys()),
            label="Select a Tool",
            value="Daily Summary"  # Set default selection
        )
        msg = gr.Textbox(label="Message", scale=5)  # Make message box wider

    def user_submit(message, tool_name):
        return chat_fn(message, tool_name), ""

    msg.submit(
        user_submit,
        inputs=[msg, tool_selector],
        outputs=[chatbot, msg]
    )

# For Debugging and direct runs
#demo.launch(show_api=False, show_error=False)

if __name__ == "__main__":
    demo.launch()