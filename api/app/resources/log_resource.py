from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.log_service import get_logs
from database.db_connector import local_db


router = APIRouter()


@router.get("/v1/logs", tags=["Logs"])
async def get_logs_resource(db: Session = Depends(local_db.get_db_session)):
    logs = get_logs(db)

    if not logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Logs Found"
        )

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(logs))

