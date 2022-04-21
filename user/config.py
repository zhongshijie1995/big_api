from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from starlette import status


# 随机密钥，生成命令：openssl rand -hex 32
SECRET_KEY = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
# 加密算法
ALGORITHM = 'HS256'
# 令牌有效时间
ACCESS_TOKEN_EXPIRE_MINUTES = 3600*24*7
# 配置密码认证相关
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 配置授权密码
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
# 异常返回码
exception_dict = {
    '未登录或认证失败': status.HTTP_401_UNAUTHORIZED,
    '用户名或密码错误': status.HTTP_401_UNAUTHORIZED,
    '获取用户失败': status.HTTP_401_UNAUTHORIZED,
}
