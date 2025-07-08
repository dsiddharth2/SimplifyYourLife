"""
message_handler.py

Utility functions for preparing and handling chat messages in the SYL UI.
"""

def prepare_message(message):
    """
    Create a user message dictionary for chat history.

    Args:
        message (str): The user's message text.

    Returns:
        dict: A dictionary with 'role' set to 'user' and 'content' set to the message.
    """
    return {"role": "user", "content": message}

