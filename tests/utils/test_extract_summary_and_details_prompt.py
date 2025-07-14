import unittest
import os
import sys
sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)

from src.utils.qwen_summarizer import QwenSummarizer

class TestExtractSummaryAndDetailsPrompt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prompt_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/prompts/extract_summary_and_details.txt'))
        if not os.path.exists(cls.prompt_file):
            raise unittest.SkipTest(f"Prompt file not found: {cls.prompt_file}")
        cls.summarizer = QwenSummarizer()

    def test_extract_summary_and_details(self):
        sample_text = (
            "Following is my tasks, Attended meeting with the team to discuss project requirements. Also take update from the following paths:\n C:\\2_WorkSpace\\BluB0X\\BBX_AI"
        )
        with open(self.prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = prompt.replace("{Paste your text here}", sample_text)
        result = self.summarizer.summarize_from_text(prompt)
        self.assertIsInstance(result, str)
        self.assertTrue(result.strip(), "The summarizer response should be non-empty text.")
        
if __name__ == "__main__":
    unittest.main()
