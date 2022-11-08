from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from . import crud
from . import schemas

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@router.get("/api/users", response_model=list[schemas.UserDetail])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return users


@router.get("/api/user/{user_id}", response_model=list[schemas.UserDetail])
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(db=db, user_id=user_id)


@router.post("/api/user/create", response_model=schemas.UserDetail)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.put("/api/user/update/{user_id}", response_model=schemas.UserDetail)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db=db, user_id=user_id, user=user)


@router.delete("/api/user/delete/{user_id}", response_model=schemas.UserDetail)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_user(db=db, user_id=user_id)
