from fastapi import status,HTTPException
import models.users
from sqlalchemy import select, func
from services.auth import hash_password, oauth2_scheme, verify_password, create_access_token, verify_access_token
from datetime import datetime, UTC, timedelta
from core.config import settings
from schemas.users import Token

def create_user(user, db):
    result = db.execute(select(models.users.User).where(func.lower(models.users.User.username) == user.username.lower()),)
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    result = db.execute(select(models.users.User).where(func.lower(models.users.User.email) == user.email.lower()),)
    existing_email = result.scalars().first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_user = models.users.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_for_access_token(form_data,db):
    result =  db.execute(select(models.users.User).where(func.lower(models.users.User.email) == form_data.username.lower()))
    user= result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data ={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

def get_current_user(token, db):
    user_id = verify_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id_int = int(user_id)
    except TypeError, ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    result = db.execute(select(models.users.User).where(models.users.User.id == user_id_int))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_user(user_id, db):
    result = db.execute(select(models.users.User).where(models.users.User.id == user_id),)

    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
