from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.pool_service import get_domains_with_pool
from database.db_connector import local_db
from starlette.responses import RedirectResponse
from random import choices

router = APIRouter()


@router.get("/v1/redirect_domain/{pool_id:int}", tags=["Redirects"])
async def redirect_domain(pool_id: int, db: Session = Depends(local_db.get_db_session)):
    # Fetching the domain pools from the database for a given pool id
    pools_and_domains = get_domains_with_pool(db, pool_id)

    if not pools_and_domains:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Domains Found"
        )

    domains = [domain.domain for _, domain in pools_and_domains]
    domain_weights = [domain.weight for _, domain in pools_and_domains]
    # Picking a random domain based on the weights
    selected_domain = choices(domains, weights=domain_weights, k=1)[0]

    if not selected_domain.startswith('http'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Selected Domain has no protocol"
        )

    return RedirectResponse(url=selected_domain)

