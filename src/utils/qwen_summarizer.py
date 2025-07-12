"""
QwenSummarizer Utility
----------------------

This module provides the QwenSummarizer class, which interfaces with a locally hosted Qwen language model API to generate summaries from prompts or text. It supports both standard and streaming responses, with optional callback handling for real-time output (e.g., for UI applications).

Key Features:
- Summarize content from prompt files or direct text input.
- Supports streaming output with callback for chunk-wise processing.
- Cleans up model output by removing <think>...</think> sections.
- Designed for integration with local Qwen model API (default: http://localhost:11434).

Classes:
    QwenSummarizer: Main class for summarization tasks.

Example Usage:
    summarizer = QwenSummarizer()
    summary = summarizer.summarize_from_text("Summarize this text.")

    # With streaming and callback
    def my_callback(chunk, is_done):
        print(chunk, end='')
    summarizer.summarize_from_text("Summarize this text.", stream=True, callback=my_callback)
"""

import requests
import json
import re
from typing import List, Tuple

class QwenSummarizer:
    def __init__(self, host="http://localhost:11434", model="qwen3"):
        """
        Initialize the QwenSummarizer.

        Args:
            host (str): The base URL of the Qwen model API.
            model (str): The model name to use for summarization.
        """
        self.api_url = f"{host}/api/generate"
        self.api_tags = f"{host}/api/tags"
        self.model = model

    def remove_think_section(self, text):
        """
        Remove all <think>...</think> sections from the given text.

        Args:
            text (str): The text to clean.
        Returns:
            str: The cleaned text without <think> sections.
        """
        return re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)

    def _post_to_model(self, prompt, stream=False, callback=None, remove_think=True):
        """
        Send a prompt to the Qwen model API and return the response.

        Args:
            prompt (str): The prompt to send to the model.
            stream (bool): Whether to use streaming response.
            callback (callable, optional): Callback for streaming. Called with (chunk, is_done).
            remove_think (bool): Whether to remove <think>...</think> sections from the output.
        Returns:
            dict: The model's response.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.api_url, data=json.dumps(payload), headers=headers, stream=stream)
        response.raise_for_status()
        
        if stream and callback:
            return self._handle_streaming_response(response, callback, remove_think=remove_think)
        else:
            return response.json()

    def _handle_streaming_response(self, response, callback, remove_think=True):
        """
        Handle streaming response from the model, calling the callback with each chunk.
        Optionally removes <think>...</think> sections from the streamed output.

        Args:
            response: The streaming response object from requests.
            callback (callable): Function to call with each chunk and done flag.
            remove_think (bool): Whether to remove <think>...</think> sections from the output.
        Returns:
            dict: The full response and done status.
        """
        if remove_think:
            buffer = ['']
            def process_chunk(chunk, is_done):
                import re
                buffer[0] += chunk
                cleaned = ''
                pattern = re.compile(r'<think>.*?</think>\s*', re.DOTALL)
                while True:
                    match = pattern.search(buffer[0])
                    if not match:
                        break
                    cleaned += buffer[0][:match.start()]
                    buffer[0] = buffer[0][match.end():]
                incomplete_think = buffer[0].find('<think>')
                if incomplete_think != -1:
                    cleaned += buffer[0][:incomplete_think]
                    buffer[0] = buffer[0][incomplete_think:]
                else:
                    cleaned += buffer[0]
                    buffer[0] = ''
                if cleaned:
                    callback(cleaned, is_done)
            cb = process_chunk
        else:
            cb = callback
        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if 'response' in data:
                        chunk = data['response']
                        full_response += chunk
                        cb(chunk, data.get('done', False))
                    if data.get('done', False):
                        cb(full_response, True)
                        break
                except json.JSONDecodeError:
                    continue
        return {"response": full_response, "done": True}

    def _extract_summary(self, data):
        """
        Extract the summary text from the model's response data.
        Removes <think>...</think> sections from the summary.

        Args:
            data (dict): The response data from the model.
        Returns:
            str: The cleaned summary text.
        """
        if 'response' in data:
            summary = data['response']
        else:
            summary = None
            for value in data.values():
                if isinstance(value, dict) and 'response' in value:
                    summary = value['response']
                    break
            if not summary and 'choices' in data and isinstance(data['choices'], list) and data['choices']:
                summary = data['choices'][0].get('message', {}).get('content', '')
            if not summary:
                summary = str(data)
        return self.remove_think_section(summary)

    def summarize(self, prompt_file, stream=False, replacements: List[Tuple[str, str]] = None, callback=None, remove_think=True):
        """
        Summarize the content of a prompt file using the locally hosted Qwen model.
        Optionally supports streaming and text replacements.

        Args:
            prompt_file (str): Path to the prompt file.
            stream (bool): Whether to use streaming response.
            replacements (List[Tuple[str, str]], optional): List of (old, new) tuples for text replacement.
            callback (callable, optional): Callback for streaming. Called with (chunk, is_done).
            remove_think (bool): Whether to remove <think>...</think> sections from the output.
        Returns:
            str: The summary text.
        """
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
        if replacements:
            for old, new in replacements:
                prompt = prompt.replace(old, new)
        data = self._post_to_model(prompt, stream=stream, callback=callback, remove_think=remove_think)
        if not stream:
            return self._extract_summary(data) if remove_think else data.get('response', str(data))
        return self._extract_summary(data)

    def summarize_from_text(self, prompt_text, stream=False, callback=None, remove_think=True):
        """
        Summarize the given prompt text using the locally hosted Qwen model.
        Optionally supports streaming and callback.

        Args:
            prompt_text (str): The text to summarize.
            stream (bool): Whether to use streaming response.
            callback (callable, optional): Callback for streaming. Called with (chunk, is_done).
            remove_think (bool): Whether to remove <think>...</think> sections from the output.
        Returns:
            str: The summary text.
        """
        data = self._post_to_model(prompt_text, stream=stream, callback=callback, remove_think=remove_think)
        if not stream:
            return self._extract_summary(data) if remove_think else data.get('response', str(data))
        return self._extract_summary(data)

    def check_ollama_and_model(self):
        """
        Checks if Ollama is running and if the Qwen model is available.
        Returns a dict with 'status' (bool) and 'message' (str).
        """
        # Check if Ollama is running
        try:
            response = requests.get(self.api_tags, timeout=2)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            msg = (f"Ollama is not running or not reachable at {self.api_url.replace('/api/generate', '')}. "
                   "Please install and start Ollama: https://ollama.com/download")
            return {"status": False, "message": msg}
        except Exception as e:
            return {"status": False, "message": f"Error connecting to Ollama: {e}"}
        # Check if Qwen model is available
        try:
            tags = response.json().get('models', [])
            if not any(self.model.lower() in tag.get('name', '').lower() for tag in tags):
                msg = f"Qwen model '{self.model}' is not available in Ollama. Run: ollama pull {self.model}"
                return {"status": False, "message": msg}
        except Exception as e:
            return {"status": False, "message": f"Error checking Qwen model: {e}"}
        return {"status": True, "message": "Ollama and Qwen model are available."}
