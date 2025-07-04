import requests
import json
import re
from typing import List, Tuple

class QwenSummarizer:
    def __init__(self, host="http://localhost:11434", model="qwen3"):
        self.api_url = f"{host}/api/generate"
        self.model = model

    def remove_think_section(self, text):
        return re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)

    def summarize(self, prompt_file, stream=False, replacements: List[Tuple[str, str]] = None):
        """
        Summarize the content of a prompt file using the locally hosted Qwen model.
        Args:
            prompt_file (str): Path to the file containing the prompt.
            stream (bool): Whether to use streaming mode.
            replacements (List[Tuple[str, str]]): List of (old, new) string replacements to apply to the prompt before summarizing.
        Returns:
            str: The summary response from the model.
        """
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
        if replacements:
            for old, new in replacements:
                prompt = prompt.replace(old, new)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        data = response.json()
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
