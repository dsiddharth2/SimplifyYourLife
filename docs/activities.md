# Activities Module (`src/activities`)

This module contains activity logic, such as daily update automation.

## Files

- `daily_update_activity.py`: Implements the `DaillyUpdateActivity` class.
  - Methods:
    - `run(since_date=None)`: Generates a daily update summary since a specific date, using git history and file changes.

## Usage

Instantiate `DaillyUpdateActivity` and call `run()` to generate a daily update summary.

[Back to Main Docs](README.md)
