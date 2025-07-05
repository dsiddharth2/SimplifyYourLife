import os
import datetime
from src.tools.git_tools import GitTools
from src.utils.qwen_summarizer import QwenSummarizer

class DaillyUpdateActivity:
    def __init__(self, project_dir=None):
        self.project_dir = project_dir
        self.git_tools = GitTools(self.project_dir)
        self.summarizer = QwenSummarizer()
        self.tasks = []

    def run(self, since_date=None):
        # 1. Get commit history and current file changes
        if since_date is None:
            since_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        commit_info = self.git_tools.get_changes_since_date(since_date, with_commit_messages=True, author='Sid')
        current_changes = self.git_tools.get_current_changes(with_diffs=True)
        
        # 2. Summarize per file
        summaries = []
        today = datetime.date.today().strftime("%A, %d %B %Y")
        status = f"🗓️ Daily Status for {today}"
        status += "✅ Tasks for Today:"

        # For each changed file, get a summary
        if current_changes and 'modified' in current_changes:
            for file in current_changes['modified']:
                file_diff = current_changes['diffs'].get(file, '') if 'diffs' in current_changes else ''
                replacements = [("{file_name}", file), ("{file_modifications}", file_diff)]
                summary = self.summarizer.summarize(
                    os.path.join(os.path.dirname(__file__), '../prompts/summarize_file_changes.txt'),
                    replacements=replacements
                )
                summaries.append(f"Summary for {file}:\n{summary}")
        # Optionally, print commit messages
        commit_summaries = []
        if commit_info and 'commit_messages' in commit_info:
            for c in commit_info['commit_messages']:
                commit_summaries.append(f"- {c['date']} {c['author']}: {c['message']}")
        # Combine all summaries and commits into one context for Qwen
        daily_update_context = status
        if summaries:
            daily_update_context += "\n📝 File Summaries:\n" + "\n".join(summaries)
        if commit_summaries:
            daily_update_context += "\n\n🔨 Recent Commits:\n" + "\n".join(commit_summaries)
        # Use the summarize_daily_update.txt prompt
        prompt_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../prompts/summarize_daily_update.txt'))
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
        prompt = prompt_template.replace('{daily_update_context}', daily_update_context)
        final_summary = self.summarizer.summarize_from_text(prompt)
        print("\n===== Consolidated Daily Update =====\n")
        print(final_summary)
