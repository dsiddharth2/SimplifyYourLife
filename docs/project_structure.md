# Project Structure

The project is organized as follows:

```
SYL/
├── src/
│   ├── activities/
│   │   └── daily_update_manager.py
│   ├── prompts/
│   │   └── summarize_file_changes.txt
│   ├── tools/
│   │   └── git_tools.py
│   ├── utils/
│   │   └── qwen_summarizer.py
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

- `src/` - Main source code directory
  - `activities/` - Activity logic (e.g., daily update automation)
  - `prompts/` - Prompt templates for summarization and reporting
  - `tools/` - Utility classes for interacting with git and other tools
  - `utils/` - Helper utilities (e.g., summarization)
- `tests/` - Unit and integration tests for each module
- `requirements.txt` - Python dependencies
- `README.md` - Project overview

[Back to Main Docs](README.md)
