import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, DATE, String
from sqlalchemy.orm import Session

from db import database


class VipModel(database.Base):
    __tablename__ = 'vips'
    id = Column(Integer, primary_key=True)
    start_time = Column(DATE)
    end_time = Column(DATE)
    username = Column(String, ForeignKey("users.username"))


class VipType(BaseModel):
    id: Optional[int]
    start_time: datetime.date
    end_time: datetime.date
    username: str


class VipListType(BaseModel):
    username: str
    vips: list


def add_vip(db: Session, vip: VipType):
    db_vip = VipModel(**vip.__dict__)
    db_vip.id = len(query_vip(db, db_vip.username))
    db.add(db_vip)
    db.commit()
    db.refresh(db_vip)
    return db_vip


def query_vip(db: Session, username: str) -> list:
    return db.query(VipModel).filter(VipModel.username == username).all()
