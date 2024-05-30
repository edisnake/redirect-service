from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import os


class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("DATABASE_HOST")
        self.user = os.getenv("DATABASE_USERNAME")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.database = os.getenv("DATABASE")
        self.port = int(os.getenv("DATABASE_PORT"))
        if not self.host:
            raise EnvironmentError("DATABASE_HOST environment variable not found")
        if not self.user:
            raise EnvironmentError("DATABASE_USERNAME environment variable not found")
        if not self.password:
            raise EnvironmentError("DATABASE_PASSWORD environment variable not found")
        if not self.database:
            raise EnvironmentError("DATABASE environment variable not found")

        self.db_uri = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        self.engine = create_engine(self.db_uri)
        self.metadata = MetaData()
        self.db_session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db_session(self):
        db = self.db_session()
        try:
            yield db
        finally:
            db.close()


local_db = DatabaseConnector()
