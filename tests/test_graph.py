from app.database.repositories.user import UserRepository
from app.services.graph_service import GraphService


def test_graph_create_flow(session):
    user = UserRepository(session).create(telegram_user_id=111, username="u", first_name="U")
    session.commit()
    graph = GraphService(session)

    s1 = graph.process_event(user.telegram_user_id, 1, "callback", "action_create")
    assert s1["step"] == "waiting_title"

    s2 = graph.process_event(user.telegram_user_id, 1, "message", "Minha tarefa")
    assert s2["step"] == "waiting_description"

    s3 = graph.process_event(user.telegram_user_id, 1, "message", "Descrição da tarefa")
    assert s3["step"] == "waiting_status"

    s4 = graph.process_event(user.telegram_user_id, 1, "callback", "status_pending")
    assert s4["action"] == "menu"


def test_graph_cancel(session):
    user = UserRepository(session).create(telegram_user_id=222, username="u", first_name="U")
    session.commit()
    graph = GraphService(session)

    graph.process_event(user.telegram_user_id, 1, "callback", "action_create")
    canceled = graph.process_event(user.telegram_user_id, 1, "callback", "cancel")
    assert canceled["action"] == "menu"
    assert canceled["step"] == "idle"
