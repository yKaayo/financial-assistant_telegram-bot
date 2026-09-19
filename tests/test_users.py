from app.database.repositories.user import UserRepository


def test_create_user(session):
    repo = UserRepository(session)
    created = repo.create(telegram_user_id=101, username="john", first_name="John")
    session.commit()

    loaded = repo.get_by_telegram_user_id(101)
    assert loaded is not None
    assert loaded.id == created.id
    assert loaded.username == "john"
