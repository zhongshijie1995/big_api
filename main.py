from fastapi import FastAPI

from user import routers as user_routers
from comm import database


# 初始化数据库
database.init_db()

# 初始化应用
app = FastAPI(
    title='API试验场',
    description='FastAPI实验大操场，集成一些实验过程',
    version='0.0.1',
    redoc_url=None,
    docs_url='/',
    swagger_ui_parameters={
        'defaultModelsExpandDepth': -1,
        'tryItOutEnabled': True
    },
)
# 包括模块的路由
app.include_router(user_routers.router, tags=['用户'])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host="0.0.0.0", port=28998, reload=True)
