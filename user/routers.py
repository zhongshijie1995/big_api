from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from user import models, config, func
from db import database


# 初始化路由
router = APIRouter()


@router.post('/user/signup', response_model=models.UserType, summary='注册', description='用户注册')
def register(user: models.UserType, db: Session = Depends(database.get_db)):
    # 对密码进行加密
    user.password = config.pwd_context.hash(user.password)
    # 创建用户资料
    user_model = models.create_user(db, user)
    return user_model.__dict__


@router.post('/user/login', response_model=models.TokenType, summary='登录', description='用户登录')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # 用户认证
    user = func.authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise func.get_exception('用户名或密码错误')
    # 为用户创建令牌
    access_token = func.get_access_token(user.username)
    # 返回令牌
    return models.TokenType(access_token=access_token, token_type='bearer')


@router.get('/user/me', response_model=models.UserType, summary='我')
def me(token: str = Depends(config.oauth2_scheme), db: Session = Depends(database.get_db)):
    # 获取用户名
    username = func.get_username_by_token(token)
    if username is None:
        raise func.get_exception('未登录或认证失败')
    # 获取用户资料
    user_model = models.get_user(db, username=username)
    if user_model is None:
        raise func.get_exception('获取用户失败')
    # 返回用户资料
    return user_model.__dict__
