from src.ui.uitools.daily_summary_tool import tool_daily_summary
from src.ui.uitools.hello_world_tool import tool_hello_world

TOOLS = {
    "Hello World": tool_hello_world,
    "Daily Summary": tool_daily_summary
}

def get_tool_function(tool_name):
    """
    Returns the function for the given tool name, or None if not found.
    """
    return TOOLS.get(tool_name)

# Optionally, you can add a function to get the list of tool names
def get_tool_names():
    return list(TOOLS.keys())
