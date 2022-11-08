from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas
from .models import User


def get_user_by_id(db: Session, user_id: int) -> Session.query:
    user = db.query(models.User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
    return user


def get_user_by_email(db: Session, email: str) -> Session.query:
    user = db.query(models.User).filter(User.email == email).first()
    return user


def get_all_users_skips(db: Session, skip: int = 0, limit: int = 100) -> Session.query:
    return db.query(User).offset(skip).limit(limit).all()


def get_all_users(db: Session, ) -> Session.query:
    return db.query(User).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    password = "fakehashed" + user.password
    new_user = models.User(email=user.email,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user: schemas.UserUpdate, user_id):
    user_data = user.dict(exclude_unset=True)
    updating_user = get_user_by_id(db, user_id)
    for key, value in user_data.items():
        setattr(updating_user, key, value)
    db.add(updating_user)
    db.commit()
    db.refresh(updating_user)
    return updating_user


def delete_user(db: Session, user_id: int):
    deleting_user = get_user_by_id(db, user_id)
    db.delete(deleting_user)
    db.commit()
    raise HTTPException(status_code=200, detail="User successfully deleted")


