
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.db import Base, get_db
from app.database import repository
from app.database.models import User
from app.api.auth import hash_password


@pytest.fixture
def client(monkeypatch):

    # Separate temporary database for tests
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    # Use temporary database for repository operations
    monkeypatch.setattr(
        repository,
        "SessionLocal",
        TestingSessionLocal
    )

    # Use temporary database for authentication
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestingSessionLocal() as db:
        test_user = User(
            name="Test User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123")
        )
        db.add(test_user)
        db.commit()

    with TestClient(app) as test_client:

        # Automatically log in test user
        response = test_client.post(
            "/auth/login",
            json={
                "email": "test@example.com",
                "password": "TestPassword123"
            }
        )

        assert response.status_code == 200

        yield test_client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)
    engine.dispose()
