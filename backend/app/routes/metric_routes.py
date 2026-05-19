from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.db_metric import DBMetric

router=APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


def get_db():

    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_metrics(
    db:Session=
    Depends(
        get_db
    )
):

    return db.query(
        DBMetric
    ).all()