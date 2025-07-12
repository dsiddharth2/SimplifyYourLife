# Utils Module (`src/utils`)

This module provides helper utilities for the project.

## Files

- `qwen_summarizer.py`: Contains the `QwenSummarizer` class for summarizing text using prompt templates.

## Usage

Import and use `QwenSummarizer` to generate summaries from text or prompt files. The `check_ollama_and_model()` method checks if Ollama is running and if the Qwen model is available, returning a status and message. The `summarize_from_text` and `summarize` methods support streaming output and callback functions for real-time UI integration.

[Back to Main Docs](README.md)
