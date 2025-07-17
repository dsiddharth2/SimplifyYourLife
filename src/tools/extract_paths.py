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

    def extract_paths_and_summary_with_llm(self, text: str) -> dict:
        """
        Uses the extract_paths_and_activity prompt to extract both file/directory paths 
        and work summary from a daily update text.
        Returns a dictionary with 'project_paths' (list) and 'work_summary' (str).
        """
        import os
        
        # Get the path to the extract_paths_and_activity prompt
        prompt_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '../prompts/extract_paths_and_activity.txt'
        ))
        
        # Prepare replacements for the prompt
        replacements = [("{daily_update_context}", text)]
        
        try:
            # Call the Qwen LLM using the specific prompt file
            result = self.qwen.summarize(prompt_file, replacements=replacements)
            
            # Try to parse the result as JSON
            import json
            try:
                parsed_result = json.loads(result)
                
                # Validate the expected structure
                if isinstance(parsed_result, dict) and \
                   "project_paths" in parsed_result and \
                   "work_summary" in parsed_result:
                    return parsed_result
                else:
                    return {"project_paths": [], "work_summary": "Failed to parse response structure"}
                    
            except json.JSONDecodeError:
                return {"project_paths": [], "work_summary": f"Failed to parse JSON: {result}"}
                
        except Exception as e:
            return {"project_paths": [], "work_summary": f"Error calling LLM: {str(e)}"}
