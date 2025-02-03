from http.client import HTTPException
from pony.orm import *
from fastapi import FastAPI, Form, Depends
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from pydantic_read import CarResponse
from models import db, User, Car
from pydantic_create import UserCreate, CarCreate


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
#Создание Экземпляра класса FastAPI
app = FastAPI(middleware=middleware, title='FastAPI Домашняя работа')
# templates = Jinja2Templates(directory="templates")




#Функция поиска по имени
@db_session
def get_user_by_username(username: str):
    user = User.get(username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#Функция поиска по id
@db_session
def get_user_by_id(user_id: int):
    user = User.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


#Функция добавления пользователя
@app.post("/users", summary="Создание нового пользователя", tags=["Добавить пользователя"])
@db_session
def create_user(user: UserCreate):
    new_user = User(**user.dict())
    commit()
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "cars": [car.model for car in new_user.cars],
    }

#Функция удаления пользователя
@app.delete("/users/{user_id}", summary="Удалить пользователя", tags=["Удалить пользователя"])
@db_session
def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    user.delete()
    commit()



#Функцяи добавления автомобиля
@app.post("/users/{user_id}/cars", summary="Добавление автомобиля", tags=["Добавить автомобиль"])
@db_session
def add_car_to_user(user_id: int, car: CarCreate):
    user = get_user_by_id(user_id)
    new_car = Car(**car.dict(), user=user)
    commit()
    return {
        "id": new_car.id,
        "model": new_car.model,
        "year": new_car.year,
    }

#Функция поиска по имени
@app.get("/users/{username}", summary="Поиск по имени", tags=["Поиск по имени пользователя"])
@db_session
def find_user_by_username(username: str, user: User = Depends(get_user_by_username)):
    user = get_user_by_username(username)
    cars_data = [CarResponse(id=car.id, model=car.model, year=car.year) for car in user.cars]
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "cars": cars_data,
    }


#Функция поиска всех автомобилей пользователя
@app.get("/users/{user_id}/cars", summary="Все автомобили пользоватея", tags=["Вывод всех автомобилей пользователя"])
@db_session
def get_all_user_cars(user_id: int):
    user = get_user_by_id(user_id)
    return [
        {
            "id": car.id,
            "model": car.model,
            "year": car.year
         }
        for car in user.cars
    ]

#Создание базы данных
db.bind(provider="sqlite", filename="database.db", create_db=True)
db.generate_mapping(create_tables=True)





















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