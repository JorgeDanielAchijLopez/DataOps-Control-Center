from app.database import SessionLocal
from app.models.db_metric import DBMetric
from app.models.alert_log import AlertLog
from app.models.replication_status import ReplicationStatus
from app.models.backup_history import BackupHistory


def run_alert_engine():

    db = SessionLocal()

    try:

        latest_metrics = db.query(
            DBMetric
        ).order_by(
            DBMetric.id.desc()
        ).limit(
            5
        ).all()

        for metric in latest_metrics:

            if metric.cpu > 85:

                db.add(
                    AlertLog(
                        db_id=metric.connection_id,
                        severity="WARNING",
                        condition="CPU > 85%",
                        message=f"CPU alto detectado: {metric.cpu}%",
                        status="OPEN"
                    )
                )

            if metric.deadlocks > 3:

                db.add(
                    AlertLog(
                        db_id=metric.connection_id,
                        severity="CRITICAL",
                        condition="Deadlocks > 3",
                        message=f"Deadlocks críticos detectados: {metric.deadlocks}",
                        status="OPEN"
                    )
                )

            if metric.disk_usage > 90:

                db.add(
                    AlertLog(
                        db_id=metric.connection_id,
                        severity="CRITICAL",
                        condition="Disco > 90%",
                        message=f"Uso de disco crítico: {metric.disk_usage}%",
                        status="OPEN"
                    )
                )

            if metric.connections > 80:

                db.add(
                    AlertLog(
                        db_id=metric.connection_id,
                        severity="WARNING",
                        condition="Conexiones > umbral",
                        message=f"Muchas conexiones activas: {metric.connections}",
                        status="OPEN"
                    )
                )

        latest_replication = db.query(
            ReplicationStatus
        ).order_by(
            ReplicationStatus.id.desc()
        ).first()

        if latest_replication and latest_replication.replication_lag > 10:

            db.add(
                AlertLog(
                    db_id=None,
                    severity="WARNING",
                    condition="Lag replicación > 10 seg",
                    message=f"Lag de replicación alto: {latest_replication.replication_lag} seg",
                    status="OPEN"
                )
            )

        latest_backup = db.query(
            BackupHistory
        ).order_by(
            BackupHistory.id.desc()
        ).first()

        if latest_backup and latest_backup.status == "FAILED":

            db.add(
                AlertLog(
                    db_id=None,
                    severity="CRITICAL",
                    condition="Backup fallido",
                    message=f"Fallo detectado en backup: {latest_backup.file_name}",
                    status="OPEN"
                )
            )

        db.commit()

        print(
            "Alert Engine ejecutado con reglas extendidas",
            flush=True
        )

    finally:

        db.close()