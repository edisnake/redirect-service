from sqlalchemy.ext.declarative import declarative_base, declared_attr
from database.db_connector import local_db
from app.utils import camel2snake


class CustomBase:
    # Generates __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)  # type: ignore


Base = declarative_base(cls=CustomBase, metadata=local_db.metadata)
