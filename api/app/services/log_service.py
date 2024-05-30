from sqlalchemy.orm import Session
from app.models.core import Logs


def get_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Logs).offset(skip).limit(limit).all()
