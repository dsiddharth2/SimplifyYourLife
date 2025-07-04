# DaillyUpdate

This project provides utilities for managing and tracking updates in a codebase, with a focus on Git repositories. It includes Python scripts and tests for automating the process of checking the status of files (added, modified, removed) in a specified directory and performing update-related operations.

## Structure
- `create_update.py`: Main script containing functions to get Git status and perform update operations.
- `requirements.txt`: Lists required Python packages (such as `gitpython`).
- `tests/`: Contains unit tests for the main script, including tests for Git status and main update logic.

## Usage
- The main functions can be imported and used in other Python scripts.
- Unit tests can be run using `python -m unittest discover tests` from the `DaillyUpdate` directory.

## Requirements
- Python 3.x
- GitPython (`pip install gitpython`)

## Example
The test suite demonstrates how to use the main functions to check the status of a Git repository and perform update operations on a specified directory.

---
**Note:** The test cases assume the presence of a valid Git repository at the specified test directory. Adjust the test directory path as needed for your environment.
