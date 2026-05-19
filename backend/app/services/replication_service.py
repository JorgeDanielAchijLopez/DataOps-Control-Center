import random

from app.database import SessionLocal
from app.models.replication_status import ReplicationStatus


def monitor_replication():

    db = SessionLocal()

    try:

        lag = round(
            random.uniform(
                0,
                15
            ),
            2
        )

        status = (
            "HEALTHY"
            if lag < 5
            else "CRITICAL"
        )

        replication = ReplicationStatus(

            primary_node=
            "postgres-primary",

            replica_node=
            "postgres-replica",

            replication_lag=
            lag,

            status=
            status
        )

        db.add(
            replication
        )

        db.commit()

        print(
            "Replicación monitoreada",
            flush=True
        )

    finally:

        db.close()