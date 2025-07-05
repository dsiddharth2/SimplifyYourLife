# Project Structure

The project is organized as follows:

```
SYL/
├── release/
│   ├── app.spec
│   ├── hooks/
│   ├── runtime_hook.py
│   └── deploy_scripts/
├── src/
│   ├── activities/
│   │   └── daily_update_manager.py
│   ├── prompts/
│   │   └── summarize_file_changes.txt
│   ├── tools/
│   │   └── git_tools.py
│   ├── utils/
│   │   └── qwen_summarizer.py
│   ├── ui/
│   │   └── chat_ui.py
│   └── __init__.py
├── tests/
│   ├── test_create_update.py
│   ├── tools/
│   │   └── test_git_tools.py
│   └── utils/
│       └── test_qwen_summarizer.py
├── requirements.txt
└── README.md
```

- [release/ - Deployment, packaging, and build scripts](release_folder.md)
- src/ - Main source code directory
  - activities/ - Activity logic (e.g., daily update automation)
  - prompts/ - Prompt templates for summarization and reporting
  - tools/ - Utility classes for interacting with git and other tools
  - utils/ - Helper utilities (e.g., summarization)
  - [ui/ - User interface code (e.g., Gradio apps)](ui_folder.md)
- tests/ - Unit and integration tests for each module
- requirements.txt - Python dependencies
- README.md - Project overview

[Back to Main Docs](README.md)
