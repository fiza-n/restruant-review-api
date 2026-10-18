from tests.conftest import  create_test_review, create_test_restaurant

def test_create_review_success(client, auth_headers, reviewer_headers):
    restaurants = create_test_restaurant(client, auth_headers, title="Test Review Success")
    review = create_test_review(client, reviewer_headers, restaurants["id"])

    assert review["rating"] == 5
    assert review["sentiment_label"] == "positive"

def test_create_review_own_restaurant(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers,title="Test own restaurant")
    response = client.post(
        f"/api/v1/restaurants/{restaurant['id']}/reviews",
        json={
            "title": "Review of my own restaurant",
            "body": "it was good",
            "rating": 5
        },
        headers=auth_headers
    )
    assert response.status_code == 403 , f"expected 403 for reviewing own restaurant, got {response.status_code}"
    

def test_create_review_unauthorized(client, auth_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Unauth Review Test")
    response = client.post(
        f"/api/v1/restaurants/{restaurant['id']}/reviews",
        json={
            "title": "Unauthorized review",
            "body": "it was good",
            "rating": 5
        }
    )
    assert response.status_code == 401 , f"expected 401 for unauthorized review, got {response.status_code}"
   

def test_create_review_restaurant_not_found(client, reviewer_headers):
    response  = client.post(
        "/api/v1/restaurants/999/reviews",
        json={
            "title": "Test review for non-existent restaurant",
            "body": "it was good",
            "rating": 5

        },
        headers=reviewer_headers
    )
    assert response.status_code == 404 , f"expected 404 for restaurant not found, got {response.status_code}"


def test_get_reviews(client, auth_headers, reviewer_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Get reviews test")
    create_test_review(client, reviewer_headers, restaurant["id"], title="Test review 1")
    create_test_review(client, reviewer_headers, restaurant["id"], title="Test review 2")

    response = client.get(f"/api/v1/restaurants/{restaurant['id']}/reviews")
    assert response.status_code == 200
    reviews = response.json()
    assert len(reviews) == 2


def test_delete_review_not_owner(client, auth_headers, reviewer_headers):
    restaurant = create_test_restaurant(client, auth_headers, title="Delete review test")
    review = create_test_review(client, reviewer_headers, restaurant["id"], title="Test review to delete")

    response = client.delete(
        f"/api/v1/reviews/{review['id']}",
        headers=auth_headers
    )
    assert response.status_code == 403 , f"expected 403 for deleting review not owned by user, got {response.status_code}"