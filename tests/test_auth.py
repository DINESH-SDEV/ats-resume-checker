import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


USER = {"name": "Test User", "email": "test@example.com", "password": "secret123"}


def register(client):
    return client.post("/register", json=USER)


def login(client, password="secret123"):
    return client.post("/login", data={"username": USER["email"], "password": password})


def test_register_success(client):
    r = register(client)
    assert r.status_code == 200
    assert r.json()["email"] == USER["email"]
    assert "password" not in r.json()
    assert "hashed_password" not in r.json()


def test_register_duplicate_email(client):
    register(client)
    r = register(client)
    assert r.status_code == 400


def test_login_success(client):
    register(client)
    r = login(client)
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    register(client)
    r = login(client, password="wrong")
    assert r.status_code == 401


def test_me_without_token(client):
    r = client.get("/me")
    assert r.status_code == 401


def test_me_with_token(client):
    register(client)
    token = login(client).json()["access_token"]
    r = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["email"] == USER["email"]