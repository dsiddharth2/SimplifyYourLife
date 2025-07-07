import unittest
import os
import sys
sysPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, sysPath)
from src.tools.extract_paths import ExtractPathsTool

class TestExtractPaths(unittest.TestCase):

    def test_extract_paths_with_llm(self):
        # Patch QwenSummarizer to return a fixed result
        extractPathsTool = ExtractPathsTool()
        text = "My Code is in the following path : C:\\2_WorkSpace\\BluB0X\\BBX_AI and also /home/user/project."
        paths = extractPathsTool.extract_paths_with_llm(text)
        self.assertIn("C:\\2_WorkSpace\\BluB0X\\BBX_AI", paths)
        self.assertIn("/home/user/project", paths)
        self.assertEqual(len(paths), 2)

    def test_extract_paths(self):
        extractPathsTool = ExtractPathsTool()
        text = "My Code is in the following path : C:\\2_WorkSpace\\BluB0X\\BBX_AI and also /home/user/project."
        paths = extractPathsTool.extract_paths(text)
        self.assertIn("C:\\2_WorkSpace\\BluB0X\\BBX_AI", paths)
        self.assertIn("/home/user/project", paths)
        self.assertEqual(len(paths), 2)

if __name__ == "__main__":
    unittest.main()
