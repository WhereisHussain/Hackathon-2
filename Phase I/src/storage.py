from typing import List, Optional, Dict
from datetime import datetime
from src.models import Task, TaskStatus

class InMemoryStorage:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
            
        return task

    def delete_task(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = TaskStatus.COMPLETED
        return task

    def mark_incomplete(self, task_id: int) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        task.status = TaskStatus.PENDING
        return task
