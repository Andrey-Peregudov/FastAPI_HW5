from typing import List
from pydantic_read import UserResponse, CarResponse
from pydantic_create import UserCreate, Careate

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from starlette.responses import Response
from starlette.status import HTTP_202_ACCEPTED, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_406_NOT_ACCEPTABLE, HTTP_405_METHOD_NOT_ALLOWED, HTTP_409_CONFLICT
#
# from database import get_session
# from models import User, UserRead, UserAndNews, News, UserReadOrderBy, UserUpdate

router = APIRouter()
#
#
# @router.get('/user', response_model=UserRead)
# async def user(user_id: int, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE)
#     return user
#
#
# @router.get('/user_and_news', response_model=UserAndNews)
# async def user_and_news(user_id: int, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
#     news = session.exec(select(News).where(News.nums > 80).limit(20)).all()
#     response = UserAndNews(user=user, news=news)
#     return response
#
#
# @router.delete('/user')
# def delete_user(user_id: int, session: Session = Depends(get_session)):
#     user = session.get(User, user_id)
#     session.delete(user)
#     session.commit()
#     return Response(status_code=HTTP_202_ACCEPTED)
#
#
# @router.get('/user_list', response_model=List[UserReadOrderBy], summary='Список с сортировкой')
# def user_list(session: Session = Depends(get_session)):
#     response = session.exec(select(User).order_by(User.username)).all()
#     return response
#
#
# @router.put('/user/{id}', response_model=UserRead)
# async def update_user(id: int, user_new: UserUpdate, session: Session = Depends(get_session)):
#     user = session.get(User, id)
#     if not user:
#         raise HTTPException(status_code=HTTP_409_CONFLICT, detail='Not found user')
#     user_data = user_new.dict(exclude_unset=True)
#     for key, value in user_data.items():
#         setattr(user, key, value)
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user
