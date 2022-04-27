from starlette import status


# 异常返回码
exception_dict = {
    '未登录或认证失败': status.HTTP_401_UNAUTHORIZED,
    '用户名或密码错误': status.HTTP_401_UNAUTHORIZED,
    '获取用户失败': status.HTTP_401_UNAUTHORIZED,
}
