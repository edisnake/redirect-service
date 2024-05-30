from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.services.pool_service import create_pool, get_domains_with_pool
from app.schemas.pool_schema import PoolSchema, DomainSchema, PoolOutputSchema
from database.db_connector import local_db


router = APIRouter()


@router.get("/v1/pools", tags=["Pools"])
async def get_pools_resource(db: Session = Depends(local_db.get_db_session)):
    # Fetch the domain pools from the database
    domain_pools = get_domains_with_pool(db)

    if not domain_pools:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Pools Found"
        )

    pools_dict = {}
    for pool, domain in domain_pools:
        if pool.id not in pools_dict:
            pools_dict[pool.id] = PoolOutputSchema(id=pool.id, name=pool.name, domains=[])

        pools_dict[pool.id].domains.append(DomainSchema(pool_id=pool.id, weight=domain.weight, domain=domain.domain))

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(list(pools_dict.values())))


@router.post("/v1/pools", tags=["Pools"], response_model=PoolSchema)
async def create_pool_resource(pool_data: PoolSchema, db: Session = Depends(local_db.get_db_session)):
    try:
        create_pool(db, pool_data)
        return pool_data
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )



