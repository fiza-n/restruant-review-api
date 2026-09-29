from fastapi import FastAPI
from fastapi.testclient import TestClient

test_auth = FastAPI()

@test_auth.get("/api/v1/users")
def test_auth_routes():
    return {"message": "hello"}

client = TestClient(test_auth_routes)

def test_auth():
    response = client.get("/api/v1/users")
    assert response.status_code == 200