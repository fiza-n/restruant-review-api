from sqlalchemy import select
import models.restaurants, models.reviews, models.users
from fastapi import HTTPException, status
from sentiment import *


def create_review(db,restaurant_id, review):

    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    label, compound = evaluate_sentiment(review.body)
    
    new_review = models.reviews.Reviews(
                title=review.title,
                body=review.body,
                rating=review.rating,
                sentiment_label=label,
                sentiment_score=compound,
                user_id=1,
                restaurants_id=restaurant_id,

    
            )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    

    all_reviews = db.execute(select(models.reviews.Reviews).where(
        models.reviews.Reviews.restaurant_id == restaurant_id
    ))
    reviews_list = all_reviews.scalars().all()
    existing_restaurant.avg_rating = sum(r.rating for r in reviews_list) / len(reviews_list)
    db.commit()

    return new_review

def delete_review(review_id, db):
    result = db.execute(select(models.reviews.Reviews).where(models.reviews.Reviews.id == review_id))
    existing_review = result.scalars().first()
    if not existing_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    
    db.delete(existing_review)
    db.commit()
    return

def get_reviews_for_restaurant(restaurant_id, db):
    result = db.execute(select(models.reviews.Reviews).where(models.reviews.Reviews.restaurants_id == restaurant_id))
    reviews = result.scalars().all()
    if reviews:
        return reviews
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found for the specified restaurant")