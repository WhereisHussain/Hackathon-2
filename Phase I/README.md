# Todo Console App

A basic in-memory console-based Todo application built with Python.

## Prerequisites
- Python 3.13+
- `uv` (optional, for dependency management)

## Setup
1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd e:\Python\todo-console-app
   ```
3. Install dependencies (if using uv):
   ```bash
   uv sync
   ```

## How to Run

### Method 1: Python Module (Recommended)
Run the application as a module from the project root:
```bash
python -m src.main
```

### Method 2: UV
If you have `uv` installed and configured:
```bash
uv run src/main.py
```

## Features
- Add Task
- View Tasks
- Update Task
- Delete Task
- Mark Task as Complete/Incomplete
