# release/ Folder

The `release/` folder at the root of the project is dedicated to deployment, packaging, and build scripts. It is **not** a release or distribution folder itself, but rather a workspace for all files and scripts needed to create a release build of the application.

## What goes in `release/`?
- PyInstaller spec files (e.g., `app.spec`)
- Custom PyInstaller hooks (e.g., `hooks/`)
- Runtime hooks (e.g., `runtime_hook.py`)
- Any batch scripts, shell scripts, or configuration files used for packaging or deployment

## Why use a `release/` folder?
- Keeps deployment and build logic separate from application source code (`src/`)
- Makes it easy to find and update packaging scripts
- Supports clean collaboration between developers and release managers

## How to use
- To build the app, run PyInstaller with the spec file in this folder:
  ```powershell
  pyinstaller release/app.spec
  ```
  Note that you should be in the folder where app.py exists
- Update any paths in the spec file to be relative to the `release/` folder as needed.