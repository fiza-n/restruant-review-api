import os
from dotenv import load_dotenv

load_dotenv(".env.test", override=True)

db_url = os.environ.get("DATABASE_URL")

if not db_url:
    raise RuntimeError("DATABASE_URL not set for tests")
if "test" not in db_url.split("/")[-1]:
    raise RuntimeError("Refusing to run tests: DATABASE_URL is not a test database")

os.environ["SECRET_KEY"] = "test-secret-key-at-least-32-characters-long"

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
        db_url,
        poolclass=NullPool,
        connect_args={"connect_timeout": 30},
    )
    yield engine
    engine.dispose()

@pytest.fixture(scope="session")
def setup_database(test_engine):

    Base.metadata.create_all(bind=test_engine)
    
    yield
    
    Base.metadata.drop_all(bind=test_engine)
    

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
    return response.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(client):
    create_test_users(client, username="owneruser", email="owner@example.com")
    token = login_user(client, email="owner@example.com")
    return {"Authorization": f"Bearer {token}"}


def create_test_restaurant(
    client, 
    auth_headers,
    title: str = "Test Restaurant"
):
    response = client.post(
        "/api/v1/restaurants",
        json={
            "title": title,
            "location": "Karachi",
            "cuisine": "Pakistani",
            "contact_number": "03001234567"
        },
        headers=auth_headers  
    )
    assert response.status_code == 201
    return response.json() 

def create_test_review(client, headers,restaurant_id : int, title: str= "Test review"):
    
    response = client.post(
        f"/api/v1/restaurants/{restaurant_id}/reviews",
        json={
            "title":title,
            "body" :"it was good",
            "rating":5
        },
        headers=headers
    )
    assert response.status_code == 201, f"Failed to create review: {response.text}"
    return response.json()

@pytest.fixture(scope="session")
def reviewer_headers(client):
    create_test_users(
        client,
        username="reviewer",
        email="reviewer@example.com",
        password="testpassword123"
    )
    token = login_user(client, email="reviewer@example.com", password="testpassword123")
    return {"Authorization": f"Bearer {token}"}