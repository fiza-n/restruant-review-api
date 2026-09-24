from fastapi import APIRouter,Depends, status
import models.users
from typing import Annotated
from sqlalchemy.orm import Session
import services.review as review_sv
from db.base import get_db
from schemas.review import ReviewResponse, ReviewCreate
from core.dependencies import CurrentUser
router = APIRouter()


@router.post("/{restaurant_id}/reviews", response_model=ReviewResponse,  status_code=status.HTTP_201_CREATED)
def create_review(restaurant_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)], current_user: CurrentUser):
    return review_sv.create_review(db, restaurant_id, review, current_user)

@router.get("/{restaurant_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_for_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
   return review_sv.get_reviews_for_restaurant(restaurant_id, db)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Annotated[Session, Depends(get_db)], current_user: CurrentUser):
   return review_sv.delete_review(review_id, db, current_user)