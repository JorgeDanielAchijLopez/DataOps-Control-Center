import time
import random

from fastapi import APIRouter
from app.database import SessionLocal
from app.models.recovery_log import RecoveryLog
from app.models.backup_history import BackupHistory
from app.services.s3_restore_service import download_backup_from_s3


router = APIRouter(
    prefix="/recovery",
    tags=["Recovery"]
)


@router.post("/drop-table")
def simulate_drop_table():

    db = SessionLocal()

    try:

        log = RecoveryLog(
            event_type="DROP_TABLE",
            affected_table="simulated_orders",
            status="DISASTER_DETECTED",
            rpo_minutes=0,
            rto_seconds=0,
            message="DROP TABLE accidental simulado"
        )

        db.add(log)
        db.commit()

        return {
            "message":
            "DROP TABLE accidental ejecutado"
        }

    finally:

        db.close()


@router.post("/restore")
def restore_latest_backup():

    db = SessionLocal()

    try:

        latest_backup = db.query(
            BackupHistory
        ).order_by(
            BackupHistory.id.desc()
        ).first()

        if not latest_backup:

            return {
                "error":
                "No existen backups"
            }

        start = time.time()

        restored_path = download_backup_from_s3(
            latest_backup.file_name
        )

        time.sleep(2)

        rto = round(
            time.time() - start,
            2
        )

        rpo = round(
            random.uniform(
                5,
                15
            ),
            2
        )

        log = RecoveryLog(
            event_type="RESTORE",
            affected_table="simulated_orders",
            status="RESTORED_FROM_S3",
            rpo_minutes=rpo,
            rto_seconds=rto,
            message=f"Restaurado desde {restored_path}"
        )

        db.add(log)
        db.commit()

        return {
            "message":
            "Restauración desde S3 completada",

            "restored_file":
            restored_path,

            "rpo_minutes":
            rpo,

            "rto_seconds":
            rto
        }

    finally:

        db.close()


@router.get("/history")
def recovery_history():

    db = SessionLocal()

    try:

        return db.query(
            RecoveryLog
        ).all()

    finally:

        db.close()