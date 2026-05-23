from app.database import SessionLocal
from app.models.db_metric import DBMetric
from app.models.alert_log import AlertLog
from app.models.replication_status import ReplicationStatus
from app.models.backup_history import BackupHistory
from app.services.email_service import send_alert_email


def create_alert(
    db,
    db_id,
    severity,
    condition,
    message
):

    alert = AlertLog(
        db_id=db_id,
        severity=severity,
        condition=condition,
        message=message,
        status="OPEN"
    )

    db.add(alert)

    if severity in ["CRITICAL", "WARNING"]:

        send_alert_email(
            subject=f"Alerta crítica DataOps: {condition}",
            message=message
        )


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

                create_alert(
                    db=db,
                    db_id=metric.connection_id,
                    severity="WARNING",
                    condition="CPU > 85%",
                    message=f"CPU alto detectado: {metric.cpu}%"
                )

            if metric.deadlocks > 3:

                create_alert(
                    db=db,
                    db_id=metric.connection_id,
                    severity="CRITICAL",
                    condition="Deadlocks > 3",
                    message=f"Deadlocks críticos detectados: {metric.deadlocks}"
                )

            if metric.disk_usage > 90:

                create_alert(
                    db=db,
                    db_id=metric.connection_id,
                    severity="CRITICAL",
                    condition="Disco > 90%",
                    message=f"Uso de disco crítico: {metric.disk_usage}%"
                )

            if metric.connections > 80:

                create_alert(
                    db=db,
                    db_id=metric.connection_id,
                    severity="WARNING",
                    condition="Conexiones > umbral",
                    message=f"Muchas conexiones activas: {metric.connections}"
                )

        latest_replication = db.query(
            ReplicationStatus
        ).order_by(
            ReplicationStatus.id.desc()
        ).first()

        if latest_replication and latest_replication.replication_lag > 10:

            create_alert(
                db=db,
                db_id=None,
                severity="WARNING",
                condition="Lag replicación > 10 seg",
                message=f"Lag de replicación alto: {latest_replication.replication_lag} seg"
            )

        latest_backup = db.query(
            BackupHistory
        ).order_by(
            BackupHistory.id.desc()
        ).first()

        if latest_backup and latest_backup.status == "FAILED":

            create_alert(
                db=db,
                db_id=None,
                severity="CRITICAL",
                condition="Backup fallido",
                message=f"Fallo detectado en backup: {latest_backup.file_name}"
            )

        db.commit()

        print(
            "Alert Engine ejecutado con correo SMTP",
            flush=True
        )

    finally:

        db.close()