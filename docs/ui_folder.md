# src/ui/ Folder

The `src/ui/` folder contains all user interface code for the project. This includes Gradio apps, web UIs, and any other UI components.

## What goes in `src/ui/`?
- Gradio app scripts (e.g., `chat_ui.py`)
- Any UI-specific modules, assets, or helpers
- The `uitools/` directory for tool implementations

## Why use a `ui/` subfolder?
- Keeps UI code organized and separate from backend logic, activities, and utilities
- Makes it easy to extend or replace the UI without affecting core logic

## Structure and Responsibilities

- **`chat_ui.py`**: The main entry point for the UI. This file sets up the initial Gradio interface and connects user input to the available tools.
- **`uitools/` directory**: Contains all tool implementations that can be used from the UI. Each tool is a Python module (e.g., `daily_summary_tool.py`, `hello_world_tool.py`) and exposes a callable interface for the UI to use.
- **`tools_list.py`**: Provides a list of available tools and maps tool names to their corresponding functions. This file also contains code to retrieve tool functions by name.
- **`message_handler.py`**: Handles the preparation and sending of messages (including yielded messages) from the backend to the frontend, ensuring proper formatting and delivery.

## How to use
- Import UI modules in your main app (e.g., `from src.ui.chat_ui import demo`)
- Add new UI components or apps as needed in this folder
- Add new tools to the `uitools/` directory and register them in `tools_list.py` to make them available in the UI
