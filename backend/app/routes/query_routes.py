from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.query_log import QueryLog

router = APIRouter(
    prefix="/queries",
    tags=["Queries"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_queries(
    db: Session = Depends(get_db)
):

    return db.query(
        QueryLog
    ).all()