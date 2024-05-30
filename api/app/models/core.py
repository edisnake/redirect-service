from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, event, text, insert
from app.models.base import Base
from database.db_connector import local_db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


class Logs(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    message = Column(String(500), nullable=False)
    level = Column(String(50))
    params = Column(String(200))


class Pool(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)


class Domain(Base):
    id = Column(Integer, primary_key=True)
    pool_id = Column(Integer, ForeignKey("pool.id"), nullable=False)
    weight = Column(Integer, nullable=False)
    domain = Column(String(200), nullable=False)


# Following this pattern to make sure the table models are created into the DB
local_db.metadata.create_all(local_db.engine)


class SQLAlchemyLogHandler(logging.Handler):
    def emit(self, record):
        # Skipping redundant DB logs
        if 'logs' in record.msg:
            return None

        # Insert log entry into the database
        with local_db.engine.connect() as connection:
            connection.execute(
                insert(Logs).values(message=record.msg, level=record.levelname, params=str(record.args))
            )


# Add the handler to the root logger
logging.getLogger().addHandler(SQLAlchemyLogHandler())


# Log SQL statements
@event.listens_for(local_db.engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    logging.info(f" Executed: {statement} with params: {parameters}")

