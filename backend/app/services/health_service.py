from app.database import SessionLocal
from app.models.connection import Connection
from app.models.db_metric import DBMetric

import random


def run_health_check():

    db=SessionLocal()

    try:

        connections=db.query(
            Connection
        ).all()

        for connection in connections:

            metric=DBMetric(

                connection_id=
                connection.id,

                cpu=round(
                    random.uniform(
                        10,
                        90
                    ),
                    2
                ),

                memory=round(
                    random.uniform(
                        20,
                        95
                    ),
                    2
                ),

                connections=random.randint(
                    1,
                    100
                ),

                locks=random.randint(
                    0,
                    10
                ),

                deadlocks=random.randint(
                    0,
                    5
                ),

                disk_usage=round(
                    random.uniform(
                        30,
                        95
                    ),
                    2
                )
            )

            db.add(
                metric
            )

        db.commit()

        print(
            "Health Check ejecutado correctamente",
            flush=True
        )

    finally:

        db.close()