from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from datetime import datetime

from app.database import Base


class BackupHistory(Base):

    __tablename__ = "backup_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    backup_type = Column(
        String
    )

    file_name = Column(
        String
    )

    size_mb = Column(
        Float
    )

    duration_seconds = Column(
        Float
    )

    restore_point = Column(
        String
    )

    status = Column(
        String
    )

    checksum = Column(
        String
    )

    cloud_url = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )