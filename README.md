# DaillyUpdate

This project provides utilities for managing and tracking updates in a codebase, with a focus on Git repositories and automated daily update summaries. The codebase is modular, with each directory under `src` and `tests` serving a specific purpose.

## Folder Structure

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

## Directory Overview

### src/activities/
- **daily_update_manager.py**: Implements the main activity for the project, which is the daily update activity. It manages scanning a Git repository, collecting file changes, and generating summaries.

### src/prompts/
- **summarize_file_changes.txt**: Template prompt for summarizing file changes. Placeholders like `{file_name}` and `{file_modifications}` are replaced at runtime for LLM summarization.

### src/tools/
- **git_tools.py**: Contains the `GitTools` class for interacting with Git repositories, including reading current changes and changes since a specific commit date, and retrieving diffs.

### src/utils/
- **qwen_summarizer.py**: Utility for summarizing text using a locally hosted Qwen LLM. Supports prompt templates and dynamic replacements, and cleans up model responses for user display.

### tests/
- **test_create_update.py**: Legacy or example test for earlier update scripts.
- **tools/test_git_tools.py**: Tests for the `GitTools` class, running against a real Git repository.
- **utils/test_qwen_summarizer.py**: Tests the Qwen summarizer utility, including prompt replacement and LLM integration.

## Usage
- The main activity is the daily update, managed by `daily_update_manager.py`.
- Prompts for summarization are stored in `src/prompts/` and can be customized.
- Utilities and tools are modular and can be reused in other activities as the project grows.
- Run tests using `python -m unittest discover tests` from the project root.

## Requirements
- Python 3.x
- GitPython (`pip install gitpython`)
- requests (`pip install requests`)
- A locally hosted Qwen LLM (for summarization)

## Example
The daily update activity scans a Git repository, collects file changes, and uses the Qwen LLM to generate a summary based on a customizable prompt. Tests are provided for all major utilities.

---
**Note:** Only the daily update activity is currently implemented. The structure is designed for easy extension as new activities and tools are added.
