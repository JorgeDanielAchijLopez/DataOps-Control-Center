from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.alert_log import AlertLog

router=APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


def get_db():

    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_alerts(
    db:Session=
    Depends(
        get_db)
):

    return db.query(
        AlertLog
    ).all()