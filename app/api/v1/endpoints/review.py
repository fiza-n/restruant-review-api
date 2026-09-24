from fastapi import APIRouter,Depends, status,HTTPException
import models.users
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy.orm import selectinload, Session
import services.review as review_sv
from db.base import get_db
from schemas.review import ReviewResponse, ReviewCreate
from services.auth import oauth2_scheme

router = APIRouter()


@router.post("/{restaurant_id}/reviews", response_model=ReviewResponse,  status_code=status.HTTP_201_CREATED)
def create_review(restaurant_id: int, review: ReviewCreate, db: Annotated[Session, Depends(get_db)],):
    return review_sv.create_review(db, restaurant_id, review)

@router.get("/{restaurant_id}/reviews", response_model=list[ReviewResponse])
def get_reviews_for_restaurant(restaurant_id: int, db: Annotated[Session, Depends(get_db)],):
   return review_sv.get_reviews_for_restaurant(restaurant_id, db)

@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(review_id: int, db: Annotated[Session, Depends(get_db)],):
   return review_sv.delete_review(review_id, db)