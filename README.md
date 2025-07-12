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

## Prerequisites
  - **Ollama must be installed and running.**
  - **You must pull and have the Qwen or Qwen3:latest model installed in Ollama before running this project.**  
  - To install Qwen3:latest, run: `ollama pull qwen3:latest`
  - For more info, see [Ollama documentation](https://ollama.com/)
  - For Qwen model info, see [Qwen on Ollama](https://ollama.com/library/qwen3)
  - A locally hosted Qwen LLM (for summarization)

---

## Releases
- The current stable release is **v1.0**. See the release notes in [docs/release_notes/v1.0.md](docs/release_notes/v1.0.md) for details.
- We encourage you to use v1.0 and contribute feedback, bug reports, or new features via pull requests and issues.

For more details, see the documentation in the [docs/](docs/README.md) folder.

## Contributing
We welcome contributions from the community! You can help by:
- Reporting bugs or issues
- Suggesting new features or improvements
- Submitting pull requests for code, documentation, or tests

**Contribution Guidelines:**
- Please create your feature or fix branches from the `development` branch (not `main`).
- After making your changes, submit a pull request to merge your branch into `development`.
- Review the release notes and documentation before contributing.
- For major changes, open an issue first to discuss what you would like to change.
