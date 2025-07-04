import os
import hashlib
import json
from datetime import datetime
import requests
from git import Repo, InvalidGitRepositoryError

class DaillyUpdateManager:
    def __init__(self, project_dir=None):
        self.PROJECT_DIR = project_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def describe_change(self, file_path):
        _, ext = os.path.splitext(file_path)
        if ext in ['.py']:
            return f"Python script: {file_path}"
        elif ext in ['.md']:
            return f"Markdown documentation: {file_path}"
        elif ext in ['.txt']:
            return f"Text file: {file_path}"
        elif ext in ['.json']:
            return f"JSON data/config: {file_path}"
        else:
            return f"File: {file_path}"

    def get_git_status(self, base_dir):
        try:
            repo = Repo(base_dir)
            added, modified, removed = [], [], []
            for path in repo.untracked_files:
                added.append(path)
            for item in repo.index.diff(None):
                if item.change_type == 'M':
                    modified.append(item.a_path)
                elif item.change_type == 'D':
                    removed.append(item.a_path)
            for item in repo.index.diff('HEAD'):
                if item.change_type == 'A' and item.a_path not in added:
                    added.append(item.a_path)
                elif item.change_type == 'M' and item.a_path not in modified:
                    modified.append(item.a_path)
                elif item.change_type == 'D' and item.a_path not in removed:
                    removed.append(item.a_path)
            return added, modified, removed
        except (InvalidGitRepositoryError, Exception) as e:
            print(f"Error in get_git_status: {e}")
            return None

    def print_git_status_result(self, git_result):
        added, modified, removed = git_result
        if not (added or removed or modified):
            print("No changes detected (git).")
        else:
            print("Changes detected (git):")
            for f in added:
                print(f"[ADDED] {self.describe_change(f)}")
            for f in removed:
                print(f"[REMOVED] {self.describe_change(f)}")
            for f in modified:
                print(f"[MODIFIED] {self.describe_change(f)}")
        print(f"Scan complete at {datetime.now().isoformat()}")

    def get_code_change_list(self, git_result):
        added, modified, removed = git_result
        changes = []
        for f in added:
            changes.append({"type": "ADDED", "file": f, "description": self.describe_change(f)})
        for f in removed:
            changes.append({"type": "REMOVED", "file": f, "description": self.describe_change(f)})
        for f in modified:
            changes.append({"type": "MODIFIED", "file": f, "description": self.describe_change(f)})
        return changes

    def get_file_modifications(self, base_dir, modified_files):
        repo = Repo(base_dir)
        diffs = {}
        for file_path in modified_files:
            try:
                diff_text = repo.git.diff(file_path)
                diffs[file_path] = diff_text
            except Exception as e:
                diffs[file_path] = f"Error getting diff: {e}"
        return diffs

    def summarize_code_changes(self, prompt, code_changes, diffs=None):
        summary = []
        for change in code_changes:
            line = f"{change['type']}: {change['file']} - {change['description']}"
            if diffs and change['type'] == 'MODIFIED' and change['file'] in diffs:
                diff = diffs[change['file']]
                line += f" (Modified lines: {len(diff.splitlines())})"
            summary.append(line)
        return summary

    def call_local_llm_api(self, prompt, code_changes, diffs=None):
        url = "http://localhost:1234/v1/chat/completions"
        system_message = (
            "Summarize my work today in a fun, creative daily update format with emojis and sections like Completed, In Progress, Retried, Improvements, and Issues. "
            "Respond in plain text only. Do not use Markdown formatting, bullet points, or bold text."
        )
        user_content = "\n".join([
            f"{c['type']}: {c['file']} - {c['description']}" + (f"\nDiff:\n{diffs[c['file']]}" if diffs and c['type'] == 'MODIFIED' and c['file'] in diffs else "")
            for c in code_changes
        ])
        payload = {
            "model": "meta-llama-3.1-8b-instruct",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": -1,
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=300)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"Error calling local LLM API: {e}"

    def main(self, project_dir=None, summarize_prompt=None, use_llm_api=True):
        if project_dir is None:
            project_dir = self.PROJECT_DIR
        print(f"Scanning project directory: {project_dir}")
        git_dir = os.path.join(project_dir, '.git')
        if os.path.exists(git_dir):
            git_result = self.get_git_status(project_dir)
            if git_result is not None:
                code_changes = self.get_code_change_list(git_result)
                self.print_git_status_result(git_result)
                modified_files = [c['file'] for c in code_changes if c['type'] == 'MODIFIED']
                diffs = self.get_file_modifications(project_dir, modified_files) if modified_files else None
                if modified_files and diffs:
                    for file, diff in diffs.items():
                        print(f"\nDiff for {file}:\n{diff}")
                if use_llm_api:
                    print("\nSummary from local LLM API:")
                    summary = self.call_local_llm_api(summarize_prompt, code_changes, diffs)
                    print(summary)
                elif summarize_prompt:
                    summary = self.summarize_code_changes(summarize_prompt, code_changes, diffs)
                    print("\nSummary of key accomplishments and features implemented:")
                    for line in summary:
                        print(f"- {line}")
                return
        else:
            print("Not a git directory. Exiting.")
            return

# For backward compatibility
DaillyUpdateManagerInstance = DaillyUpdateManager()
def get_git_status(base_dir):
    return DaillyUpdateManagerInstance.get_git_status(base_dir)
def main(project_dir=None, summarize_prompt=None, use_llm_api=True):
    return DaillyUpdateManagerInstance.main(project_dir, summarize_prompt, use_llm_api)
