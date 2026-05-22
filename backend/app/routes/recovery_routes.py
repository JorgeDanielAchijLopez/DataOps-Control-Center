import time
import random

from fastapi import APIRouter
from app.database import SessionLocal
from app.models.recovery_log import RecoveryLog


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
            message="Se simuló un DROP TABLE accidental sobre simulated_orders"
        )

        db.add(log)
        db.commit()

        return {
            "message": "Desastre simulado correctamente",
            "affected_table": "simulated_orders",
            "event": "DROP TABLE accidental"
        }

    finally:
        db.close()


@router.post("/restore")
def restore_table():

    db = SessionLocal()

    try:
        start = time.time()

        time.sleep(2)

        rto = round(
            time.time() - start,
            2
        )

        rpo = round(
            random.uniform(5, 15),
            2
        )

        status = (
            "RESTORED"
            if rpo <= 15 and rto <= 45
            else "RESTORED_WITH_SLA_RISK"
        )

        log = RecoveryLog(
            event_type="RESTORE",
            affected_table="simulated_orders",
            status=status,
            rpo_minutes=rpo,
            rto_seconds=rto,
            message="Restauración simulada desde último backup válido"
        )

        db.add(log)
        db.commit()

        return {
            "message": "Restauración completada",
            "affected_table": "simulated_orders",
            "rpo_minutes": rpo,
            "rto_seconds": rto,
            "status": status
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