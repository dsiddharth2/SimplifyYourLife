import os
import hashlib
import json
from datetime import datetime
from git import Repo, InvalidGitRepositoryError
import requests

# Directory to monitor (relative to this script)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATE_FILE = os.path.join(os.path.dirname(__file__), '.file_state.json')

def get_file_hash(filepath):
    """Return the SHA256 hash of a file's contents."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def scan_files(base_dir):
    """Scan all files in the directory recursively and return a dict of {relpath: hash}."""
    file_hashes = {}
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.startswith('.') or file == os.path.basename(__file__):
                continue  # Skip hidden and this script
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, base_dir)
            try:
                file_hashes[relpath] = get_file_hash(filepath)
            except Exception as e:
                print(f"Could not hash {relpath}: {e}")
    return file_hashes

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def describe_change(file_path):
    """Try to describe what a file does based on its name and extension."""
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

def get_git_status(base_dir):
    """Return lists of added, modified, and removed files using GitPython."""
    try:
        repo = Repo(base_dir)
        added, modified, removed = [], [], []
        # Untracked files
        for path in repo.untracked_files:
            added.append(path)
        # Changed files (staged and unstaged)
        for item in repo.index.diff(None):  # Working tree diff
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

def print_git_status_result(git_result):
    added, modified, removed = git_result
    if not (added or removed or modified):
        print("No changes detected (git).")
    else:
        print("Changes detected (git):")
        for f in added:
            print(f"[ADDED] {describe_change(f)}")
        for f in removed:
            print(f"[REMOVED] {describe_change(f)}")
        for f in modified:
            print(f"[MODIFIED] {describe_change(f)}")
    print(f"Scan complete at {datetime.now().isoformat()}")

def get_code_change_list(git_result):
    """Return a list of dictionaries describing each code change from git_result."""
    added, modified, removed = git_result
    changes = []
    for f in added:
        changes.append({"type": "ADDED", "file": f, "description": describe_change(f)})
    for f in removed:
        changes.append({"type": "REMOVED", "file": f, "description": describe_change(f)})
    for f in modified:
        changes.append({"type": "MODIFIED", "file": f, "description": describe_change(f)})
    return changes

def get_file_modifications(base_dir, modified_files):
    """Return a dict mapping each modified file to its git diff as a string."""
    repo = Repo(base_dir)
    diffs = {}
    for file_path in modified_files:
        try:
            diff_text = repo.git.diff(file_path)
            diffs[file_path] = diff_text
        except Exception as e:
            diffs[file_path] = f"Error getting diff: {e}"
    return diffs

def summarize_code_changes(prompt, code_changes, diffs=None):
    """
    Given a prompt, a list of code changes (from get_code_change_list), and optional diffs,
    return a summary of key accomplishments and features implemented.
    This is a placeholder for AI integration; currently, it generates a simple summary.
    """
    summary = []
    for change in code_changes:
        line = f"{change['type']}: {change['file']} - {change['description']}"
        if diffs and change['type'] == 'MODIFIED' and change['file'] in diffs:
            diff = diffs[change['file']]
            # Optionally, include a snippet of the diff or a note
            line += f" (Modified lines: {len(diff.splitlines())})"
        summary.append(line)
    # In a real AI model, you would send prompt + code_changes (+diffs) to an LLM here
    return summary

def call_local_llm_api(prompt, code_changes, diffs=None):
    """Call a local LLM API to summarize code changes, requesting a fun daily update with emojis and sections."""
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
        response = requests.post(url, json=payload, headers=headers, timeout=300)  # 5 minutes
        response.raise_for_status()
        data = response.json()
        # Extract the model's reply
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error calling local LLM API: {e}"

def main(project_dir=None, summarize_prompt=None, use_llm_api=True):
    if project_dir is None:
        project_dir = PROJECT_DIR
    print(f"Scanning project directory: {project_dir}")
    # Check if .git exists
    git_dir = os.path.join(project_dir, '.git')
    if os.path.exists(git_dir):
        git_result = get_git_status(project_dir)
        if git_result is not None:
            code_changes = get_code_change_list(git_result)
            print_git_status_result(git_result)
            modified_files = [c['file'] for c in code_changes if c['type'] == 'MODIFIED']
            diffs = get_file_modifications(project_dir, modified_files) if modified_files else None
            if modified_files and diffs:
                for file, diff in diffs.items():
                    print(f"\nDiff for {file}:\n{diff}")
            if use_llm_api:
                print("\nSummary from local LLM API:")
                summary = call_local_llm_api(summarize_prompt, code_changes, diffs)
                print(summary)
            elif summarize_prompt:
                summary = summarize_code_changes(summarize_prompt, code_changes, diffs)
                print("\nSummary of key accomplishments and features implemented:")
                for line in summary:
                    print(f"- {line}")
            return
    
    # Fallback to old method if not a git repo
    prev_state = load_state()
    curr_state = scan_files(project_dir)
    added = [f for f in curr_state if f not in prev_state]
    removed = [f for f in prev_state if f not in curr_state]
    modified = [f for f in curr_state if f in prev_state and curr_state[f] != prev_state[f]]
    if not (added or removed or modified):
        print("No changes detected.")
    else:
        print("Changes detected:")
        for f in added:
            print(f"[ADDED] {describe_change(f)}")
        for f in removed:
            print(f"[REMOVED] {describe_change(f)}")
        for f in modified:
            print(f"[MODIFIED] {describe_change(f)}")
    save_state(curr_state)
    print(f"Scan complete at {datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
