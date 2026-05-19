from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.replication_status import ReplicationStatus

router = APIRouter(
    prefix="/replication",
    tags=["Replication"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_replication(
    db: Session =
    Depends(
        get_db
    )
):

    return db.query(
        ReplicationStatus
    ).all()