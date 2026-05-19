from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.backup_history import BackupHistory

router = APIRouter(
    prefix="/backups",
    tags=["Backups"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.get("/")
def get_backups(
    db: Session =
    Depends(
        get_db
    )
):

    return db.query(
        BackupHistory
    ).all()