import mcp.server.fastapi
from mcp.types import Tool, TextContent
from typing import Annotated, Optional
import json
from .models import Task
from .database import engine
from sqlmodel import Session, select
from uuid import UUID

app = mcp.server.fastapi.Context()

@app.tool()
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None
) -> str:
    """Create a new task."""
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": str(task.id),
            "status": "created",
            "title": task.title
        })

@app.tool()
async def list_tasks(
    user_id: str,
    status: str = "all"
) -> str:
    """Retrieve tasks from the list. status can be 'all', 'pending', or 'completed'."""
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        
        results = session.exec(statement).all()
        tasks = [
            {"id": str(t.id), "title": t.title, "completed": t.completed}
            for t in results
        ]
        return json.dumps(tasks)

@app.tool()
async def complete_task(
    user_id: str,
    task_id: str
) -> str:
    """Mark a task as complete."""
    with Session(engine) as session:
        task = session.get(Task, UUID(task_id))
        if not task or task.user_id != user_id:
            return json.dumps({"error": "Task not found"})
        
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": str(task.id),
            "status": "completed",
            "title": task.title
        })

@app.tool()
async def delete_task(
    user_id: str,
    task_id: str
) -> str:
    """Remove a task from the list."""
    with Session(engine) as session:
        task = session.get(Task, UUID(task_id))
        if not task or task.user_id != user_id:
            return json.dumps({"error": "Task not found"})
        
        session.delete(task)
        session.commit()
        return json.dumps({
            "task_id": task_id,
            "status": "deleted",
            "title": task.title
        })

@app.tool()
async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> str:
    """Modify task title or description."""
    with Session(engine) as session:
        task = session.get(Task, UUID(task_id))
        if not task or task.user_id != user_id:
            return json.dumps({"error": "Task not found"})
        
        if title:
            task.title = title
        if description:
            task.description = description
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return json.dumps({
            "task_id": str(task.id),
            "status": "updated",
            "title": task.title
        })
