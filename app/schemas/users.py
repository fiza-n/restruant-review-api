from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str = Field(min_length=1, max_length = 50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length = 50)



class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length = 50)

class UserPublic(BaseModel):
    id: int
    username: str
    image_file: str | None
    image_path: str | None
    model_config = ConfigDict(from_attributes=True)

class UserPrivate(UserPublic):
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str