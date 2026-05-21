import random

from app.database import SessionLocal
from app.models.snapshot_log import SnapshotLog


def create_snapshot(name, description):

    db = SessionLocal()

    try:
        rpo = round(random.uniform(5, 20), 2)
        rto = round(random.uniform(20, 60), 2)

        sla_status = (
            "CUMPLE"
            if rpo <= 15 and rto <= 45
            else "NO CUMPLE"
        )

        snapshot = SnapshotLog(
            name=name,
            description=description,
            status="CREATED",
            rpo_minutes=rpo,
            rto_minutes=rto,
            sla_status=sla_status
        )

        db.add(snapshot)
        db.commit()

        print(
            f"Snapshot {name} creado",
            flush=True
        )

    finally:
        db.close()


def create_default_snapshots():

    create_snapshot(
        "PRE_DEPLOY",
        "Snapshot antes de despliegue"
    )

    create_snapshot(
        "PRE_TEST",
        "Snapshot antes de pruebas"
    )

    create_snapshot(
        "PRE_IMPORT",
        "Snapshot antes de importación"
    )