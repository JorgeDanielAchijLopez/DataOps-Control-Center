from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.backup_history import BackupHistory
from app.services.backup_service import generate_backup


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
    db: Session = Depends(get_db)
):

    return db.query(
        BackupHistory
    ).all()


@router.post("/run/{backup_type}")
def run_backup(
    backup_type: str
):

    generate_backup(
        backup_type.upper()
    )

    return {
        "message":
        f"Backup {backup_type.upper()} ejecutado correctamente"
    }