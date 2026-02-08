# Spec 001: Basic Todo App Features

## Goal
Create a basic in-memory console-based Todo application.

## Features

### 1. Data Structure
- **Task Object**:
  - `id`: Unique Integer/UUID (auto-increment or UUID).
  - `title`: String (required).
  - `description`: String (optional).
  - `status`: Enum (Pending, Completed).
  - `created_at`: Datetime.

### 2. Storage
- In-memory list or dictionary.
- Data is lost when app exits.

### 3. CLI Interface
- **Main Menu**:
  1. Add Task
  2. View Tasks
  3. Update Task
  4. Delete Task
  5. Mark Complete
  6. Exit

### 4. Operations
- **Add**: Prompt for title, description.
- **View**: List all tasks with ID, Status [ ]/[x], Title.
- **Update**: Ask for ID, then prompt for new title/desc. Keep old if empty.
- **Delete**: Ask for ID, remove from list.
- **Mark Complete**: Ask for ID, toggle status to Completed.

## Technical Constraints
- Use `src/` directory.
- Use `main.py` as entry point.
- Clean separation of CLI and Logic (MVC pattern preferred or Service layer).
