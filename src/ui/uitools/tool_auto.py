from src.ui.message_handler import prepare_message

def tool_auto(message=None):
    yield prepare_message("Starting Hello World tool...")
    import time
    time.sleep(2)
    yield prepare_message("Halfway done...")
    time.sleep(2)
    yield prepare_message("Tool [Hello World] : Hello from the tool!")
