from fastapi import status,HTTPException
import models.users
from sqlalchemy import select

def create_user(user, db):
    result = db.execute(select(models.users.User).where(models.users.User.username == user.username),)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    result = db.execute(select(models.users.User).where(models.users.User.email == user.email),)
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = models.users.User(
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(user_id, db):
    result = db.execute(select(models.users.User).where(models.users.User.id == user_id),)

    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
