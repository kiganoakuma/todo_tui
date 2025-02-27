import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """TODO TASK REPR"""

    id: int
    title: str
    completed: bool = False
    priority: str = "medium"  # low, medium, high, urgent
    due_date: Optional[datetime.date] = None
    category: Optional[str] = None
    notes: Optional[str] = None

    def is_overdue(self) -> bool:
        """Task over: True or False"""
        if not self.due_date:
            return False
        return self.due_date < datetime.date.today() and not self.completed

    def to_dict(self) -> dict:
        """Task to Dict Storage"""
        task_dict = {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "priority": self.priority,
            "category": self.category,
            "notes": self.notes,
        }

        if self.due_date:
            task_dict["due_date"] = self.due_date.isoformat()
        else:
            task_dict["due_date"] = None

        return task_dict

    @classmethod
    def from_dict(cls, task_dict: dict) -> "Task":
        """task obj creation from dict"""
        due_date = task_dict.get("due_date")
        if due_date:
            task_dict["due_date"] = datetime.date.fromisoformat(due_date)

        return cls(**task_dict)
