from tests.conftest import login_user,create_test_users


def test_register_success(client):
    user = create_test_users(client)
    assert user["email"] == "test@example.com"
    assert user["username"] == "testuser"
    assert "password" not in user
    
def test_login_success(client):
    token = login_user(client)
    assert token is not None
    assert isinstance(token, str)


def test_register_duplicate_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 400, f"expected 400 for duplicate email, got {response.status_code}"

def test_register_duplicate_username(client):
    response = client.post(
        "/api/v1/auth/register",
        json = {
            "username": "testuser",
            "email": "test1@example.com",
            "password": "testpassword123"
        }

    )
    assert response.status_code == 400, f"expected 400 for duplicate username, got {response.status_code}"

def test_register_short_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json = {
            "username": "testuser3",
            "email": "test2@example.com",
            "password": "test"
        }
    )
    assert response.status_code == 422, f"expected 422 for short password, got {response.status_code}"

def test_login_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        data = {
            "username": "test@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401, f"expected 401 for wrong password, got {response.status_code}"