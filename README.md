# SYL: Simplify Your Life

This project provides a suite of utilities and tools designed to simplify your daily workflow using Generative AI. It helps automate routine tasks, manage and track updates in your codebase, and more. The codebase is modular, allowing for easy extension as new activities and tools are added.

## Key Features
- Automate daily updates and summaries from your codebase (e.g., Git repositories)
- Use AI-powered tools to streamline repetitive or complex tasks
- Modular structure: add new activities and tools as your needs grow
- Designed to help you focus on what matters, letting AI handle the routine

## Documentation
- For detailed documentation on each module and project structure, see the [docs/](docs/README.md) folder.
- Each section in the docs folder provides navigation links for easy browsing.

## Quick Start
- The main activity currently implemented is the daily update, managed by the activities module.
- Prompts for summarization are stored in `src/prompts/` and can be customized.
- Utilities and tools are modular and can be reused in other activities as the project grows.
- Run tests using `python -m unittest discover tests` from the project root.

## Requirements
- Python 3.x
- GitPython (`pip install gitpython`)
- requests (`pip install requests`)
- A locally hosted Qwen LLM (for summarization)

---

For more details, see the documentation in the [docs/](docs/README.md) folder.
