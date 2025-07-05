# src/ui/ Folder

The `src/ui/` folder contains all user interface code for the project. This includes Gradio apps, web UIs, and any other UI components.

## What goes in `src/ui/`?
- Gradio app scripts (e.g., `chat_ui.py`)
- Any UI-specific modules, assets, or helpers

## Why use a `ui/` subfolder?
- Keeps UI code organized and separate from backend logic, activities, and utilities
- Makes it easy to extend or replace the UI without affecting core logic

## How to use
- Import UI modules in your main app (e.g., `from src.ui.chat_ui import demo`)
- Add new UI components or apps as needed in this folder
