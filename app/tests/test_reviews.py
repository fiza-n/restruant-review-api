from tests.conftest import  create_test_review, create_test_restaurant, auth_headers

def test_create_review_success(client, auth_headers, reviewer_headers):
    restaurants = create_test_restaurant(client, auth_headers)
    review = create_test_review(client, reviewer_headers, restaurants["id"])

    assert review["ratings"] == 5
    assert review["sentiment_label"] == "positive"

def test_create_review_own_restaurant(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers)
    response = client.post(
        f"/api/v1/restaurants/{restaurant['id']}/reviews",
        json={
            "title": "Test review",
            "body": "it was good",
            "rating": 5
        },
        headers=auth_headers
    )
    assert response.status_code == 403 , f"expected 403 for reviewing own restaurant, got {response.status_code}"
    return response.json()

def test_create_review_unauthorized(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Unauth review test")
    response = client.post(
        f"/api/v1/restaurants/{restaurant['id']}/reviews",
        json={
            "title": "Test review",
            "body": "it was good",
            "rating": 5
        }
    )
    assert response.status_code == 401 , f"expected 401 for unauthorized review, got {response.status_code}"
    return response.json()

