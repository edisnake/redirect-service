from sqlalchemy.orm import Session
from app.models.core import Pool, Domain, Logs
from app.schemas.pool_schema import PoolSchema
from sqlalchemy.future import select
from typing import Optional


def create_pool(db: Session, pool: PoolSchema):
    db_pool = Pool(name=pool.name)
    db.add(db_pool)
    db.commit()
    db.refresh(db_pool)

    domains = [
        Domain(pool_id=db_pool.id, weight=domain_row.weight, domain=domain_row.domain)
        for domain_row in pool.domains
    ]
    db.add_all(domains)
    db.commit()

    return db_pool


def get_pools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pool).offset(skip).limit(limit).all()


def get_domains_with_pool(db: Session, pool_id: Optional[int] = None):
    query = (
        select(Pool, Domain)
        .join(
            Domain,
            Domain.pool_id == Pool.id,
        )
    )

    if pool_id:
        query = query.filter(Pool.id == pool_id)
    else:
        query.order_by(Pool.id)

    return db.execute(query).all()
