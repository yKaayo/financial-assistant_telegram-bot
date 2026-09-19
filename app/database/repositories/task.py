from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Task


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, user_id: int, title: str, description: str, status: str) -> Task:
        task = Task(user_id=user_id, title=title, description=description, status=status)
        self.session.add(task)
        self.session.flush()
        return task

    def list_by_user(self, user_id: int, offset: int = 0, limit: int = 5) -> list[Task]:
        stmt = select(Task).where(Task.user_id == user_id).order_by(Task.id.asc()).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def count_by_user(self, user_id: int) -> int:
        return len(self.list_by_user(user_id=user_id, offset=0, limit=10_000))

    def get_user_task(self, user_id: int, task_id: int) -> Task | None:
        stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self.session.scalar(stmt)

    def update(self, task: Task, **changes: str) -> Task:
        for key, value in changes.items():
            setattr(task, key, value)
        self.session.add(task)
        self.session.flush()
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.flush()
