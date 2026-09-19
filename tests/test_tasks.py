import pytest

from app.database.repositories.task import TaskRepository
from app.database.repositories.user import UserRepository
from app.services.task_service import TaskNotFoundError, TaskService


def create_user(session, telegram_user_id: int):
    user = UserRepository(session).create(telegram_user_id=telegram_user_id, username=None, first_name="Test")
    session.commit()
    return user


def test_task_crud_and_isolation(session):
    user1 = create_user(session, 1)
    user2 = create_user(session, 2)
    service = TaskService(session)

    task = service.create_task(user1.id, "Estudar", "Estudar Python", "pending")
    tasks, total = service.list_tasks(user1.id)
    assert total == 1
    assert tasks[0].id == task.id

    service.update_task(user1.id, task.id, status="completed")
    updated = service.get_task_or_raise(user1.id, task.id)
    assert updated.status == "completed"

    with pytest.raises(TaskNotFoundError):
        service.get_task_or_raise(user2.id, task.id)

    service.delete_task(user1.id, task.id)
    with pytest.raises(TaskNotFoundError):
        service.get_task_or_raise(user1.id, task.id)
