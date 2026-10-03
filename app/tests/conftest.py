import os 
os.environ["DATABASE_URL"] = (
    ""
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base, get_db
from main import app
from sqlalchemy.pool import NullPool




@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(
        os.environ["DATABASE_URL"],
        poolclass=NullPool
    )
    return engine

@pytest.fixture(scope="session")
def setup_database(test_engine):

    Base.metadata.create_all(bind=test_engine)
    
    yield
    
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()

@pytest.fixture(scope="session")
def db_session(test_engine, setup_database):
    conn = test_engine.connect()
    trans = conn.begin()

    test_session = sessionmaker(bind=conn,expire_on_commit=False, join_transaction_mode="create_savepoint")

    with test_session() as session:

        try: 
           yield session

        finally: 
            session.close()
            trans.rollback()
            conn.close()


@pytest.fixture(scope="session")
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app=app) as c:
        yield c

    app.dependency_overrides.clear()

def create_test_users(
    client: TestClient,
    username:str =  "testuser",
    email: str = "test@example.com",
    password: str = "testpassword123"
) -> dict:
    response = client.post(
        "/api/v1/auth/register",
        json = {
            "username": username,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 201, f"failed create user: {response.text}"
    return response.json()


def login_user(client: TestClient, email: str = "test@example.com", password: str = "testpassword123") -> str:
    response = client.post(
        "/api/v1/auth/login",
        data = {
            "username": email,
            "password": password
        }
    )
    assert response.status_code == 200, f"failed login user: {response.text}"
    return response.json()
