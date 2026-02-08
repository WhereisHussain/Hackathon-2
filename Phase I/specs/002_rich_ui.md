# Spec 002: Rich UI Upgrade

## Goal
Enhance the CLI experience using the `rich` library.

## Rationale
The current plain text output is functional but unengaging. `rich` provides beautiful formatting, tables, and colors.

## Features
### 1. Main Menu
- Use a `rich.table.Table` or `console.print` with style for the menu.
- Clear screen between actions (optional/if possible across platforms).

### 2. Task List
- Display tasks in a **Rich Table**.
- Columns: ID, Status (Color coded: Green check/Red X), Title, Description, Created At.
- Striped rows for readability.

### 3. Feedback
- Use `console.print("[green]Success...[/]")` for success messages.
- Use `console.print("[red]Error...[/]")` for errors.

### 4. Input
- Use `rich.prompt.Prompt` for inputs (e.g. `Prompt.ask("Enter title")`).

## Technical Changes
- Import `rich.console.Console`, `rich.table.Table`.
- Initialize a global `console` object.
- specific changes in `src/cli.py`.
