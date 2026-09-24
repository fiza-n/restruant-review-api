from sqlalchemy import select
import models.restaurants, models.reviews, models.users
from fastapi import HTTPException, status


def create_restaurant(db, restaurant, current_user):
    result = db.execute(
        select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.title == restaurant.title)
    )
    existing_restaurant = result.scalars().first()
    if existing_restaurant:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Restaurant already exists")
    
    new_restaurant = models.restaurants.Restaurants(
        title=restaurant.title,
        location=restaurant.location,
        cuisine=restaurant.cuisine,
        contact_number=restaurant.contact_number,
        owner_id=current_user.id
        

    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

def get_restaurant(db, restaurant_id):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))

    existing_restaurant = result.scalars().first()
    if existing_restaurant:
        return existing_restaurant
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

def get_all_restaurants_by_cuisine(cuisine, db):
    if cuisine:
        result = db.execute(select(models.restaurants.Restaurants).where(
            models.restaurants.Restaurants.cuisine == cuisine
        ))
    else:
        result = db.execute(select(models.restaurants.Restaurants))
    
    restaurants = result.scalars().all()
    if not restaurants:
        raise HTTPException(404, "No restaurants found")
    return restaurants

def delete_restaurant(restaurant_id, db,current_user):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    if existing_restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this restaurant")
    
    db.delete(existing_restaurant)
    db.commit()
    return 


def update_restaurant(restaurant_id, db, restaurant, current_user):
    result = db.execute(select(models.restaurants.Restaurants).where(models.restaurants.Restaurants.id == restaurant_id))
    existing_restaurant = result.scalars().first()
    if not existing_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this restaurant")
    
    if restaurant.title is not None:
        existing_restaurant.title = restaurant.title
    if restaurant.location is not None:
        existing_restaurant.location = restaurant.location
    if restaurant.cuisine is not None:
        existing_restaurant.cuisine = restaurant.cuisine
    if restaurant.contact_number is not None:
        existing_restaurant.contact_number = restaurant.contact_number

    db.commit()
    db.refresh(existing_restaurant)
    return existing_restaurant