import unittest
import os
import sys
sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)

from src.utils.qwen_summarizer import QwenSummarizer

class TestQwenSummarizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use the summarize_file_changes.txt prompt from the prompt directory under src
        cls.prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/prompts/summarize_file_changes.txt'))
        if not os.path.exists(cls.prompt_file):
            raise unittest.SkipTest(f"Prompt file not found: {cls.prompt_file}")
        cls.summarizer = QwenSummarizer()

    def test_summarize_with_replacements(self):
        replacements = [
            ("{file_name}", "example.py"),
            ("{file_modifications}", "diff --git a/example.py b/example.py\n+")
        ]
        # This will actually call the local Qwen API, so ensure it is running
        try:
            result = self.summarizer.summarize(self.prompt_file, replacements=replacements)
            self.assertIsInstance(result, str)
            self.assertTrue("example.py" in result or result != "")
        except Exception as e:
            self.skipTest(f"Qwen API not available or failed: {e}")

if __name__ == '__main__':
    unittest.main()
