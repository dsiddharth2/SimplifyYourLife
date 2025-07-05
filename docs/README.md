# Project Overview

This documentation provides a detailed overview of the project structure, modules, and usage. For a quick start, see the main README in the project root. Use the navigation links below to explore each section:

- [Project Structure](project_structure.md)
- [Activities](activities.md)
- [Prompts](prompts.md)
- [Tools](tools.md)
- [Utils](utils.md)
- [Tests](tests.md)
- [Release Folder](release_folder.md)
- [UI](ui_folder.md)


---

## Quick Start
- The main activity is the daily update, managed by the activities module.
- Prompts for summarization are stored in `src/prompts/` and can be customized.
- Utilities and tools are modular and can be reused in other activities as the project grows.
- Run tests using `python -m unittest discover tests` from the project root.

## Requirements
- Python 3.x
- GitPython (`pip install gitpython`)
- requests (`pip install requests`)
- A locally hosted Qwen LLM (for summarization)

