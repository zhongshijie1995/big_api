from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# 数据库连接串
db_drive = 'mysql+pymysql'
db_host = '192.168.0.101'
db_port = '3306'
db_name = 'big_api_test'
db_user = 'big_api_test'
db_pwd = 'big_api_test'
# 数据库连接串
SQLALCHEMY_DATABASE_URL = '%s://%s:%s@%s:%s/%s' % (db_drive, db_user, db_pwd, db_host, db_port, db_name)
# 创建数据库连接引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
