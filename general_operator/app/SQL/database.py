from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SQLDB:
    def __init__(self, db_config:dict, echo=False):
        self.host = db_config["host"]
        self.port = db_config["port"]
        self.db = db_config["db"]
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.pool_recycle = 3600
        if db_config.get("pool_recycle", None) is not None:
            self.pool_recycle = db_config["pool_recycle"]
        self.url = f"mysql+pymysql://{self.user}:{self.password}" \
                   f"@{self.host}:{self.port}/{self.db}"
        # self.url = "postgresql://postgres:123456@localhost:5432/dispatch"
        self.engine = create_engine(
            self.url, echo=echo, connect_args={"connect_timeout": 5},
            pool_size=10,max_overflow=20, pool_recycle=self.pool_recycle)

    def get_engine(self):
        return self.engine

    def new_db_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


Base = declarative_base()

if __name__ == "__main__":
    pass
