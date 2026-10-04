from conftest import create_test_restaurant, create_test_users, login_user

def test_create_restaurant_success(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers)
    assert restaurant["title"] == "Test Restaurant"
    assert "id" in restaurant
    assert restaurant["avg_rating"] == 0.0

def test_create_restaurant_duplicate(client, auth_headers):
    response = client.post(
        "/api/v1/restaurants",
        json={
            "title": "Test Restaurant",  # ← same title
            "location": "Lahore",
            "cuisine": "Chinese",
            "contact_number": "03001234567"
        },
        headers=auth_headers
    )
    assert response.status_code == 400

def test_create_restaurant_unauthorized(client):
    response = client.post(
        "/api/v1/restaurants",
        json={
            "title": "Unauth Restaurant",
            "location": "Karachi",
            "cuisine": "Pakistani",
            "contact_number": "03001234567"
        }
    )
    assert response.status_code == 401

def test_get_restaurant_success(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Get Test")
    response = client.get(f"/api/v1/restaurants/{restaurant['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Get Test"

def test_get_restaurant_not_found(client):
    response = client.get("/api/v1/restaurants/999")
    assert response.status_code == 404

def test_update_restaurant_success(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Update Test")
    response = client.patch(
        f"/api/v1/restaurants/{restaurant['id']}",
        json={"title": "Updated Restaurant"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Restaurant"

def test_update_restaurant_not_owner(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Owner Test")
    create_test_users(client, username="testuser3", email="test3@example.com", password="testpassword123")
    other_token = login_user(client, email="test3@example.com", password="testpassword123")
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    response = client.patch(
        f"/api/v1/restaurants/{restaurant['id']}",
        json={"title": "Hacked"},
        headers=other_headers
    )
    assert response.status_code == 403

def test_delete_restaurant_success(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Delete Test")
    response = client.delete(
        f"/api/v1/restaurants/{restaurant['id']}",
        headers=auth_headers
    )
    assert response.status_code == 204