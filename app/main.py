from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from schemas.users import UserResponse, UserCreate

app = FastAPI()

users = []

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():

    return f"<h1>Hello world</h1>"


@app.post("/api/v1/users", response_model=UserResponse, status_code=201)
def create_user(user:UserCreate):
    new_user = {
        "id": 1,
        "full_name": user.full_name,
        "email": user.email,
        "password": user.password
    }
    users.append(new_user)
    return new_user

