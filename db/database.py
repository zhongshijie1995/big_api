from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from db import config


# 创建数据库连接引擎
engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': True if config.SQLALCHEMY_DATABASE_URL else False}
)
# 配置数据库连接会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 数据库ORM模型基类
Base = declarative_base()


def get_db() -> SessionLocal:
    """
    获取数据库会话

    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    初始化数据库连接

    :return:
    """
    Base.metadata.create_all(bind=engine)
