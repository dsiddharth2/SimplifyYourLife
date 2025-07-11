import os
import datetime
from src.tools.git_tools import GitTools
from src.utils.qwen_summarizer import QwenSummarizer

class DaillyUpdateActivity:
    def __init__(self, project_dirs=None):
        if project_dirs is None:
            project_dirs = []
        self.project_dirs = project_dirs
        self.git_tools = GitTools(self.project_dirs)
        self.summarizer = QwenSummarizer()
        self.tasks = []

    def run(self, since_date=None, check_for_current_changes = False, stream=False, callback=None):
        # 1. Get commit history and current file changes
        if since_date is None:
            since_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        commit_info = self.git_tools.get_changes_since_date(since_date, with_commit_messages=True, author='Sid')

        # 2. Summarize per file
        summaries = []
        today = datetime.date.today().strftime("%A, %d %B %Y")
        status = f"🗓️ Daily Status for {today}"
        status += "✅ Tasks for Today:"

        # For each changed file, collect all diffs and ask the model at once
        if check_for_current_changes:
            current_changes_list = self.git_tools.get_current_changes(with_diffs=True)
            all_file_summaries = []
            if current_changes_list:
                for current_changes in current_changes_list:
                    if current_changes and 'modified' in current_changes:
                        for file in current_changes['modified']:
                            file_diff = current_changes.get('diffs', {}).get(file, '')
                            all_file_summaries.append(f"Project: {current_changes['project_dir']}\nFile: {file}\nDiff:\n{file_diff}")
            if all_file_summaries:
                combined_diff_context = "\n\n".join(all_file_summaries)
                replacements = [("{file_changes_context}", combined_diff_context)]
                summary = self.summarizer.summarize(
                    os.path.join(os.path.dirname(__file__), '../prompts/summarize_file_changes.txt'),
                    replacements=replacements
                )
                summaries.append(f"Summary of all file changes:\n{summary}")
        #end if

        commit_summaries = []
        if commit_info:
            for project_commit_info in commit_info:
                if project_commit_info and 'commit_messages' in project_commit_info:
                    project_dir = project_commit_info.get('project_dir', '')
                    for c in project_commit_info['commit_messages']:
                        commit_summaries.append(f"Project: {project_dir} - {c['date']} {c['author']}: {c['message']}")
        
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
        final_summary = self.summarizer.summarize_from_text(prompt, stream=stream, callback=callback, remove_think=True)
        return final_summary
