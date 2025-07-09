# Tools Module (`src/tools`)

This module provides utility classes for interacting with git and other tools.

## Files

- `git_tools.py`: Contains the `GitTools` class for interacting with one or more git repositories.
  - The class now accepts a list of project directories (`project_dirs: List[str]`) and operates on all of them.
  - Methods:
    - `get_current_changes(with_diffs=False)`: Returns a list of dicts, each containing added, modified, and removed files in the working directory for each project directory, with optional diffs.
    - `get_changes_since_date(since_date, with_diffs=False, with_commit_messages=False, author=None)`: Returns a list of dicts, each with files changed in commits since a given date for each project directory, with optional diffs and commit messages. Supports filtering by author (substring match).

## Usage

Import and instantiate `GitTools` with a list of project directories. Use its methods to retrieve git status and history for all specified repositories.

Example:

```python
from src.tools.git_tools import GitTools
repos = ["/path/to/repo1", "/path/to/repo2"]
gt = GitTools(repos)
changes = gt.get_current_changes()
```

[Back to Main Docs](README.md)
