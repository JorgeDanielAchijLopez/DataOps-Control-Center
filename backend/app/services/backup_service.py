import os
import random
import hashlib
import boto3

from datetime import datetime

from app.database import SessionLocal
from app.models.backup_history import BackupHistory


def create_hash(data):

    return hashlib.sha256(
        data.encode()
    ).hexdigest()


def upload_to_s3(local_path, file_name):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )

    bucket = os.getenv("AWS_BUCKET")

    s3_key = f"backups/{file_name}"

    s3.upload_file(
        local_path,
        bucket,
        s3_key
    )

    return f"s3://{bucket}/{s3_key}"


def generate_backup(backup_type):

    db = SessionLocal()

    try:

        backup_type = backup_type.upper()

        fake_content = str(
            random.randint(
                1000,
                9999
            )
        )

        checksum = create_hash(
            fake_content
        )

        file_name = (
            f"{backup_type}_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            ".bak"
        )

        os.makedirs(
            "backups",
            exist_ok=True
        )

        local_path = f"backups/{file_name}"

        with open(
            local_path,
            "w"
        ) as file:

            file.write(
                fake_content
            )

        remote_url = None

        if os.getenv("CLOUD_PROVIDER") == "AWS":

            remote_url = upload_to_s3(
                local_path,
                file_name
            )

        backup = BackupHistory(

            backup_type=backup_type,

            file_name=file_name,

            checksum=checksum,

            size_mb=round(
                random.uniform(
                    20,
                    500
                ),
                2
            ),

            duration_seconds=round(
                random.uniform(
                    1,
                    20
                ),
                2
            ),

            restore_point=f"RESTORE_{backup_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",

            status="SUCCESS",

            cloud_url=remote_url
        )

        db.add(
            backup
        )

        db.commit()

        return {
            "backup_type": backup_type,
            "file_name": file_name,
            "checksum": checksum,
            "cloud_url": remote_url,
            "status": "SUCCESS"
        }

    finally:

        db.close()