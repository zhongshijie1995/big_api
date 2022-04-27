from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from user.config import secret
from user.dao import user
from user.dao import token
from user.func import auth
from comm import database


# 初始化路由
router = APIRouter()


@router.post('/user/signup', summary='注册', description='用户注册')
def register(_user: user.UserType, _db: Session = Depends(database.get_db)):
    # 对密码进行加密
    _user.password = secret.pwd_context.hash(_user.password)
    # 创建用户资料并获得用户资料
    _user_model = user.create_user(_db, _user).__dict__
    # 隐去敏感信息
    del _user_model['password']
    # 返回用户资料
    return _user_model


@router.post('/user/login', summary='登录', description='用户登录')
def login(form_data: OAuth2PasswordRequestForm = Depends(), _db: Session = Depends(database.get_db)):
    # 用户认证
    _user = auth.authenticate_user(_db, form_data.username, form_data.password)
    if _user is None:
        raise auth.get_exception('用户名或密码错误')
    # 为用户创建令牌
    access_token = auth.get_access_token(_user.username)
    # 获得令牌
    _token = token.TokenType(access_token=access_token, token_type='bearer')
    # 返回令牌
    return _token


@router.get('/user/me', summary='我')
def me(_token: str = Depends(secret.oauth2_scheme), _db: Session = Depends(database.get_db)):
    # 获取用户名
    username = auth.get_username_by_token(_token)
    if username is None:
        raise auth.get_exception('未登录或认证失败')
    # 获取用户资料
    _user_model = user.get_user(_db, username=username).__dict__
    if _user_model is None:
        raise auth.get_exception('获取用户失败')
    # 隐去敏感信息
    del _user_model['password']
    # 返回用户资料
    return _user_model
