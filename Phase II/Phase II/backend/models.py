from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "user"  # Better Auth uses 'user' by default
    id: str = Field(primary_key=True)
    email: str
    name: str
    created_at: datetime
    updated_at: datetime
    
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    __tablename__ = "task"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: str = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")
