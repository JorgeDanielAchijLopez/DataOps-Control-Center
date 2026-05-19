from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.tx_log import TXLog

router=APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


def get_db():

    db=SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_transactions(
    db:Session=
    Depends(
        get_db
    )
):

    return db.query(
        TXLog
    ).all()