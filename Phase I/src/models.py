from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional

class TaskStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime
