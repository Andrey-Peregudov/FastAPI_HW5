from fastapi import FastAPI, Form
from starlette.middleware import Middleware
from starlette.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.pydantic_create import UserCreate
from models import db, User, Car
# from .pydantic_read import UserResponse, CarResponse
# from .pydantic_create import UserCreate, CarCreate


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

app = FastAPI(middleware=middleware, title='FastAPI Jinja2 Postress Websocket')
# app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")




# @app.post("/user_name")
# async def user_name():
#     return {"Hello": "id"}

#
# @app.get("/test/{id}", response_class=HTMLResponse)
# async def root(request: Request, id: str):
#     return templates.TemplateResponse(
#         request=request, name="index.html", context={"id": id})
#
#
# @app.get("/form", response_class=HTMLResponse)
# async def form(request: Request):
#     return templates.TemplateResponse('form.html', {'request': request})


users = []

@app.post('/usr_name')
async def user_name(user_name: UserCreate):
    users.append(user_name)
    return users


# db.bind(provider='postgres', user='fastapi_jinja2', password='fastapi_jinja2', host='db', database='fastapi_jinja2',
#         port='5432')
# db.generate_mapping(create_tables=True)

# import user

# app.include_router(user.router, prefix="/user", tags=["user"])





















# from fastapi import FastAPI, HTTPException, Depends, status, Form
# from pony.orm import *
# from typing import List, Optional
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
#
#
# # Database setup
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
#
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is not set")
#
# db = Database()
#
# def connect_db():
#     db.bind(provider="sqlite", filename=DATABASE_URL, create_db=True)
#     db.generate_mapping(create_tables=True)
# connect_db()
#
# # Models
# class User(db.Entity):
#     id = PrimaryKey(int, auto=True)
#     username = Required(str, unique=True)
#     email = Optional(str, unique=True)
#     name = Required(str)
#     cars = Set("Car")
#
# class Car(db.Entity):
#     id = PrimaryKey(int, auto=True)
#     model = Required(str)
#     year = Optional(int)
#     user = Required(User)
#
#
# # Schemas
# class UserCreate(BaseModel):
#     username: str
#     email: Optional[str] = None
#     name: str
#
# class UserResponse(BaseModel):
#     id: int
#     username: str
#     email: Optional[str]
#     name: str
#     cars: List[str]
#
# class CarCreate(BaseModel):
#     model: str
#     year: Optional[int] = None
#
# class CarResponse(BaseModel):
#     id: int
#     model: str
#     year: Optional[int]
#
#
#
# # Utility functions
# @db_session
# def get_user_by_username(username: str):
#     user = User.get(username=username)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
# @db_session
# def get_user_by_id(user_id: int):
#     user = User.get(id=user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
#
#
# # FastAPI app
# app = FastAPI()
#
# @app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Create a new user")
# @db_session
# def create_user(user: UserCreate):
#     new_user = User(**user.dict())
#     commit()
#     return {
#         "id": new_user.id,
#         "username": new_user.username,
#         "email": new_user.email,
#         "name": new_user.name,
#         "cars": [car.model for car in new_user.cars],
#     }
#
#
# @app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user")
# @db_session
# def delete_user(user_id: int):
#     user = get_user_by_id(user_id)
#     user.delete()
#     commit()
#
#
# @app.get("/users/{username}", response_model=UserResponse, summary="Find a user by username")
# def find_user_by_username(username: str, user: User = Depends(get_user_by_username)):
#     return {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email,
#         "name": user.name,
#         "cars": [car.model for car in user.cars],
#     }
#
# @app.post("/users/{user_id}/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED, summary="Add a car to a user")
# @db_session
# def add_car_to_user(user_id: int, car: CarCreate):
#     user = get_user_by_id(user_id)
#     new_car = Car(**car.dict(), user=user)
#     commit()
#     return {
#         "id": new_car.id,
#         "model": new_car.model,
#         "year": new_car.year,
#     }
#
# @app.get("/users/{user_id}/cars", response_model=List[CarResponse], summary="Get all cars for a user")
# @db_session
# def get_all_user_cars(user_id: int):
#     user = get_user_by_id(user_id)
#     return [
#         {
#             "id": car.id,
#             "model": car.model,
#             "year": car.year
#          }
#         for car in user.cars
#     ]