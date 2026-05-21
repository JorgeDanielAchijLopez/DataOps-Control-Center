from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.snapshot_log import SnapshotLog


router = APIRouter(
    prefix="/snapshots",
    tags=["Snapshots"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_snapshots(
    db: Session = Depends(get_db)
):

    return db.query(
        SnapshotLog
    ).all()