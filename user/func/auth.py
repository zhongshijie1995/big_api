from datetime import timedelta, datetime
from typing import Optional

from user.dao import user
from user.config import secret, exception

from fastapi import HTTPException
from jose import jwt, JWTError


def authenticate_user(_db, username: str, password: str) -> Optional[user.UserModel]:
    """
    用户认证
    :param _db:
    :param username:
    :param password:
    :return:
    """
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码（明文vs密文）
        :param plain_password:
        :param hashed_password:
        :return:
        """
        return secret.pwd_context.verify(plain_password, hashed_password)

    # 获取用户数据
    _user = user.get_user(_db, username)
    if not _user:
        return None
    if not verify_password(password, _user.password):
        return None
    return _user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建认证令牌
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret.SECRET_KEY, algorithm=secret.ALGORITHM)
    return encoded_jwt


def get_exception(msg: str) -> HTTPException:
    """
    获取异常返回类
    :param msg:
    :return:
    """
    return HTTPException(exception.exception_dict[msg], msg)


def get_access_token(username: str) -> str:
    """
    获得令牌
    :param username:
    :return:
    """
    access_token_expires = timedelta(minutes=secret.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'sub': username}, expires_delta=access_token_expires)


def get_username_by_token(token: str) -> Optional[str]:
    """
    通过令牌获得用户名
    :param token:
    :return:
    """
    try:
        return jwt.decode(token, secret.SECRET_KEY, algorithms=[secret.ALGORITHM]).get('sub')
    except JWTError:
        return None
