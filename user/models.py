from typing import Optional

from sqlalchemy import Column, String
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import database


class UserModel(database.Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password = Column(String)
    email = Column(String)
    show_name = Column(String, nullable=True)
    show_desc = Column(String, nullable=True)
    addition = Column(String, nullable=True)


class UserType(BaseModel):
    username: str
    password: str
    email: str
    show_name: Optional[str] = None
    show_desc: Optional[str] = None
    addition: Optional[str] = None


class TokenType(BaseModel):
    access_token: str
    token_type: str


def create_user(db: Session, user: UserType) -> UserModel:
    """
    创建用户
    :param db:
    :param user:
    :return:
    """
    db_user = UserModel(**user.__dict__)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str) -> UserModel:
    """
    查询用户
    :param db:
    :param username:
    :return:
    """
    return db.query(UserModel).get(username)
