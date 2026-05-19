from app.database import SessionLocal
from app.models.db_metric import DBMetric
from app.models.alert_log import AlertLog


def run_alert_engine():

    db=SessionLocal()

    try:

        metrics=db.query(
            DBMetric
        ).order_by(
            DBMetric.id.desc()
        ).limit(
            5
        ).all()

        for metric in metrics:

            if metric.cpu>85:

                alert=AlertLog(

                    db_id=
                    metric.connection_id,

                    severity=
                    "WARNING",

                    condition=
                    "CPU > 85%",

                    message=
                    f"CPU alto detectado: {metric.cpu}%"
                )

                db.add(
                    alert
                )

            if metric.deadlocks>3:

                alert=AlertLog(

                    db_id=
                    metric.connection_id,

                    severity=
                    "CRITICAL",

                    condition=
                    "Deadlocks > 3",

                    message=
                    f"Deadlocks críticos detectados: {metric.deadlocks}"
                )

                db.add(
                    alert
                )

        db.commit()

        print(
            "Alert Engine ejecutado",
            flush=True
        )

    finally:

        db.close()