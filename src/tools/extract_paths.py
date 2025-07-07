import re
from typing import List
from src.utils.qwen_summarizer import QwenSummarizer  # Adjust import if needed

class ExtractPathsTool:
    def __init__(self):
        self.qwen = QwenSummarizer()

    def extract_paths(self, text: str) -> List[str]:
        """
        Extracts all Windows and Unix file/directory paths from a natural language string.
        Returns a list of unique paths found.
        """
        # Windows paths: e.g. C:\folder\subfolder or D:/folder/file.txt
        win_path_pattern = r"[A-Za-z]:\\(?:[^\s\/:*?\"<>|\r\n]+\\?)*|[A-Za-z]:/(?:[^\s/:*?\"<>|\r\n]+/?)*"
        # Unix paths: e.g. /home/user/project
        unix_path_pattern = r"/(?:[^\s/:*?\"<>|\r\n]+/?)+"
        
        win_paths = re.findall(win_path_pattern, text)
        unix_paths = re.findall(unix_path_pattern, text)
        # Remove duplicates and sort
        all_paths = list(set(win_paths + unix_paths))
        return all_paths

    def extract_paths_with_llm(self, text: str) -> list:
        """
        Uses Qwen LLM to extract file/directory paths from a natural language string.
        Returns a list of unique paths found, as interpreted by the LLM.
        """
        prompt = (
            "Extract all file and directory paths from the following text. "
            "Return only the paths as a Python list.\nText: " + text
        )
        # Call the Qwen LLM using summarize_from_text from QwenSummarizer
        result = self.qwen.summarize_from_text(prompt)
        # Try to safely evaluate the result as a list
        try:
            import ast
            paths = ast.literal_eval(result)
            if isinstance(paths, list):
                return paths
            else:
                return []
        except Exception:
            return []

if __name__ == "__main__":
    # Example usage
    tool = ExtractPathsTool()
    example = "My Code is in the following path : C:\\2_WorkSpace\\BluB0X\\BBX_AI and also /home/user/project. Can you summarize this for me?"
    print(tool.extract_paths(example))
