import random
import time
import hashlib

from datetime import datetime

from app.database import SessionLocal
from app.models.backup_history import BackupHistory


def generate_backup(
    backup_type="FULL"
):

    db = SessionLocal()

    try:

        start = time.time()

        size_map = {
            "FULL":
            random.uniform(30,50),

            "DIFF":
            random.uniform(10,20),

            "INC":
            random.uniform(1,8)
        }

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        content = (
            f"{backup_type}"
            f"{timestamp}"
        )

        checksum = hashlib.sha256(
            content.encode()
        ).hexdigest()

        backup = BackupHistory(

            backup_type=
            backup_type,

            file_name=
            f"{backup_type.lower()}_{timestamp}.bak",

            size_mb=round(
                size_map[
                    backup_type
                ],
                2
            ),

            duration_seconds=
            time.time()-start,

            restore_point=
            f"RESTORE_{timestamp}",

            status=
            "SUCCESS",

            checksum=
            checksum,

            cloud_url=
            "pendiente_subida_nube"
        )

        db.add(
            backup
        )

        db.commit()

        print(
            f"{backup_type} backup generado",
            flush=True
        )

    finally:

        db.close()