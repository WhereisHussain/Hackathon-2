from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from db import get_session
from models import Task
from auth import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
def read_tasks(
    status: Optional[str] = Query(None, pattern="^(all|pending|completed)$"),
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    query = select(Task).where(Task.user_id == user_id)
    
    if status == "pending":
        query = query.where(Task.completed == False)
    elif status == "completed":
        query = query.where(Task.completed == True)
        
    tasks = session.exec(query).all()
    return tasks

@router.post("/", response_model=Task)
def create_task(
    task: Task,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=Task)
def read_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task

@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_update: Task,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.patch("/{task_id}/complete", response_model=Task)
def complete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
        
    task.completed = not task.completed
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        
    session.delete(task)
    session.commit()
    return {"ok": True}
