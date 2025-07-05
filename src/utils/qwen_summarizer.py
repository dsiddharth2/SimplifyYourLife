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

    def _post_to_model(self, prompt, stream=False):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()

    def _extract_summary(self, data):
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

    def summarize(self, prompt_file, stream=False, replacements: List[Tuple[str, str]] = None):
        """
        Summarize the content of a prompt file using the locally hosted Qwen model.
        """
        with open(prompt_file, 'r', encoding='utf-8') as f:
            prompt = f.read()
        if replacements:
            for old, new in replacements:
                prompt = prompt.replace(old, new)
        data = self._post_to_model(prompt, stream=stream)
        return self._extract_summary(data)

    def summarize_from_text(self, prompt_text, stream=False):
        """
        Summarize the given prompt text using the locally hosted Qwen model.
        """
        data = self._post_to_model(prompt_text, stream=stream)
        return self._extract_summary(data)
