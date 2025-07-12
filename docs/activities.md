# Activities Module (`src/activities`)

This module contains activity logic, such as daily update automation.

## Files

 - `daily_update_activity.py`: Implements the `DaillyUpdateActivity` class.
   - Methods:
     - `run(since_date=None, check_for_current_changes=False, stream=False, callback=None)`: Generates a daily update summary since a specific date, using git history and file changes. Before summarization, the activity checks if Ollama and the Qwen model are running and available (returns a helpful error message if not). The `stream` and `callback` arguments allow for real-time streaming of summary output, useful for UI integration (e.g., Gradio). The `check_for_current_changes` argument enables summarizing current file changes in addition to commit history.

## Usage

Instantiate `DaillyUpdateActivity` and call `run()` to generate a daily update summary. The method will check for Ollama and Qwen model availability, and supports streaming output and callbacks for UI integration. You can also summarize current file changes by setting `check_for_current_changes=True`.

[Back to Main Docs](README.md)
