import os
from datetime import datetime
from git import Repo, InvalidGitRepositoryError, GitCommandError
from typing import List

class GitTools:
    def __init__(self, project_dirs: List[str], mark_as_safe: bool = False):
        # Accept a list of project directories
        if isinstance(project_dirs, str):
            project_dirs = [project_dirs]
        if not isinstance(project_dirs, list):
            raise TypeError("project_dirs must be a list of directory paths (str)")
        self.project_dirs = project_dirs
        self.repos = self.get_git_repos()
        if mark_as_safe:
            for repo, dir_path in zip(self.repos, self.project_dirs):
                if repo:
                    self._mark_as_safe(repo, dir_path)

    def _mark_as_safe(self, repo, dir_path):
        """
        Marks the project directory as a safe directory for git operations.
        This is necessary to avoid issues with git commands in certain environments.
        """
        try:
            repo.git.config('--global', '--add', 'safe.directory', dir_path)
            print(f"Marked '{dir_path}' as a safe directory for git operations.")
        except GitCommandError as e:
            print(f"Error marking directory as safe: {e}")

    def get_git_repos(self):
        repos = []
        for dir_path in self.project_dirs:
            git_dir = os.path.join(dir_path, '.git')
            if not os.path.exists(git_dir):
                print(f"Directory '{dir_path}' is not a git repository.")
                continue
            try:
                repos.append(Repo(dir_path))
            except InvalidGitRepositoryError:
                print(f"Invalid git repository: {dir_path}")
                repos.append(None)
        return repos

    def get_current_changes(self, with_diffs=False):
        """
        Returns a dict with lists of added, modified, and removed files in the working directory for all project dirs.
        If with_diffs is True, also returns the diffs for modified files.
        """
        results = []
        for repo, dir_path in zip(self.repos, self.project_dirs):
            if not repo:
                print(f"No git repository found for {dir_path}.")
                results.append(None)
                continue
            added, modified, removed = [], [], []
            diffs = {}
            try:
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
                if with_diffs:
                    for file_path in modified:
                        try:
                            diff_text = repo.git.diff(file_path)
                            diffs[file_path] = diff_text
                        except Exception as e:
                            diffs[file_path] = f"Error getting diff: {e}"
                result = {
                    "project_dir": dir_path,
                    "added": added,
                    "modified": modified,
                    "removed": removed
                }
                if with_diffs:
                    result["diffs"] = diffs
                results.append(result)
            except GitCommandError as e:
                print(f"Git error in {dir_path}: {e}")
                results.append(None)
        return results

    def get_changes_since_date(self, since_date, with_diffs=False, with_commit_messages=False, author=None):
        """
        Returns a dict with a list of files changed in commits since the given date (YYYY-MM-DD),
        optionally their diffs, and optionally the commit messages. If author is specified, includes commits where the author's name or email contains the substring (case-insensitive).
        Runs for all project dirs.
        """
        results = []
        for repo, dir_path in zip(self.repos, self.project_dirs):
            if not repo:
                print(f"No git repository found for {dir_path}.")
                results.append(None)
                continue
            try:
                since = datetime.strptime(since_date, "%Y-%m-%d")
            except ValueError:
                print("Date format should be YYYY-MM-DD")
                results.append(None)
                continue
            changed_files = set()
            diffs = {}
            commit_messages = []
            try:
                for commit in repo.iter_commits(since=since_date):
                    commit_date = datetime.fromtimestamp(commit.committed_date)
                    # Author filtering: substring match (case-insensitive) on name or email
                    if author:
                        author_lower = author.lower()
                        commit_author_name = commit.author.name.lower() if commit.author.name else ''
                        commit_author_email = commit.author.email.lower() if commit.author.email else ''
                        if author_lower not in commit_author_name and author_lower not in commit_author_email:
                            continue
                    if commit_date >= since:
                        commit_messages.append({
                            "commit": commit.hexsha,
                            "author": commit.author.name,
                            "date": commit_date.isoformat(),
                            "message": commit.message.strip()
                        })
                        for file in commit.stats.files.keys():
                            changed_files.add(file)
                            if with_diffs:
                                try:
                                    diff_text = commit.diff(commit.parents[0] if commit.parents else None, paths=file, create_patch=True)
                                    if diff_text:
                                        diffs[file] = '\n'.join([d.diff.decode('utf-8', errors='ignore') if hasattr(d.diff, 'decode') else str(d.diff) for d in diff_text])
                                    else:
                                        diffs[file] = ''
                                except Exception as e:
                                    diffs[file] = f"Error getting diff: {e}"
                result = {"project_dir": dir_path, "changed_files": list(changed_files)}
                if with_diffs:
                    result["diffs"] = diffs
                if with_commit_messages:
                    result["commit_messages"] = commit_messages
                results.append(result)
            except Exception as e:
                print(f"Error reading commits in {dir_path}: {e}")
                results.append(None)
        return results
