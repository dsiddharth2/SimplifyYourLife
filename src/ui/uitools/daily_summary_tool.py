from src.ui.message_handler import prepare_message
from datetime import datetime, timedelta
from src.tools.extract_paths import ExtractPathsTool
from src.activities.daily_update_activity import DaillyUpdateActivity

def callback(message, is_done):
    """
    Callback function to handle messages.
    This is a placeholder for any additional processing needed.
    """
    # For now, just return the message as is
    yield prepare_message(message)

def tool_daily_summary(message=None):
    yield prepare_message("Starting Daily Summary tool...")
    
    # check if message is provided
    if message is None:
        yield prepare_message("No input message provided.")
        return
    
    extractPathsTool = ExtractPathsTool()
    result = extractPathsTool.extract_paths_and_summary_with_llm(message)
    
    # Extract project paths from the result dictionary
    project_paths = result.get("project_paths", [])
    work_summary = result.get("work_summary", "")
    
    # Display the work summary to the user
    work_summary_message = ""
    if work_summary and work_summary != "Failed to parse response structure":
        work_summary_message = work_summary
    
    if not project_paths:
        yield prepare_message("No project paths found in the input message.")
        yield prepare_message(f"Debug info: {result}")
        return
    
    # Now read each path and print it back to front end
    daily_activity = DaillyUpdateActivity(project_paths, work_summary_message)

    # Get yesterday's date
    since_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    response = daily_activity.run(since_date=since_date, stream=True, check_for_current_changes=True, callback=callback)
    if response:
        yield prepare_message(f"{response}")
    else:
        yield prepare_message(f"No updates found for the specified project paths.")
    #end for