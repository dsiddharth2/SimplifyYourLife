# Tools Module (`src/tools`)

This module provides utility classes for interacting with git and other tools.

## Files

- `git_tools.py`: Contains the `GitTools` class for interacting with git repositories.
  - Methods:
    - `get_current_changes(with_diffs=False)`: Returns added, modified, and removed files in the working directory, with optional diffs.
    - `get_changes_since_date(since_date, with_diffs=False, with_commit_messages=False, author=None)`: Returns files changed in commits since a given date, with optional diffs and commit messages. Supports filtering by author (substring match).

## Usage

Import and instantiate `GitTools` with the project directory. Use its methods to retrieve git status and history.

[Back to Main Docs](README.md)
