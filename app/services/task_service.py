import logging

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database.models import Task
from app.database.repositories import TaskRepository
from app.utils.validators import validate_create_payload, validate_update_payload

logger = logging.getLogger(__name__)


class TaskNotFoundError(Exception):
    pass


class TaskValidationError(Exception):
    pass


class TaskService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = TaskRepository(session)

    def create_task(self, user_id: int, title: str, description: str, status: str) -> Task:
        try:
            payload = validate_create_payload({"title": title, "description": description, "status": status})
        except ValidationError as exc:
            raise TaskValidationError(str(exc)) from exc
        task = self.repository.create(user_id=user_id, **payload.model_dump())
        self.session.commit()
        logger.info("Task created user_id=%s task_id=%s", user_id, task.id)
        return task

    def list_tasks(self, user_id: int, page: int = 1, page_size: int = 5) -> tuple[list[Task], int]:
        page = max(page, 1)
        offset = (page - 1) * page_size
        tasks = self.repository.list_by_user(user_id=user_id, offset=offset, limit=page_size)
        total = self.repository.count_by_user(user_id=user_id)
        return tasks, total

    def get_task_or_raise(self, user_id: int, task_id: int) -> Task:
        task = self.repository.get_user_task(user_id=user_id, task_id=task_id)
        if task is None:
            raise TaskNotFoundError("Tarefa não encontrada")
        return task

    def update_task(self, user_id: int, task_id: int, **changes: str) -> Task:
        task = self.get_task_or_raise(user_id=user_id, task_id=task_id)
        try:
            payload = validate_update_payload(changes)
        except (ValidationError, ValueError) as exc:
            raise TaskValidationError(str(exc)) from exc
        updated = self.repository.update(task, **payload.model_dump(exclude_none=True))
        self.session.commit()
        logger.info("Task updated user_id=%s task_id=%s", user_id, task_id)
        return updated

    def delete_task(self, user_id: int, task_id: int) -> None:
        task = self.get_task_or_raise(user_id=user_id, task_id=task_id)
        self.repository.delete(task)
        self.session.commit()
        logger.info("Task deleted user_id=%s task_id=%s", user_id, task_id)
