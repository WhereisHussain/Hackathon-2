import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from src.storage import InMemoryStorage
from src.models import TaskStatus

class CLI:
    def __init__(self):
        self.storage = InMemoryStorage()
        self.console = Console()

    def run(self):
        while True:
            self.print_menu()
            choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_complete()
            elif choice == "6":
                self.console.print("[bold blue]Goodbye![/]")
                sys.exit(0)

    def print_menu(self):
        self.console.clear() 
        menu_text = (
            "[1] Add Task\n"
            "[2] View Tasks\n"
            "[3] Update Task\n"
            "[4] Delete Task\n"
            "[5] Toggle Completion\n"
            "[6] Exit"
        )
        self.console.print(Panel(menu_text, title="Todo App", subtitle="Select an option", expand=False))

    def add_task(self):
        title = Prompt.ask("Enter title")
        if not title:
            self.console.print("[bold red]Title is required.[/]")
            return
        description = Prompt.ask("Enter description (optional)") or None
        task = self.storage.add_task(title, description)
        self.console.print(f"[green]Task '{task.title}' added with ID {task.id}.[/]")
        self.wait_for_input()

    def view_tasks(self):
        tasks = self.storage.get_all_tasks()
        if not tasks:
            self.console.print("[yellow]No tasks found.[/]")
            self.wait_for_input()
            return
        
        table = Table(title="Task List")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Status", style="magenta")
        table.add_column("Title", style="bold white")
        table.add_column("Description")
        table.add_column("Created At", style="dim")

        for task in tasks:
            status_str = "[green]Completed[/]" if task.status == TaskStatus.COMPLETED else "[red]Pending[/]"
            desc_str = task.description if task.description else ""
            created_str = task.created_at.strftime("%Y-%m-%d %H:%M")
            table.add_row(str(task.id), status_str, task.title, desc_str, created_str)

        self.console.print(table)
        self.wait_for_input()

    def update_task(self):
        task_id_str = Prompt.ask("Enter Task ID to update")
        if not task_id_str.isdigit():
            self.console.print("[red]Invalid ID.[/]")
            self.wait_for_input()
            return
        task_id = int(task_id_str)
        
        task = self.storage.get_task_by_id(task_id)
        if not task:
            self.console.print("[red]Task not found.[/]")
            self.wait_for_input()
            return

        self.console.print(f"Updating '[bold]{task.title}[/]'. Press Enter to keep current value.")
        new_title = Prompt.ask(f"New title", default=task.title)
        
        current_desc = task.description if task.description else ""
        new_desc = Prompt.ask(f"New description", default=current_desc)
        
        # In rich prompt default is returned if empty, so we just use the values
        self.storage.update_task(task_id, title=new_title, description=new_desc)
        self.console.print("[green]Task updated.[/]")
        self.wait_for_input()

    def delete_task(self):
        task_id_str = Prompt.ask("Enter Task ID to delete")
        if not task_id_str.isdigit():
            self.console.print("[red]Invalid ID.[/]")
            self.wait_for_input()
            return
        
        if Confirm.ask(f"Are you sure you want to delete task {task_id_str}?"):
            if self.storage.delete_task(int(task_id_str)):
                self.console.print("[green]Task deleted.[/]")
            else:
                self.console.print("[red]Task not found.[/]")
        else:
            self.console.print("[yellow]Deletion cancelled.[/]")
        self.wait_for_input()

    def toggle_complete(self):
        task_id_str = Prompt.ask("Enter Task ID to toggle")
        if not task_id_str.isdigit():
            self.console.print("[red]Invalid ID.[/]")
            self.wait_for_input()
            return
        task_id = int(task_id_str)
        task = self.storage.get_task_by_id(task_id)
        
        if not task:
            self.console.print("[red]Task not found.[/]")
            self.wait_for_input()
            return

        if task.status == TaskStatus.PENDING:
            self.storage.mark_complete(task_id)
            self.console.print("[green]Task marked as completed.[/]")
        else:
            self.storage.mark_incomplete(task_id)
            self.console.print("[yellow]Task marked as pending.[/]")
        self.wait_for_input()

    def wait_for_input(self):
        self.console.input("\n[dim]Press Enter to continue...[/]")
