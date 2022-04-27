from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from comm import database


class UserModel(database.Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), index=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(11), nullable=True)
    show_name = Column(String(100), nullable=True)
    show_desc = Column(String(200), nullable=True)
    addition = Column(String(100), nullable=True)


class UserType(BaseModel):
    username: str
    password: str
    email: str
    phone: Optional[str]
    show_name: Optional[str]
    show_desc: Optional[str]
    addition: Optional[str]


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
