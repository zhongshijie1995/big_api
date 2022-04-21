from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import database
from user import func, config
from vip import models

router = APIRouter()


@router.post('/vip/add_vip', response_model=models.VipType, summary='添加会员', description='为指定用户添加会员')
def add_vip(vip: models.VipType, db: Session = Depends(database.get_db)):
    vip_model = models.add_vip(db, vip)
    return vip_model.__dict__


@router.post('/vip/query_vip', response_model=models.VipListType, summary='查询会员', description='查询当前用户持有的会员')
def query_vip(token: str = Depends(config.oauth2_scheme), db: Session = Depends(database.get_db)):
    # 获取用户名
    username = func.get_username_by_token(token)
    if username is None:
        raise func.get_exception('未登录或认证失败')
    vip_list_type = models.VipListType(username=username, vips=models.query_vip(db, username))
    return vip_list_type.__dict__
